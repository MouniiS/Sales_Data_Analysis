"""Beginner sales analytics project. Run from the project directory: python analysis.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data' / 'sales_data.csv'
OUT = ROOT / 'outputs'
OUT.mkdir(exist_ok=True)

# 1) Load and inspect
raw = pd.read_csv(DATA)
print('--- RAW DATA PREVIEW ---')
print(raw.head())
print('\nDataset shape:', raw.shape)
print('\nData types:\n', raw.dtypes)
print('\nMissing values:\n', raw.isna().sum())
print('\nDuplicate rows:', raw.duplicated().sum())

# 2) Clean data
sales = raw.copy()
sales['Date'] = pd.to_datetime(sales['Date'], errors='coerce')
for col in ['Quantity','Unit_Price','Discount','Sales']:
    sales[col] = pd.to_numeric(sales[col], errors='coerce')
sales = sales.drop_duplicates()
sales = sales.dropna(subset=['Date','Quantity','Unit_Price','Sales','Category','Product','Region'])
sales = sales[sales['Quantity'] > 0]
sales = sales[sales['Sales'] >= 0]
sales['Month'] = sales['Date'].dt.to_period('M').astype(str)
sales.to_csv(OUT/'cleaned_sales_data.csv', index=False)

# 3) KPIs
revenue = sales['Sales'].sum()
orders = sales['Order_ID'].nunique()
units = sales['Quantity'].sum()
avg_order = revenue/orders if orders else 0
print('\n--- KEY PERFORMANCE INDICATORS ---')
print(f'Total revenue: {revenue:,.2f}')
print(f'Orders: {orders:,}')
print(f'Units sold: {units:,}')
print(f'Average order value: {avg_order:,.2f}')

# 4) Group analyses
category = sales.groupby('Category')['Sales'].sum().sort_values(ascending=False)
region = sales.groupby('Region')['Sales'].sum().sort_values(ascending=False)
monthly = sales.groupby('Month')['Sales'].sum().sort_index()
product = sales.groupby('Product')['Sales'].sum().sort_values(ascending=False).head(10)
payment = sales.groupby('Payment_Method')['Sales'].sum().sort_values(ascending=False)
quantity_category = sales.groupby('Category')['Quantity'].sum().sort_values(ascending=False)
for name, series in [('sales_by_category',category),('sales_by_region',region),('monthly_sales',monthly),('top_products',product),('sales_by_payment',payment),('quantity_by_category',quantity_category)]:
    series.to_csv(OUT/f'{name}.csv', header=['Sales_or_Quantity'])

# 5) Charts
plots = [
 (category,'Sales by Category','Category','Sales','bar','sales_by_category.png'),
 (region,'Sales by Region','Region','Sales','bar','sales_by_region.png'),
 (monthly,'Monthly Sales Trend','Month','Sales','line','monthly_sales.png'),
 (product.sort_values(),'Top 10 Products by Sales','Product','Sales','barh','top_10_products.png'),
 (payment,'Sales by Payment Method','Payment Method','Sales','bar','sales_by_payment.png'),
 (quantity_category,'Units Sold by Category','Category','Units Sold','bar','quantity_by_category.png')]
for series,title,xlabel,ylabel,kind,filename in plots:
    plt.figure(figsize=(10,5))
    if kind=='line': series.plot(kind='line',marker='o')
    else: series.plot(kind=kind)
    plt.title(title); plt.xlabel(xlabel); plt.ylabel(ylabel)
    if kind=='bar': plt.xticks(rotation=25,ha='right')
    plt.tight_layout(); plt.savefig(OUT/filename,dpi=160); plt.close()

# 6) Export report and findings (computed from this dataset)
best_cat=category.index[0]; best_region=region.index[0]; best_product=product.index[0]; best_payment=payment.index[0]
report=f'''SALES DATA ANALYSIS REPORT\n========================\n\nDataset records after cleaning: {len(sales)}\nTotal revenue: {revenue:,.2f}\nUnique orders: {orders:,}\nUnits sold: {units:,}\nAverage order value: {avg_order:,.2f}\n\nHighest sales category: {best_cat} ({category.iloc[0]:,.2f})\nHighest sales region: {best_region} ({region.iloc[0]:,.2f})\nTop product by sales: {best_product} ({sales.groupby('Product')['Sales'].sum().loc[best_product]:,.2f})\nMost sales by payment method: {best_payment} ({payment.iloc[0]:,.2f})\n\nBusiness suggestions:\n- Review inventory and promotion strategy for high-revenue categories and products.\n- Investigate regional differences and consider targeted campaigns in weaker regions.\n- Use monthly sales patterns to plan stock and staffing; this dataset is descriptive, not a forecast.\n- Compare payment-method usage when planning checkout options.\n\nNote: Dataset is synthetic and generated for practice. These findings describe this sample only.\n'''
(OUT/'sales_analysis_report.txt').write_text(report,encoding='utf-8')
print('\n--- SAMPLE-BASED FINDINGS ---')
print(report)
print('Done. Tables, charts, cleaned data and report are in outputs/.')
