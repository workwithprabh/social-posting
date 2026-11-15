#!/usr/bin/env python3
"""Turn a bank or UPI statement into rows for the Freelance Payment sheet.

    python finance/import_statement.py STATEMENT --owner carrot|prabh|jiti --month 2026-11 [--out rows.json]

STATEMENT can be CSV, XLS/XLSX or PDF (bank statement tables, or PhonePe / Google Pay exports).
--owner is whose account the statement is: it decides which expense list (Prabh / Jiti / Carrot) the rows go to.
--month keeps only that month's transactions (YYYY-MM). Leave it out to keep everything.

Nothing is written to the sheet. The script prints a review table and writes a JSON file with:
  expenses: one row per label, several payments to the same label joined as a formula (=3841+4199+4179),
            the same way the sheet has always been filled in
  check:    payments that matched no rule or need a client named (Meta / Google ads, Deepak)
  transfers: money moved to or from a partner (reimbursements and withdrawals, not expenses)
  credits:  money received, matched to a client in the billing table where possible
Claude writes the reviewed rows into the month tab with the Google Sheets connector.
"""
import argparse
import json
import re
import sys
from collections import OrderedDict
from datetime import datetime
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent

DATE_FORMATS = ["%d/%m/%Y", "%d/%m/%y", "%d-%m-%Y", "%d-%m-%y", "%d %b %Y", "%d %b, %Y", "%b %d, %Y",
                "%d-%b-%Y", "%d-%b-%y", "%Y-%m-%d", "%d.%m.%Y", "%d %B %Y", "%B %d, %Y"]


def parse_date(s):
    s = str(s).strip()
    if not s or s.lower() in ("nan", "nat", "none"):
        return None
    s = re.sub(r"\s+\d{1,2}:\d{2}(:\d{2})?\s*(am|pm)?$", "", s, flags=re.I)
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f).date()
        except ValueError:
            pass
    try:
        return pd.to_datetime(s, dayfirst=True).date()
    except Exception:
        return None


def parse_amount(x):
    if x is None:
        return 0.0
    s = str(x).strip().replace(",", "").replace("₹", "").replace("INR", "").replace("Rs.", "").strip()
    if s.lower() in ("", "nan", "none", "-"):
        return 0.0
    m = re.search(r"-?\d+(\.\d+)?", s)
    return abs(float(m.group())) if m else 0.0


# ---------- reading the statement ----------

HEADER_WORDS = {
    "date": ["txn date", "transaction date", "value date", "date"],
    "narration": ["narration", "description", "particulars", "remarks", "details", "transaction details"],
    "debit": ["withdrawal", "debit", "dr amount", "withdrawals", "paid out"],
    "credit": ["deposit", "credit", "cr amount", "deposits", "paid in"],
    "amount": ["amount"],
    "type": ["dr/cr", "cr/dr", "type", "dr / cr"],
}


def pick_columns(header):
    cols = {}
    low = [str(h).strip().lower() for h in header]
    for key, words in HEADER_WORDS.items():
        for w in words:
            hit = next((i for i, h in enumerate(low) if w in h and i not in cols.values()), None)
            if hit is not None:
                cols[key] = hit
                break
    return cols


def rows_to_txns(rows):
    """rows: list of lists. Find the header row, then read transactions under it."""
    for hi, row in enumerate(rows):
        cols = pick_columns(row)
        if "date" in cols and "narration" in cols and ({"debit", "credit"} & cols.keys() or "amount" in cols):
            break
    else:
        return []
    txns = []
    last = None
    for row in rows[hi + 1:]:
        row = list(row) + [None] * (len(rows[hi]) - len(row))
        d = parse_date(row[cols["date"]])
        narr = " ".join(str(row[cols["narration"]] or "").split())
        if d is None:
            if last and narr and narr.lower() != "nan":  # narration wrapped onto the next line
                last["narration"] += " " + narr
            continue
        if "debit" in cols or "credit" in cols:
            dr = parse_amount(row[cols["debit"]]) if "debit" in cols else 0.0
            cr = parse_amount(row[cols["credit"]]) if "credit" in cols else 0.0
        else:
            amt = parse_amount(row[cols["amount"]])
            t = str(row[cols["type"]]).lower() if "type" in cols else ""
            is_cr = "cr" in t or "credit" in t or str(row[cols["amount"]]).strip().startswith("+")
            dr, cr = (0.0, amt) if is_cr else (amt, 0.0)
        if not dr and not cr:
            continue
        last = {"date": d, "narration": narr, "debit": dr, "credit": cr}
        txns.append(last)
    return txns


