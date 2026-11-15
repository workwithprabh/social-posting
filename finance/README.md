# Company finances: Freelance Payment sheet

Sheet: **Freelance Payment**, id `1tucoQHv6ktk28JxGw2dtAqWJQKqwPYTStugQQ5mqo_Y`. Read and write it with the Google
Sheets connector. One tab per month ("October 2026"); older months are hidden tabs. The layout is the partners'
own and stays as it is.

## Month tab layout (current, from April 2026)

| Area | Cells | What it holds |
|---|---|---|
| Totals | B1:J3 | Expenses `=SUM(rows 6-29)`, Paid `=SUM(rows 33-39)` (unused, so always 0), Pending |
| Prabh expenses | B6:C29 | Detail, Amount |
| Jiti expenses | F6:G29 | Detail, Amount |
| Carrot (company) expenses | I6:J29 | Detail, Amount |
| Notes | M:Q | shoot dates per client, small one-off shoot costs |
| Bill dates | B42:C44 | Bill of (month), Bill Raised On (1st of next month), Payment to be rec by (30th) |
| Billing table | B47:L52(+) | Status (`Rec` / `Not Rec`), Receiveable (client), Final Payment + GST, retainer, ad spend Be Carrot, ad spend/prabh, GST, paid to prabh, paid to jiti, paid to carrot, Surplus |
| Totals row | D53 | sums of the billing columns |
| Totals | E54, E55, C56, C57 | Total Expense `=SUM(D59:D61)`, Total Payement rec `=D53`, Total Recieved `=SUMIFS(D:D,B:B,"Rec")`, Total Not Recieved |
| Settlement | C58:G61 | per partner: Expenses (from row 1), Already Withdrawn (`paid to` columns I/J/K where `Rec`) |
| Profit | B63:F66 | Recieved `=D53`, After Expense, Per Share Profit `/3`; each partner gets share - withdrawn + own expenses |

Rows shift by one when the billing table has an extra client row (August 2026 has Cynor at row 53, so everything
below moves down one). Read the tab before writing to the lower half.

Billing: Final Payment + GST is `=(E*18%)+E` for trob, Capital Hyundai, MR Hyundai and one-off jobs; Arav and Dee Emm
Hyundai are billed without GST (`=E`). GST collected is included in "Recieved"; the GST paid to the government shows
up as "GST Payment" in Carrot's expenses the next month.

Fixed on 15 Nov 2026: "Already Withdrawn" pointed one column to the left (GST / paid to prabh / paid to jiti) in
April and June to October 2026, after the "ad spend Be Carrot" column was added in April; "Total Recieved" had a broken
SUMIFS in every 2026 tab; September and October had no profit formulas; October's Prabh list repeated
September's five entries (copied when the tab was made) and they were removed from October.

## How expenses are written (learned from the 2025-2026 tabs)

- **Whose list:** the account that paid. Company account → Carrot. A partner's own UPI → that partner.
- **One row per payee per month.** Several payments to the same payee go in one cell as a formula:
  `=3841+4199+4179` (petrol), `=11500+15800` (Ammar). Small food spends are summed the same way.
- **Labels:** people by first name (Anusha, Shaurya, Divya, Sahil, Ekta); teams with their role
  (Deepak Video Team, Ammar Video Editor); fixed costs by name (91 Springboard Seat, 91 Springboard Parking,
  GST Payment, CA Payment, Chatgpt, Claude, Petrol).
- **Client work is prefixed with the client:** "MR Hyundai Ads", "October Be carrot fb funds add",
  "DM Hyundai petrol", "Arav food". Meta top-ups need the client named; the statement doesn't say which.
- **Recurring every month:** Carrot: 91 Springboard Seat and Parking, GST Payment, Petrol, Chatgpt, Deepak Video
  Team, Ammar Video Editor, freelancers. Jiti: Claude (1932). CA Payment when billed.
- **Partner reimbursements and withdrawals** are not expenses. Money from the company to a partner goes in the
  billing table's `paid to prabh / jiti / carrot` columns against the client whose payment funded it.

`rules.json` holds these mappings. Add a rule whenever a new payee gets a label.

## Shoot-day rule for personal accounts

