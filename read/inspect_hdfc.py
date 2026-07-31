import pandas as pd
from pathlib import Path

path = Path('hdfc.xlsx')
print('exists', path.exists())
xl = pd.ExcelFile(path)
print('sheets', xl.sheet_names)

sheet = 'Combined'
df = pd.read_excel(path, sheet_name=sheet)
print('\nSHEET', sheet, 'shape', df.shape)
print('columns', list(df.columns))
print(df.head(40).to_string(index=False))
print('\nNon-empty rows with Date/Withdrawal/Deposit:')
subset = df[['Date', 'Narration', 'Chq./Ref.No.', 'ValueDt', 'WithdrawalAmt.', 'DepositAmt.', 'ClosingBalance']].copy()
print(subset.head(60).to_string(index=False))
