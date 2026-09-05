"""
Personal Expense Tracker with Visualization
Track your daily expenses and visualize spending patterns
Author: [Your Name]
Date: 2026
"""

import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from collections import defaultdict
import json

class ExpenseTracker:
    def __init__(self):
        self.filename = "expenses.csv"
        self.categories = [
            "Food & Dining", 
            "Transportation", 
            "Shopping", 
            "Entertainment",
            "Bills & Utilities", 
            "Healthcare", 
            "Education", 
            "Savings",
            "Rent", 
            "Other"
        ]
        self.expenses = []
        self.load_expenses()
    
    def load_expenses(self):
        """Load expenses from CSV file"""
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as file:
                    reader = csv.DictReader(file)
                    self.expenses = list(reader)
                print(f"📂 Loaded {len(self.expenses)} expenses")
            else:
                print("📝 No previous data found. Creating new file...")
                self.create_csv_file()
        except Exception as e:
            print(f"⚠️ Error loading data: {e}")
            self.expenses = []
    
    def create_csv_file(self):
        """Create CSV file with headers"""
        try:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Date', 'Category', 'Amount', 'Description', 'Payment_Method'])
            print("✅ New expense file created!")
        except Exception as e:
            print(f"❌ Error creating file: {e}")
    
    def save_expenses(self):
        """Save expenses to CSV file"""
        try:
            with open(self.filename, 'w', newline='') as file:
                fieldnames = ['Date', 'Category', 'Amount', 'Description', 'Payment_Method']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.expenses)
            return True
        except Exception as e:
            print(f"❌ Error saving expenses: {e}")
            return False
    
    def add_expense(self):
        """Add a new expense"""
        print("\n💰 ADD NEW EXPENSE")
        print("-" * 40)
        
        # Get date
        date = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format! Using today's date.")
                date = datetime.now().strftime("%Y-%m-%d")
        
        # Get category
        print("\n📂 Select Category:")
        for i, category in enumerate(self.categories, 1):
            print(f"  {i}. {category}")
        print(f"  {len(self.categories)+1}. Add Custom Category")
        
        while True:
            try:
                choice = int(input("\nEnter category number: "))
                if 1 <= choice <= len(self.categories):
                    category = self.categories[choice - 1]
                    break
                elif choice == len(self.categories) + 1:
                    category = input("Enter custom category: ").strip().title()
                    if category:
                        self.categories.append(category)
                        break
                    else:
                        print("❌ Category cannot be empty!")
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        # Get amount
        while True:
            try:
                amount = float(input("Enter amount (₹): "))
                if amount > 0:
                    break
                else:
                    print("❌ Amount must be greater than 0!")
            except ValueError:
                print("❌ Please enter a valid amount!")
        
        # Get description
        description = input("Enter description: ").strip()
        if not description:
            description = "No description"
        
        # Get payment method
        payment_methods = ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking", "Other"]
        print("\n💳 Payment Method:")
        for i, method in enumerate(payment_methods, 1):
            print(f"  {i}. {method}")
        
        while True:
            try:
                choice = int(input("Enter payment method number: "))
                if 1 <= choice <= len(payment_methods):
                    payment_method = payment_methods[choice - 1]
                    break
                else:
                    print("❌ Invalid choice!")
            except ValueError:
                print("❌ Please enter a valid number!")
        
        # Add expense
        expense = {
            'Date': date,
            'Category': category,
            'Amount': str(amount),
            'Description': description,
            'Payment_Method': payment_method
        }
        
        self.expenses.append(expense)
        if self.save_expenses():
            print(f"\n✅ Expense added successfully! (₹{amount:.2f})")
    
    def view_expenses(self):
        """View all expenses with filters"""
        if not self.expenses:
            print("📭 No expenses recorded!")
            return
        
        print("\n📋 VIEW EXPENSES")
        print("-" * 40)
        print("1. View All")
        print("2. Filter by Category")
        print("3. Filter by Date Range")
        print("4. Filter by Payment Method")
        print("5. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        filtered_expenses = self.expenses.copy()
        
        if choice == '1':
            pass  # Show all
        elif choice == '2':
            category = self.select_category()
            if category:
                filtered_expenses = [e for e in filtered_expenses if e['Category'] == category]
        elif choice == '3':
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                filtered_expenses = [
                    e for e in filtered_expenses 
                    if start <= datetime.strptime(e['Date'], "%Y-%m-%d") <= end
                ]
            except ValueError:
                print("❌ Invalid date format!")
                return
        elif choice == '4':
            methods = list(set(e['Payment_Method'] for e in self.expenses))
            print("\nAvailable Payment Methods:")
            for i, method in enumerate(methods, 1):
                print(f"  {i}. {method}")
            try:
                choice = int(input("Select payment method: "))
                if 1 <= choice <= len(methods):
                    filtered_expenses = [e for e in filtered_expenses if e['Payment_Method'] == methods[choice-1]]
            except ValueError:
                print("❌ Invalid choice!")
                return
        elif choice == '5':
            return
        else:
            print("❌ Invalid choice!")
            return
        
        if not filtered_expenses:
            print("📭 No expenses found!")
            return
        
        self.display_expenses(filtered_expenses)
    
    def display_expenses(self, expenses):
        """Display expenses in a formatted table"""
        print("\n" + "="*80)
        print(f"{'Date':<12} {'Category':<20} {'Amount':>10} {'Description':<20} {'Payment':<15}")
        print("-"*80)
        
        total = 0
        for expense in sorted(expenses, key=lambda x: x['Date'], reverse=True):
            amount = float(expense['Amount'])
            total += amount
            print(f"{expense['Date']:<12} {expense['Category']:<20} ₹{amount:>9.2f} {expense['Description']:<20} {expense['Payment_Method']:<15}")
        
        print("-"*80)
        print(f"{'Total':<32} ₹{total:>9.2f}")
        print("="*80)
        
        return total
    
    def select_category(self):
        """Helper to select a category"""
        categories = list(set(e['Category'] for e in self.expenses))
        if not categories:
            print("📭 No categories available!")
            return None
        
        print("\n📂 Categories:")
        for i, cat in enumerate(categories, 1):
            count = len([e for e in self.expenses if e['Category'] == cat])
            print(f"  {i}. {cat} ({count} expenses)")
        
        try:
            choice = int(input("Select category: "))
            if 1 <= choice <= len(categories):
                return categories[choice-1]
        except ValueError:
            print("❌ Invalid choice!")
        return None
    
    def monthly_summary(self):
        """Show monthly expense summary"""
        if not self.expenses:
            print("📭 No expenses recorded!")
            return
        
        # Get month and year
        current_date = datetime.now()
        year = input(f"Enter year (default {current_date.year}): ").strip()
        year = int(year) if year else current_date.year
        
        month = input(f"Enter month (1-12, default {current_date.month}): ").strip()
        month = int(month) if month else current_date.month
        
        # Filter expenses for the month
        monthly_expenses = [
            e for e in self.expenses 
            if datetime.strptime(e['Date'], "%Y-%m-%d").year == year 
            and datetime.strptime(e['Date'], "%Y-%m-%d").month == month
        ]
        
        if not monthly_expenses:
            print(f"📭 No expenses for {datetime(year, month, 1).strftime('%B %Y')}")
            return
        
        print(f"\n📊 MONTHLY SUMMARY - {datetime(year, month, 1).strftime('%B %Y')}")
        print("="*50)
        
        # Calculate total
        total = sum(float(e['Amount']) for e in monthly_expenses)
        print(f"💰 Total Expenses: ₹{total:.2f}")
        print(f"📅 Number of Transactions: {len(monthly_expenses)}")
        print(f"📊 Average per Day: ₹{total/30:.2f}")
        
        # Category breakdown
        category_totals = defaultdict(float)
        for expense in monthly_expenses:
            category_totals[expense['Category']] += float(expense['Amount'])
        
        print("\n📂 Category Breakdown:")
        for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100
            bar = '█' * int(percentage / 2)
            print(f"  {category:<20}: ₹{amount:>9.2f} ({percentage:>5.1f}%) {bar}")
        
        return monthly_expenses, category_totals
    
    def visualize_data(self):
        """Generate visual charts for expenses"""
        if len(self.expenses) < 3:
            print("📭 Need at least 3 expenses for visualization!")
            return
        
        monthly_expenses, category_totals = self.monthly_summary()
        if not monthly_expenses:
            return
        
        # Create charts
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('💰 Personal Expense Analysis', fontsize=16, fontweight='bold')
        
        # 1. Category Pie Chart
        if category_totals:
            categories = list(category_totals.keys())
            amounts = list(category_totals.values())
            axes[0, 0].pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
            axes[0, 0].set_title('Expenses by Category')
        
        # 2. Daily Expenses Bar Chart
        daily_totals = defaultdict(float)
        for expense in monthly_expenses:
            daily_totals[expense['Date']] += float(expense['Amount'])
        
        dates = sorted(daily_totals.keys())
        daily_amounts = [daily_totals[date] for date in dates]
        axes[0, 1].bar(dates, daily_amounts, color='skyblue', alpha=0.7)
        axes[0, 1].set_title('Daily Expenses')
        axes[0, 1].set_xlabel('Date')
        axes[0, 1].set_ylabel('Amount (₹)')
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # 3. Payment Methods
        payment_totals = defaultdict(float)
        for expense in monthly_expenses:
            payment_totals[expense['Payment_Method']] += float(expense['Amount'])
        
        if payment_totals:
            methods = list(payment_totals.keys())
            amounts = list(payment_totals.values())
            axes[1, 0].bar(methods, amounts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
            axes[1, 0].set_title('Expenses by Payment Method')
            axes[1, 0].set_ylabel('Amount (₹)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Monthly Trend (if multiple months)
        # Group by month
        month_totals = defaultdict(float)
        for expense in self.expenses:
            date_obj = datetime.strptime(expense['Date'], "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            month_totals[month_key] += float(expense['Amount'])
        
        if len(month_totals) > 1:
            months = sorted(month_totals.keys())
            amounts = [month_totals[month] for month in months]
            axes[1, 1].plot(months, amounts, marker='o', linewidth=2, color='green')
            axes[1, 1].set_title('Monthly Expense Trend')
            axes[1, 1].set_xlabel('Month')
            axes[1, 1].set_ylabel('Amount (₹)')
            axes[1, 1].tick_params(axis='x', rotation=45)
        else:
            # Show top 5 expenses by amount
            top_expenses = sorted(monthly_expenses, key=lambda x: float(x['Amount']), reverse=True)[:5]
            desc = [f"{e['Description'][:15]}..." for e in top_expenses]
            amounts = [float(e['Amount']) for e in top_expenses]
            axes[1, 1].barh(desc, amounts, color='orange')
            axes[1, 1].set_title('Top 5 Expenses')
            axes[1, 1].set_xlabel('Amount (₹)')
        
        plt.tight_layout()
        plt.show()
    
    def delete_expense(self):
        """Delete an expense"""
        if not self.expenses:
            print("📭 No expenses to delete!")
            return
        
        # Show recent expenses
        print("\n🗑️ DELETE EXPENSE")
        print("Recent Expenses:")
        for i, expense in enumerate(self.expenses[-10:], 1):
            print(f"{i}. {expense['Date']} - {expense['Category']} - ₹{float(expense['Amount']):.2f} - {expense['Description']}")
        
        try:
            choice = int(input("\nEnter expense number to delete (0 to cancel): "))
            if choice == 0:
                return
            if 1 <= choice <= len(self.expenses):
                deleted = self.expenses.pop(-10 + choice - 1)
                if self.save_expenses():
                    print(f"✅ Deleted: {deleted['Date']} - {deleted['Category']} - ₹{float(deleted['Amount']):.2f}")
            else:
                print("❌ Invalid choice!")
        except ValueError:
            print("❌ Invalid input!")
    
    def export_report(self):
        """Export expense report to a text file"""
        if not self.expenses:
            print("📭 No data to export!")
            return
        
        filename = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w') as file:
                file.write("="*60 + "\n")
                file.write("EXPENSE TRACKER REPORT\n")
                file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("="*60 + "\n\n")
                
                # Overall statistics
                total = sum(float(e['Amount']) for e in self.expenses)
                file.write(f"💰 Total Expenses: ₹{total:.2f}\n")
                file.write(f"📅 Total Transactions: {len(self.expenses)}\n")
                
                # Category summary
                category_totals = defaultdict(float)
                for expense in self.expenses:
                    category_totals[expense['Category']] += float(expense['Amount'])
                
                file.write("\n📂 Category Summary:\n")
                file.write("-"*40 + "\n")
                for category, amount in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
                    percentage = (amount / total) * 100 if total > 0 else 0
                    file.write(f"  {category:<20}: ₹{amount:>9.2f} ({percentage:>5.1f}%)\n")
                
                # All expenses
                file.write("\n\n📋 All Expenses:\n")
                file.write("="*60 + "\n")
                file.write(f"{'Date':<12} {'Category':<20} {'Amount':>10} {'Description':<20}\n")
                file.write("-"*60 + "\n")
                
                for expense in sorted(self.expenses, key=lambda x: x['Date']):
                    file.write(f"{expense['Date']:<12} {expense['Category']:<20} ₹{float(expense['Amount']):>9.2f} {expense['Description']:<20}\n")
                
                file.write("="*60 + "\n")
            
            print(f"✅ Report exported to '{filename}' successfully!")
        except Exception as e:
            print(f"❌ Error exporting report: {e}")
    
    def set_budget(self):
        """Set and check monthly budget"""
        budget_file = "budget.json"
        try:
            if os.path.exists(budget_file):
                with open(budget_file, 'r') as f:
                    budget_data = json.load(f)
                current_budget = budget_data.get('amount', 0)
                print(f"💰 Current Monthly Budget: ₹{current_budget:.2f}")
            else:
                current_budget = 0
                budget_data = {}
        except:
            current_budget = 0
            budget_data = {}
        
        new_budget = input(f"Enter new monthly budget (₹) (current: ₹{current_budget:.2f}): ").strip()
        if new_budget:
            try:
                budget_amount = float(new_budget)
                if budget_amount > 0:
                    budget_data['amount'] = budget_amount
                    budget_data['updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    with open(budget_file, 'w') as f:
                        json.dump(budget_data, f)
                    print(f"✅ Budget set to ₹{budget_amount:.2f}")
                    
                    # Check current month expenses against budget
                    current_month = datetime.now().strftime("%Y-%m")
                    monthly_total = sum(
                        float(e['Amount']) for e in self.expenses 
                        if e['Date'].startswith(current_month)
                    )
                    
                    if monthly_total > 0:
                        print(f"\n📊 Current month expenses: ₹{monthly_total:.2f}")
                        if monthly_total > budget_amount:
                            print(f"⚠️ You've exceeded your budget by ₹{monthly_total - budget_amount:.2f}!")
                            print(f"📈 You've used {(monthly_total/budget_amount)*100:.1f}% of your budget")
                        else:
                            remaining = budget_amount - monthly_total
                            print(f"✅ You're within budget! ₹{remaining:.2f} remaining")
                            print(f"📈 Used {(monthly_total/budget_amount)*100:.1f}% of budget")
                else:
                    print("❌ Budget must be greater than 0!")
            except ValueError:
                print("❌ Invalid amount!")
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("💰 PERSONAL EXPENSE TRACKER")
        print("="*50)
        print("1. ➕ Add Expense")
        print("2. 👁️ View Expenses")
        print("3. 📊 Monthly Summary")
        print("4. 📈 Visualize Data")
        print("5. 🗑️ Delete Expense")
        print("6. 💰 Set Budget")
        print("7. 💾 Export Report")
        print("8. ❌ Exit")
        print("="*50)
        
        # Show today's total
        today = datetime.now().strftime("%Y-%m-%d")
        today_total = sum(
            float(e['Amount']) for e in self.expenses 
            if e['Date'] == today
        )
        if today_total > 0:
            print(f"📅 Today's Spending: ₹{today_total:.2f}")
    
    def run(self):
        """Main program loop"""
        print("🎯 Welcome to Personal Expense Tracker!")
        print(f"📊 Managing {len(self.expenses)} expenses")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.add_expense()
            elif choice == '2':
                self.view_expenses()
            elif choice == '3':
                self.monthly_summary()
            elif choice == '4':
                try:
                    self.visualize_data()
                except Exception as e:
                    print(f"⚠️ Error generating charts: {e}")
                    print("💡 Make sure matplotlib is installed: pip install matplotlib")
            elif choice == '5':
                self.delete_expense()
            elif choice == '6':
                self.set_budget()
            elif choice == '7':
                self.export_report()
            elif choice == '8':
                print("\n👋 Thank you for using Expense Tracker!")
                print("💾 Data saved automatically.")
                break
            else:
                print("❌ Invalid choice! Please enter 1-8.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()