"""
Kikapu Naturals - Synthetic Dataset Generator
Script for generating investor-ready CPG business data
"""

import pandas as pd # type: ignore
import numpy as np # type: ignore
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple, Any
import os

# ============================================================================
# DATA GENERATION CLASS
class KikapuDataGenerator:
    """Generate synthetic datasets for Kikapu Naturals CPG business"""
    
    def __init__(self):
        self.products = None
        self.customers = None
        self.orders = None
        self.order_line_items = None
        
    def weighted_random(self, weights: List[int]) -> int:
        """Select index based on weighted probabilities"""
        total = sum(weights)
        rand = random.random() * total
        for i, weight in enumerate(weights):
            if rand < weight:
                return i
            rand -= weight
        return len(weights) - 1
    
    def random_date(self, start_date: datetime, end_date: datetime) -> datetime:
        """Generate random date between start and end"""
        delta = end_date - start_date
        random_days = random.random() * delta.days
        return start_date + timedelta(days=random_days)
    
    def generate_products(self) -> pd.DataFrame:
        """Generate product catalog (10 CPG products)"""
        print("Generating products...")
        
        products_data = [
            {'product_id': 'P001', 'category': 'Beverage', 'name': 'Organic Green Tea', 
             'unit_price': 18.99, 'avg_cogs': 8.50, 'active_since': '2021-03-01'},
            {'product_id': 'P002', 'category': 'Beverage', 'name': 'Herbal Wellness Blend', 
             'unit_price': 22.99, 'avg_cogs': 10.20, 'active_since': '2021-06-15'},
            {'product_id': 'P003', 'category': 'Snack', 'name': 'Superfood Energy Bars', 
             'unit_price': 24.99, 'avg_cogs': 12.00, 'active_since': '2021-01-10'},
            {'product_id': 'P004', 'category': 'Snack', 'name': 'Organic Trail Mix', 
             'unit_price': 15.99, 'avg_cogs': 7.80, 'active_since': '2021-08-01'},
            {'product_id': 'P005', 'category': 'Supplement', 'name': 'Vitamin D3 Gummies', 
             'unit_price': 29.99, 'avg_cogs': 14.50, 'active_since': '2022-01-01'},
            {'product_id': 'P006', 'category': 'Supplement', 'name': 'Probiotic Blend', 
             'unit_price': 34.99, 'avg_cogs': 16.80, 'active_since': '2022-03-15'},
            {'product_id': 'P007', 'category': 'Personal Care', 'name': 'Natural Face Serum', 
             'unit_price': 39.99, 'avg_cogs': 18.00, 'active_since': '2022-06-01'},
            {'product_id': 'P008', 'category': 'Personal Care', 'name': 'Organic Body Lotion', 
             'unit_price': 26.99, 'avg_cogs': 12.50, 'active_since': '2022-08-10'},
            {'product_id': 'P009', 'category': 'Beverage', 'name': 'Detox Tea Collection', 
             'unit_price': 32.99, 'avg_cogs': 15.00, 'active_since': '2023-01-05'},
            {'product_id': 'P010', 'category': 'Snack', 'name': 'Keto-Friendly Crackers', 
             'unit_price': 19.99, 'avg_cogs': 9.50, 'active_since': '2023-04-20'}
        ]
        
        self.products = pd.DataFrame(products_data)
        return self.products
    
    def generate_customers(self, num_d2c: int = 50000, num_b2b: int = 200) -> pd.DataFrame:
        """Generate customer data with realistic attributes and data quality issues"""
        print(f"Generating {num_d2c} D2C customers...")
        
        customers_data = []
        channels = ['Paid Ads', 'Organic Social', 'Email', 'Referral', 'SEO', 'Sales']
        countries = ['US', 'UK', 'CA', 'AU', 'DE'] # USA, UK, Canada, Australia, Germany
        statuses = ['Active', 'Churned', 'At Risk']
        
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2024, 11, 30)
        
        # Generate D2C customers
        for i in range(1, num_d2c + 1):
            if i % 10000 == 0:
                print(f"  Generated {i}/{num_d2c} D2C customers...")
            
            acq_date = self.random_date(start_date, end_date)
            days_since_acq = (end_date - acq_date).days
            
            # Realistic churn based on cohort age
            if days_since_acq < 90:
                status = statuses[self.weighted_random([80, 15, 5])]
            elif days_since_acq < 365:
                status = statuses[self.weighted_random([60, 30, 10])]
            else:
                status = statuses[self.weighted_random([40, 50, 10])]
            
            customer = {
                'customer_id': f"C{i:06d}",
                'segment': 'D2C',
                'acquisition_date': acq_date.strftime('%Y-%m-%d'),
                'channel': channels[self.weighted_random([30, 25, 15, 12, 15, 3])],
                'country': countries[self.weighted_random([50, 20, 15, 10, 5])],
                'status': status,
                'company_name': None,
                'account_tier': None
            }
            
            # Introduce data quality issues
            if random.random() < 0.02:  # 2% missing acquisition dates
                customer['acquisition_date'] = None
            if random.random() < 0.01:  # 1% missing channels
                customer['channel'] = None
            
            customers_data.append(customer)
        
        # Generate B2B customers
        print(f"Generating {num_b2b} B2B customers...")
        for i in range(1, num_b2b + 1):
            acq_date = self.random_date(datetime(2021, 6, 1), end_date)
            
            customer = {
                'customer_id': f"B{i:05d}",
                'segment': 'B2B',
                'acquisition_date': acq_date.strftime('%Y-%m-%d'),
                'channel': 'Sales',
                'country': countries[self.weighted_random([40, 30, 15, 10, 5])],
                'status': 'Active',
                'company_name': f"Business Customer {i}",
                'account_tier': ['Enterprise', 'Mid-Market', 'SMB'][self.weighted_random([20, 50, 30])]
            }
            
            customers_data.append(customer)
        
        self.customers = pd.DataFrame(customers_data)
        print(f"Total customers generated: {len(self.customers)}")
        return self.customers
    
    def generate_orders(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Generate orders and line items with realistic transaction patterns"""
        print("Generating orders and line items...")
        
        if self.customers is None or self.products is None:
            raise ValueError("Must generate customers and products first")
        
        orders_data = []
        line_items_data = []
        order_id = 1
        
        end_date = datetime(2024, 11, 30)
        
        for i, (idx, customer) in enumerate(self.customers.iterrows()):
            if i % 5000 == 0:
                print(f"  Processing customer {i}/{len(self.customers)}...")
            
            is_b2b = customer['segment'] == 'B2B'
            
            # Parse acquisition date
            if pd.isna(customer['acquisition_date']):
                acq_date = datetime(2023, 1, 1)
            else:
                acq_date = datetime.strptime(customer['acquisition_date'], '%Y-%m-%d')
            
            # Determine number of orders based on segment and status
            if is_b2b:
                num_orders = random.randint(12, 36)  # B2B: 12-36 orders
            else:
                if customer['status'] == 'Active':
                    num_orders = random.randint(2, 10)  # 2-10 orders
                elif customer['status'] == 'Churned':
                    num_orders = random.randint(1, 3)   # 1-3 orders
                else:
                    num_orders = random.randint(2, 7)   # 2-7 orders
            
            # Generate orders over time
            for _ in range(num_orders):
                days_since_acq = (end_date - acq_date).days
                order_date = self.random_date(acq_date, 
                                             acq_date + timedelta(days=min(days_since_acq, 730)))
                
                # Products per order
                num_products = random.randint(3, 8) if is_b2b else random.randint(1, 3)
                
                # Select random products
                selected_products = []
                for _ in range(num_products):
                    product = self.products.iloc[random.randint(0, len(self.products) - 1)]
                    quantity = random.randint(10, 60) if is_b2b else random.randint(1, 3)
                    selected_products.append({'product': product, 'quantity': quantity})
                
                # Calculate order totals
                subtotal = sum(item['product']['unit_price'] * item['quantity'] 
                             for item in selected_products)
                
                # Discount logic
                if is_b2b:
                    discount_percent = [0, 5, 10, 15, 20][self.weighted_random([20, 30, 30, 15, 5])]
                else:
                    discount_percent = [0, 10, 15][self.weighted_random([70, 25, 5])]
                
                discount_amount = subtotal * (discount_percent / 100)
                revenue = subtotal - discount_amount
                total_cogs = sum(item['product']['avg_cogs'] * item['quantity'] 
                               for item in selected_products)
                profit = revenue - total_cogs
                
                # Create order record
                order = {
                    'order_id': f"ORD{order_id:07d}",
                    'customer_id': customer['customer_id'],
                    'order_date': order_date.strftime('%Y-%m-%d'),
                    'subtotal': round(subtotal, 2),
                    'discount_percent': discount_percent,
                    'discount_amount': round(discount_amount, 2),
                    'revenue': round(revenue, 2),
                    'total_cogs': round(total_cogs, 2),
                    'profit': round(profit, 2),
                    'num_items': len(selected_products)
                }
                
                # Data quality issues
                if random.random() < 0.005:  # 0.5% missing order dates
                    order['order_date'] = None
                if random.random() < 0.03:   # 3% missing COGS
                    order['total_cogs'] = None
                    order['profit'] = None
                
                orders_data.append(order)
                
                # Create line items
                for item_idx, item in enumerate(selected_products, 1):
                    item_subtotal = item['product']['unit_price'] * item['quantity']
                    item_discount = (item_subtotal / subtotal) * discount_amount
                    item_revenue = item_subtotal - item_discount
                    item_cogs = item['product']['avg_cogs'] * item['quantity']
                    item_profit = item_revenue - item_cogs
                    
                    line_item = {
                        'line_item_id': f"LI{order_id:07d}_{item_idx}",
                        'order_id': order['order_id'],
                        'customer_id': customer['customer_id'],
                        'product_id': item['product']['product_id'],
                        'product_name': item['product']['name'],
                        'category': item['product']['category'],
                        'quantity': item['quantity'],
                        'unit_price': item['product']['unit_price'],
                        'subtotal': round(item_subtotal, 2),
                        'discount_amount': round(item_discount, 2),
                        'revenue': round(item_revenue, 2),
                        'cogs': round(item_cogs, 2),
                        'profit': round(item_profit, 2),
                        'order_date': order['order_date']
                    }
                    
                    line_items_data.append(line_item)
                
                order_id += 1
        
        self.orders = pd.DataFrame(orders_data)
        self.order_line_items = pd.DataFrame(line_items_data)
        
        print(f"Total orders generated: {len(self.orders)}")
        print(f"Total line items generated: {len(self.order_line_items)}")
        
        return self.orders, self.order_line_items
    
    def generate_all(self) -> Dict[str, Any]:
        """Generate complete dataset"""
        print("\n" + "="*60)
        print("Kikapu Naturals - Dataset Generation")
        print("="*60 + "\n")
        
        self.generate_products()
        self.generate_customers()
        self.generate_orders()
        
        # Calculate statistics
        total_customers = len(self.customers) if self.customers is not None else 0
        d2c_customers = len(self.customers[self.customers['segment'] == 'D2C']) if self.customers is not None else 0
        b2b_customers = len(self.customers[self.customers['segment'] == 'B2B']) if self.customers is not None else 0
        total_orders = len(self.orders) if self.orders is not None else 0
        total_line_items = len(self.order_line_items) if self.order_line_items is not None else 0
        total_revenue = self.orders['revenue'].sum() if self.orders is not None else 0.0

        stats = {
            'total_customers': total_customers,
            'd2c_customers': d2c_customers,
            'b2b_customers': b2b_customers,
            'total_orders': total_orders,
            'total_line_items': total_line_items,
            'total_revenue': total_revenue,
            'date_range': {
                'start': '2022-01-01',
                'end': '2024-11-30'
            }
        }

        print("\n" + "="*60)
        print("Generation Complete - Dataset Statistics")
        print("="*60)
        print(f"Total Customers:     {stats['total_customers']:,}")
        print(f"  - D2C Customers:   {stats['d2c_customers']:,}")
        print(f"  - B2B Clients:     {stats['b2b_customers']:,}")
        print(f"Total Orders:        {stats['total_orders']:,}")
        print(f"Total Line Items:    {stats['total_line_items']:,}")
        print(f"Total Revenue:       ${stats['total_revenue']:,.2f}")
        print(f"Date Range:          {stats['date_range']['start']} to {stats['date_range']['end']}")
        print("="*60 + "\n")

        return {
            'products': self.products,
            'customers': self.customers,
            'orders': self.orders,
            'order_line_items': self.order_line_items,
            'stats': stats
        }
    
    def save_to_csv(self, output_dir: str = './kikapu_data'):
        """Save all datasets to CSV files"""
        # Ensure datasets are generated before attempting to save
        if self.products is None or self.customers is None or self.orders is None or self.order_line_items is None:
            print("One or more datasets are missing; generating all datasets now...")
            # This will populate products, customers, orders, and order_line_items
            self.generate_all()

        # Make sure static type checkers know these are not None at this point
        assert self.products is not None and self.customers is not None and self.orders is not None and self.order_line_items is not None, "Datasets must be generated before saving"

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        print(f"\nSaving datasets to {output_dir}/...")
        
        self.products.to_csv(f"{output_dir}/kikapu_products.csv", index=False)
        print(f"  ✓ Saved kikapu_products.csv")
        
        self.customers.to_csv(f"{output_dir}/kikapu_customers.csv", index=False)
        print(f"  ✓ Saved kikapu_customers.csv")
        
        self.orders.to_csv(f"{output_dir}/kikapu_orders.csv", index=False)
        print(f"  ✓ Saved kikapu_orders.csv")

        self.order_line_items.to_csv(f"{output_dir}/kikapu_order_line_items.csv", index=False)
        print(f"  ✓ Saved kikapu_order_line_items.csv")

        print(f"\nAll files saved to {output_dir}/")
    
    def get_data_quality_report(self) -> str:
        """Generate data quality report"""
        if self.customers is None or self.orders is None:
            return "No data generated yet"
        
        report = "\n" + "="*60 + "\n"
        report += "Data Quality Report\n"
        report += "="*60 + "\n\n"
        
        # Customer data quality
        missing_acq_dates = self.customers['acquisition_date'].isna().sum()
        missing_channels = self.customers['channel'].isna().sum()
        
        report += "CUSTOMERS:\n"
        report += f"  • Missing acquisition dates: {missing_acq_dates} "
        report += f"({missing_acq_dates/len(self.customers)*100:.2f}%)\n"
        report += f"  • Missing channels: {missing_channels} "
        report += f"({missing_channels/len(self.customers)*100:.2f}%)\n\n"
        
        # Order data quality
        missing_order_dates = self.orders['order_date'].isna().sum()
        missing_cogs = self.orders['total_cogs'].isna().sum()
        
        report += "ORDERS:\n"
        report += f"  • Missing order dates: {missing_order_dates} "
        report += f"({missing_order_dates/len(self.orders)*100:.2f}%)\n"
        report += f"  • Missing COGS: {missing_cogs} "
        report += f"({missing_cogs/len(self.orders)*100:.2f}%)\n\n"
        
        report += "NOTE: These data quality issues are intentional and reflect\n"
        report += "real-world fragmented data scenarios.\n"
        report += "="*60 + "\n"
        
        return report


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

if __name__ == "__main__":
    # Setting random seed for reproducibility
    random.seed(42)
    
    # Initialize generator
    generator = KikapuDataGenerator()
    
    # Generate all datasets
    datasets = generator.generate_all()
    
    # Save to CSV files
    generator.save_to_csv(output_dir='./kikapu_data')
    
    # Print data quality report
    print(generator.get_data_quality_report())
    
    # Optional: Display sample data
    print("\nSample Data Preview:")
    print("\n--- Products ---")
    print(datasets['products'].head())
    
    print("\n--- Customers (first 5) ---")
    print(datasets['customers'].head())
    
    print("\n--- Orders (first 5) ---")
    print(datasets['orders'].head())
    
    print("\n--- Order Line Items (first 5) ---")
    print(datasets['order_line_items'].head())