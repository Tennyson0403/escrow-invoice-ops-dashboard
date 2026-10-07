"""Generate SYNTHETIC escrow insurance invoice data for the Power BI dashboard.

All values are randomly generated (seed 42). No real client, loan or payment data is used.
Usage: python scripts/generate_data.py --rows 150 --out data/escrow_invoices.csv
"""
import argparse
import csv
import random
from datetime import date, timedelta


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=150)
    parser.add_argument("--out", default="data/escrow_invoices.csv")
    args = parser.parse_args()

    random.seed(42)
    start = date(2026, 1, 5)
    loan_types = ["Conventional", "FHA", "VA"]
    payees = ["Servicing Agent", "Vendor"]
    statuses = ["Disbursed"] * 82 + ["Pending"] * 8 + ["Discarded-Duplicate"] * 6 + ["Resubmitted"] * 4

    rows = []
    for i in range(1, args.rows + 1):
        received = start + timedelta(days=random.randint(0, 250))
        investor_coded = random.random() < 0.35
        approval_days = random.randint(1, 5) if investor_coded else 0
        processing_days = random.randint(1, 3) + approval_days
        status = random.choice(statuses)
        processed = received + timedelta(days=processing_days) if status != "Pending" else ""
        rows.append({
            "invoice_id": f"INV-{i:05d}",
            "received_date": received.isoformat(),
            "processed_date": processed.isoformat() if processed else "",
            "loan_type": random.choice(loan_types),
            "investor_coded": "Y" if investor_coded else "N",
            "payee_type": random.choice(payees),
            "invoice_amount": round(random.uniform(350, 6200), 2),
            "approval_days": approval_days,
            "processing_days": processing_days if status != "Pending" else "",
            "status": status,
        })

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
