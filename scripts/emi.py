"""City-wise on-road price and EMI for a model, from CarDekho's public price pages.

Usage:
  python scripts/emi.py hyundai/creta noida gurgaon ghaziabad [--down 150000 | --down-pct 10] [--rate 9.8] [--months 60]

For each city: the base variant's ex-showroom, registration (RTO), insurance, other charges and on-road price
(mandatory items only; CarDekho's optional accessories are left out), the loan after the down payment, the EMI and
the total interest, plus the on-road price CarDekho lists for each variant in that city.
Model slugs are CarDekho's: hyundai/creta, hyundai/venue, hyundai/exter, mahindra/xuv-3xo, mahindra/thar-roxx ...
Numbers are indicative; dealer prices can differ. Prints JSON.
"""
import argparse
import html
import json
import re
import urllib.request

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'


def page_text(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    t = urllib.request.urlopen(req, timeout=60).read().decode('utf-8', 'ignore')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))


def rupees(s):
    return int(s.replace(',', ''))


def city_prices(model, city):
    url = f'https://www.cardekho.com/{model}/price-in-{city}'
    x = page_text(url)
    m = re.search(r'([A-Za-z0-9() .+\-]+?) \(Base Model\) Ex-Showroom Price Rs\. ([\d,]+) Registration Charges Rs\. ([\d,]+) '
                  r'Insurance .*? Rs\. ([\d,]+) Others Rs\. ([\d,]+)', x)
    if not m:
        raise RuntimeError(f'No price breakdown found at {url}')
    variant, exs, rto, ins, oth = m.group(1).strip(), *[rupees(g) for g in m.groups()[1:]]
    variant = re.sub(r'^.*\b(?:Manual|Automatic) ', '', variant)
    listed = []
    for name, lakh in re.findall(r'((?:Hyundai|Mahindra) [^*]+?) Rs\. ([\d.]+) Lakh \*', x[:x.find('Ex-Showroom Price')]):
        listed.append({'variant': name.split('Variants On-Road Price ')[-1].strip(), 'on_road_lakh': float(lakh)})
    return dict(city=city, source=url, base_variant=variant, ex_showroom=exs, registration=rto, insurance=ins, others=oth,
                on_road=exs + rto + ins + oth, variants_on_road=listed[:12])


def emi(principal, rate_pct, months):
    r = rate_pct / 1200
    return principal * r * (1 + r) ** months / ((1 + r) ** months - 1)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('model'); ap.add_argument('cities', nargs='+')
    ap.add_argument('--down', type=int); ap.add_argument('--down-pct', type=float, default=10)
    ap.add_argument('--rate', type=float, default=9.8); ap.add_argument('--months', type=int, default=60)
    a = ap.parse_args()
    out = []
    for c in a.cities:
        p = city_prices(a.model, c)
        down = a.down if a.down is not None else round(p['on_road'] * a.down_pct / 100)
        loan = p['on_road'] - down
        e = emi(loan, a.rate, a.months)
        p.update(down_payment=down, loan=loan, rate_pct=a.rate, months=a.months, emi=round(e), total_interest=round(e * a.months - loan))
        out.append(p)
    print(json.dumps(out, indent=1, ensure_ascii=False))
