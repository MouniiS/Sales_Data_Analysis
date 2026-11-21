import csv, random, datetime
random.seed(42)
products={
 'Electronics':[('Headphones',45),('Keyboard',35),('Mouse',20),('Monitor',180),('USB Cable',12)],
 'Clothing':[('T-Shirt',18),('Jeans',55),('Jacket',90),('Sneakers',75),('Cap',15)],
 'Home & Kitchen':[('Coffee Mug',10),('Blender',60),('Cookware Set',120),('Lamp',35),('Storage Box',25)],
 'Books':[('Novel',14),('Notebook',8),('Cookbook',22),('Biography',18),('Planner',16)],
 'Sports':[('Yoga Mat',30),('Dumbbells',50),('Water Bottle',15),('Football',25),('Resistance Bands',20)]}
regions=['North','South','East','West']; payments=['Credit Card','Debit Card','UPI','Cash']
start=datetime.date(2025,1,1)
with open('data/sales_data.csv','w',newline='',encoding='utf-8') as f:
 w=csv.writer(f); w.writerow(['Order_ID','Date','Region','Category','Product','Quantity','Unit_Price','Discount','Sales','Payment_Method'])
 for i in range(1,501):
  date=start+datetime.timedelta(days=random.randrange(365)); category=random.choice(list(products)); product,price=random.choice(products[category]); qty=random.randint(1,5); discount=random.choice([0,0,0.05,0.10,0.15]); unit=round(price*(1+random.uniform(-.08,.08)),2); sales=round(unit*qty*(1-discount),2)
  w.writerow([f'S{i:04d}',date.isoformat(),random.choice(regions),category,product,qty,unit,discount,sales,random.choice(payments)])