APP_LINE = re.compile(
    r"(?P<date>[A-Z][a-z]{2} \d{1,2}, \d{4}|\d{1,2} [A-Z][a-z]{2},? \d{4})\s+(?:\d{1,2}:\d{2}\s*[ap]m\s+)?"
    r"(?P<what>(?:Paid to|Received from|Sent to|Money sent to|Money received from)\s+.+?)\s+"
    # the rupee sign often extracts as another character, or as Rs / INR
    r"(?:(?P<type>DEBIT|CREDIT)\s*(?:₹|Rs\.?|INR|[^\d\s])?|₹|Rs\.?|INR)\s?(?P<amt>[\d,]+(?:\.\d+)?)", re.I)


def read_pdf(path):
    import pdfplumber
    rows, text = [], []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                rows.extend(table)
            text.append(page.extract_text() or "")
    txns = rows_to_txns(rows) if rows else []
    if txns:
        return txns
    # PhonePe / Google Pay style: one line per payment
    for m in APP_LINE.finditer("\n".join(text)):
        what = m.group("what")
        is_cr = (m.group("type") or "").upper() == "CREDIT" or what.lower().startswith(("received", "money received"))
        amt = parse_amount(m.group("amt"))
        txns.append({"date": parse_date(m.group("date")), "narration": what,
                     "debit": 0.0 if is_cr else amt, "credit": amt if is_cr else 0.0})
    return txns


def read_statement(path):
    p = Path(path)
    ext = p.suffix.lower()
    if ext == ".pdf":
        return read_pdf(p)
    if ext in (".xls", ".xlsx"):
        sheets = pd.read_excel(p, sheet_name=None, header=None, dtype=str)
        rows = [r for df in sheets.values() for r in df.fillna("").values.tolist()]
    else:
        df = pd.read_csv(p, header=None, dtype=str, skip_blank_lines=False, on_bad_lines="skip", engine="python")
        rows = df.fillna("").values.tolist()
    return rows_to_txns(rows)


# ---------- classifying ----------

UPI_NOISE = {"upi", "dr", "cr", "imps", "neft", "rtgs", "p2a", "p2m", "payment", "paid", "to", "from", "via",
             "sent", "using", "collect", "pay", "ybl", "okaxis", "oksbi", "okhdfcbank", "okicici", "paytm", "ibl"}


def payee_name(narr):
    """Best guess at the payee in a UPI / NEFT narration, for unmatched rows."""
    m = re.match(r"(?:paid to|sent to|money sent to|received from|money received from)\s+(.+)", narr, re.I)
    if m:
        return m.group(1).strip().title()
    for part in re.split(r"[/|\-]", narr):
        words = [w for w in re.findall(r"[A-Za-z][A-Za-z.&']+", part) if w.lower() not in UPI_NOISE]
        if words and not re.search(r"\d", part) and "@" not in part and len(" ".join(words)) > 2:
            return " ".join(words).title()
    return narr[:40]


def matches(words, text):
    return any((re.search(w, text) if any(c in w for c in "\\[]()|^$") else w in text) for w in words)


def classify(txn, cfg, owner):
    text = " " + txn["narration"].lower() + " "
    amount = txn["debit"] or txn["credit"]
    for who, words in cfg["partners"].items():
        if who.startswith("_") or who == owner:
            continue
        if matches(words, text):
            return {"kind": "transfer", "label": f"{'to' if txn['debit'] else 'from'} {who.title()}"}
    if txn["credit"]:
        for client, words in cfg["clients"].items():
            if not client.startswith("_") and matches(words, text):
                return {"kind": "credit", "label": client}
        return {"kind": "credit", "label": payee_name(txn["narration"]), "check": True}
    for r in cfg["rules"]:
        if "max_amount" in r and amount > r["max_amount"]:
            continue
        if "min_amount" in r and amount < r["min_amount"]:
            continue
        if matches(r["match"], text):
            return {"kind": r.get("kind", "expense"), "label": r["label"], "check": r.get("check", False),
                    "fuel": r.get("fuel", False)}
    return {"kind": "expense", "label": payee_name(txn["narration"]), "check": True}


