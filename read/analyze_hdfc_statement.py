import re
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

WORKDIR = Path(__file__).resolve().parent
XLSX_PATH = WORKDIR / 'hdfc.xlsx'
OUT_HTML = WORKDIR / 'hdfc_statement_report.html'
OUT_CSV = WORKDIR / 'hdfc_transactions.csv'


def parse_date(value):
    if pd.isna(value):
        return pd.NaT
    if isinstance(value, (datetime, pd.Timestamp)):
        return pd.Timestamp(value)
    text = str(value).strip()
    if not text:
        return pd.NaT
    for fmt in ['%d/%m/%y', '%d/%m/%Y', '%d-%m-%y', '%d-%m-%Y']:
        try:
            return pd.Timestamp(datetime.strptime(text, fmt))
        except ValueError:
            continue
    return pd.NaT


def parse_amount(value):
    if pd.isna(value):
        return 0.0
    text = str(value).strip().replace(',', '')
    if not text or text in {'nan', 'None'}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def categorize_narration(narration):
    text = (narration or '').upper()
    if 'BLINKIT' in text or 'SWIGGY' in text or 'ZOMATO' in text or 'FOOD' in text:
        return 'Food & Dining'
    if 'RENT' in text or 'HOUSE' in text:
        return 'Rent / Housing'
    if 'GOOGLE' in text or 'PLAYSTORE' in text or 'NETFLIX' in text or 'SPOTIFY' in text:
        return 'Subscriptions / Entertainment'
    if 'JIO' in text or 'RECHARGE' in text or 'MOBILE' in text:
        return 'Mobile / Recharge'
    if 'MEDICAL' in text or 'HOSP' in text or 'PHARMA' in text:
        return 'Medical'
    if 'IRCTC' in text or 'TRAIN' in text or 'BUS' in text or 'CAB' in text:
        return 'Travel / Transport'
    if 'ELECTRIC' in text or 'SEDCL' in text or 'UTILITY' in text or 'BILL' in text:
        return 'Utilities'
    if 'UPI' in text and 'MONEY' in text:
        return 'Transfers'
    if 'ACHD' in text or 'NEFT' in text or 'RTGS' in text:
        return 'Bank Transfers'
    if 'POS' in text:
        return 'POS / Card Spend'
    return 'Other Expenses'


if not XLSX_PATH.exists():
    raise FileNotFoundError(f'Workbook not found: {XLSX_PATH}')

xl = pd.ExcelFile(XLSX_PATH)
print('Sheets:', xl.sheet_names)

sheet_name = 'Combined'
df = pd.read_excel(XLSX_PATH, sheet_name=sheet_name)
print('Loaded shape:', df.shape)

# Keep only rows that look like transaction rows
keep_cols = ['Date', 'Narration', 'Chq./Ref.No.', 'ValueDt', 'WithdrawalAmt.', 'DepositAmt.', 'ClosingBalance']
subset = df[[c for c in keep_cols if c in df.columns]].copy()

# Extract rows where Date is present and one of the amounts is present.
transaction_rows = subset[(subset['Date'].notna()) & ((subset['WithdrawalAmt.'].notna()) | (subset['DepositAmt.'].notna()))].copy()
transaction_rows = transaction_rows[~transaction_rows['Date'].astype(str).str.contains('Date', case=False, na=False)]

# Clean and standardize
transaction_rows['Date'] = transaction_rows['Date'].apply(parse_date)
transaction_rows['WithdrawalAmt.'] = transaction_rows['WithdrawalAmt.'].apply(parse_amount)
transaction_rows['DepositAmt.'] = transaction_rows['DepositAmt.'].apply(parse_amount)
transaction_rows['Narration'] = transaction_rows['Narration'].fillna('')
transaction_rows['Amount'] = transaction_rows['WithdrawalAmt.'] - transaction_rows['DepositAmt.']
transaction_rows['Type'] = transaction_rows['Amount'].apply(lambda x: 'Expense' if x < 0 else 'Deposit')
transaction_rows['Category'] = transaction_rows.apply(lambda r: 'Deposit' if r['Type'] == 'Deposit' else categorize_narration(r['Narration']), axis=1)

# Keep only real transactions
transaction_rows = transaction_rows[transaction_rows['Date'].notna()].copy()
transaction_rows = transaction_rows.sort_values('Date').reset_index(drop=True)

# Save cleaned rows
transaction_rows.to_csv(OUT_CSV, index=False)

summary = {
    'Total Transactions': len(transaction_rows),
    'Total Expenses': round(abs(transaction_rows.loc[transaction_rows['Type'] == 'Expense', 'Amount'].sum()), 2),
    'Total Deposits': round(transaction_rows.loc[transaction_rows['Type'] == 'Deposit', 'Amount'].sum(), 2),
    'Net Flow': round(transaction_rows['Amount'].sum(), 2),
}