A partner's personal spend counts as a company expense only on a **shoot day**. Shoot days are in the month tab's
"Shoot Date" notes (column M date, column N client; for October 2026: 3 Mahindra Arav, 4 Capital Hyundai, 12 MR
Hyundai, ...). On a personal statement:

- Spends on a shoot day **between 11 am and 9 pm** go in that partner's list, named after the shoot
  ("Mahindra Arav food", "MR Hyundai fuel"). Before 11 am or after 9 pm they are personal.
- Fuel, CNG and Fastag count on a shoot day at any hour, and on the day just before or just after a shoot (named after
  that shoot). Fuel on any other day is left out.
- Everything else on a non-shoot day is personal and left out, and so are card bill payments, loan repayments and
  failed payments.
- Facebook ad top-ups count whatever the day. Meta is also paid through "Razorpay Checkout" and "PayU Checkout"; check
  the "fb funds add" rows already in the tab (and the tab before) before adding one, since they are often written
  in by hand.
- CRED has no statement: the partner sends screenshots of CRED's payment history; read the payee, date, time and
  amount from them and apply the same rules.

The company account has no such filter: everything on it is a company expense.

## Which statement to use

Payments are made with PhonePe and CRED. Both are only apps on top of a bank account or a credit card, so the
complete record is the **bank account statement** (net banking or the bank app, downloaded as XLS/CSV). It has every
PhonePe and CRED UPI payment. CRED has no statement download.

- Use the bank statement as the one source for each account. Don't also import the PhonePe statement for the same
  account and month: the same payments would be added twice.
- Payments made **with a credit card** (card swiped, or a RuPay card on UPI in CRED or PhonePe) are on the
  **credit card statement**, the monthly PDF the bank emails. Import that for card spends. The card bill paid
  through CRED shows in the bank statement as a CRED payment and is left out (`rules.json`).
- For a single missing payment, a screenshot of the CRED or PhonePe history works; Claude reads it and adds the row.

## Processing a statement

When a partner shares a UPI or bank statement (CSV, XLSX or PDF):

1. Save it to the session scratchpad (not the repo; statements never get committed).
2. Password-protected PDFs (IndusInd and card statements): pass `--password` or set `STATEMENT_PASSWORD`. The user
   gives the password in the conversation; never write it into this repo or any file.
3. Read the month tab's Shoot Date notes, then run
   `python finance/import_statement.py <file> --owner carrot|prabh|jiti --month 2026-10 --shoots "3=Mahindra Arav; 4=Capital Hyundai" --out <scratchpad>/rows.json`
   (`--shoots` and `--month` are required for prabh and jiti).
4. Show the user the result: the expense rows, the **needs a label** list (unknown payees, Meta/Google ads without a
   client), **fuel on a non-shoot day** to approve, partner transfers, money received, and what was left out as
   personal. Ask about the unclear ones.
5. Before adding anything, check it isn't already in the sheet: compare amounts (and dates in the Detail text)
   against that owner's list in this month's tab **and the tabs either side**. Entries are sometimes written in the
   month they were paid for, not the month they were paid ("Petrol 3rd oct" and "October Be carrot fb funds add" sit in
   the September 2026 tab).
6. Read the month tab, then append the new rows below the last filled row of that owner's list (rows 6-29) with
   `update_formulas`. If a label already has a row, add the new amounts to its formula
   (`=4248` → `=4248+1142`) instead of adding a second row.
7. Money received from a client pays the previous month's bill (an October receipt goes in the September tab, a
   November receipt in October). A regular client: set its Status to `Rec` after checking the amount against Final
   Payment + GST (Capital Hyundai pays less 1% TDS: 38,940 billed, 38,610 received). Any other client gets its own
   row: insert it above the billing totals row, Status `Rec`, retainer = amount / 1.18 when GST was charged, and
   extend the totals row's sums to include it. trob is the Dee Emm Mahindra monthly retainer.
8. Read the tab again and report the new totals.

Add rules for any label the user gave in step 3 to `rules.json`.

## Starting a new month

The month tab for a month is created at the start of it by copying the previous tab: clear the three expense lists,
the shoot notes and the `paid to` columns, set the billing rows to `Not Rec`, and update Bill of / Bill Raised On /
Payment to be rec by.