def parse_shoots(s):
    """'3=Mahindra Arav; 4=Capital Hyundai; 24=DM Mahindra / Car & Bike' -> {3: 'Mahindra Arav', ...}"""
    shoots = {}
    for part in filter(None, (p.strip() for p in (s or "").split(";"))):
        day, _, client = part.partition("=")
        shoots[int(re.sub(r"\D", "", day))] = client.strip()
    return shoots


def money(x):
    return int(x) if float(x).is_integer() else round(x, 2)


def cell(amounts):
    """One amount stays a number; several become =a+b+c, as the sheet does."""
    if len(amounts) == 1:
        return money(amounts[0])
    return "=" + "+".join(str(money(a)) for a in amounts)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("statement")
    ap.add_argument("--owner", required=True, choices=["carrot", "prabh", "jiti"])
    ap.add_argument("--month", help="YYYY-MM")
    ap.add_argument("--shoots", help="shoot days of the month, '3=Mahindra Arav; 4=Capital Hyundai' "
                    "(from the month tab's Shoot Date notes); required for a personal account")
    ap.add_argument("--rules", default=str(HERE / "rules.json"))
    ap.add_argument("--out", default="statement_rows.json")
    a = ap.parse_args()

    personal = a.owner in ("prabh", "jiti")
    shoots = parse_shoots(a.shoots)
    if personal and not (a.month and shoots):
        sys.exit("A personal account needs --month and --shoots: only spends on shoot days count for the company.")

    cfg = json.load(open(a.rules))
    txns = read_statement(a.statement)
    if not txns:
        sys.exit("No transactions found. Check the file, or send a CSV/XLSX export instead of a PDF.")
    if a.month:
        y, m = map(int, a.month.split("-"))
        txns = [t for t in txns if t["date"] and (t["date"].year, t["date"].month) == (y, m)]

    expenses, check, transfers, credits = OrderedDict(), [], [], []
    ask_fuel, skipped = [], []
    for t in sorted(txns, key=lambda t: t["date"]):
        c = classify(t, cfg, a.owner)
        rec = {"date": t["date"].isoformat(), "amount": money(t["debit"] or t["credit"]),
               "label": c["label"], "narration": t["narration"]}
        if c["kind"] == "ignore":
            skipped.append(rec)
            continue
        if personal and c["kind"] == "expense":
            # Personal account: a spend counts for the company only on a shoot day, and is named after
            # that shoot ("Mahindra Arav Food"). Fuel on other days is asked about; the rest is left out.
            client = shoots.get(t["date"].day)
            if client is None:
                (ask_fuel if c.get("fuel") else skipped).append(rec)
                continue
            rec["label"] = c["label"] = f"{client} {c['label']}"
            rec["shoot"] = client
        if c["kind"] == "transfer":
            transfers.append(rec)
        elif c["kind"] == "credit":
            rec["matched"] = not c.get("check")
            credits.append(rec)
        elif c.get("check"):
            check.append(rec)
        else:
            expenses.setdefault(c["label"], []).append(t["debit"])

    out = {
        "owner": a.owner,
        "month": a.month,
        "expenses": [[label, cell(v)] for label, v in expenses.items()],
        "expenses_total": money(sum(sum(v) for v in expenses.values())),
        "check": check,
        "ask_fuel": ask_fuel,
        "left_out": skipped,
        "transfers": transfers,
        "credits": credits,
    }
    Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False))

    print(f"{len(txns)} transactions, owner {a.owner}, month {a.month or 'all'}")
    print(f"\nEXPENSES for the {a.owner.title()} list (total {out['expenses_total']}):")
    for label, v in out["expenses"]:
        print(f"  {label:32} {v}")
    if personal:
        print("  shoot days: " + ", ".join(f"{d} {c}" for d, c in sorted(shoots.items())))
    for name, items in (("NEEDS A LABEL / CLIENT", check),
                        ("FUEL ON A NON-SHOOT DAY (ask whether to add)", ask_fuel),
                        ("PARTNER TRANSFERS", transfers), ("MONEY RECEIVED", credits),
                        ("LEFT OUT: card bill payments, and personal spends on non-shoot days", skipped)):
        if items:
            print(f"\n{name}:")
            for r in items:
                flag = "" if r.get("matched", True) else "  (client?)"
                print(f"  {r['date']}  {r['amount']:>10}  {r['label'][:28]:28}  {r['narration'][:70]}{flag}")
    print(f"\nWrote {a.out}")


if __name__ == "__main__":
    main()