monthly = transaction_rows.groupby(transaction_rows['Date'].dt.to_period('M')).agg(
    expenses=('Amount', lambda s: abs(s[s < 0].sum())),
    deposits=('Amount', lambda s: s[s > 0].sum()),
    transactions=('Amount', 'count')
)
monthly.index = monthly.index.astype(str)

category_summary = transaction_rows[transaction_rows['Type'] == 'Expense'].groupby('Category')['Amount'].sum().abs().sort_values(ascending=False)

deposit_summary = transaction_rows[transaction_rows['Type'] == 'Deposit'].groupby('Category')['Amount'].sum().sort_values(ascending=False)

# Charts
plt.figure(figsize=(8, 4))
plt.bar(monthly.index, monthly['expenses'], color='#d9534f')
plt.xticks(rotation=45)
plt.title('Monthly Expenses')
plt.ylabel('Amount (₹)')
plt.tight_layout()
plt.savefig(WORKDIR / 'monthly_expenses.png', dpi=200)
plt.close()

plt.figure(figsize=(8, 4))
plt.bar(monthly.index, monthly['deposits'], color='#5cb85c')
plt.xticks(rotation=45)
plt.title('Monthly Deposits')
plt.ylabel('Amount (₹)')
plt.tight_layout()
plt.savefig(WORKDIR / 'monthly_deposits.png', dpi=200)
plt.close()

plt.figure(figsize=(8, 4))
if not category_summary.empty:
    category_summary.plot(kind='bar', color='#337ab7')
    plt.title('Expenses by Category')
    plt.ylabel('Amount (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(WORKDIR / 'category_expenses.png', dpi=200)
    plt.close()

# Build HTML report
html = f"""
<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>Bank Statement Analysis Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #222; }}
    h1, h2 {{ color: #1f4e79; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 14px; margin-bottom: 16px; }}
    .stat {{ display: inline-block; width: 180px; margin-right: 12px; }}
    .chart {{ width: 100%; max-width: 700px; margin: 12px 0; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 8px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f5f5f5; }}
  </style>
</head>
<body>
  <h1>Bank Statement Analysis Report</h1>
  <p>Source: {XLSX_PATH.name}</p>

  <div class='card'>
    <h2>Key Summary</h2>
    <div class='stat'><b>Total transactions</b><br>{summary['Total Transactions']}</div>
    <div class='stat'><b>Total expenses</b><br>₹ {summary['Total Expenses']:.2f}</div>
    <div class='stat'><b>Total deposits</b><br>₹ {summary['Total Deposits']:.2f}</div>
    <div class='stat'><b>Net flow</b><br>₹ {summary['Net Flow']:.2f}</div>
  </div>

  <div class='card'>
    <h2>Monthly View</h2>
    <img class='chart' src='monthly_expenses.png' alt='Monthly expenses'>
    <img class='chart' src='monthly_deposits.png' alt='Monthly deposits'>
    <table>
      <tr><th>Month</th><th>Expenses</th><th>Deposits</th><th>Transactions</th></tr>
      {''.join(f"<tr><td>{m}</td><td>₹ {monthly.loc[m, 'expenses']:.2f}</td><td>₹ {monthly.loc[m, 'deposits']:.2f}</td><td>{int(monthly.loc[m, 'transactions'])}</td></tr>" for m in monthly.index)}
    </table>
  </div>

  <div class='card'>
    <h2>Expense Categories</h2>
    <img class='chart' src='category_expenses.png' alt='Expenses by category'>
    <table>
      <tr><th>Category</th><th>Amount</th></tr>
      {''.join(f"<tr><td>{cat}</td><td>₹ {amt:.2f}</td></tr>" for cat, amt in category_summary.items())}
    </table>
  </div>

  <div class='card'>
    <h2>Deposit Summary</h2>
    <table>
      <tr><th>Category</th><th>Amount</th></tr>
      {''.join(f"<tr><td>{cat}</td><td>₹ {amt:.2f}</td></tr>" for cat, amt in deposit_summary.items())}
    </table>
  </div>

  <div class='card'>
    <h2>Top Transactions</h2>
    <table>
      <tr><th>Date</th><th>Type</th><th>Category</th><th>Narration</th><th>Amount</th></tr>
      {''.join(f"<tr><td>{row['Date'].strftime('%d/%m/%Y')}</td><td>{row['Type']}</td><td>{row['Category']}</td><td>{row['Narration']}</td><td>₹ {abs(row['Amount']):.2f}</td></tr>" for _, row in transaction_rows.sort_values('Amount').head(15).iterrows())}
    </table>
  </div>
</body>
</html>
"""

OUT_HTML.write_text(html, encoding='utf-8')
print('Saved:', OUT_HTML)
print('Saved:', OUT_CSV)
print('Summary:')
print(summary)
print('Category summary:')
print(category_summary)
print('Deposit summary:')
print(deposit_summary)
