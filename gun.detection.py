import json
import os
from datetime import datetime

class InventorySystem:
    def __init__(self, filename="inventory_data.json"):
        self.filename = filename
        self.products = {}
        self.sales_log = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.products = data.get("products", {})
                    self.sales_log = data.get("sales_log", [])
            except json.JSONDecodeError:
                print("⚠️ Error reading file. Starting with empty database.")

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump({"products": self.products, "sales_log": self.sales_log}, f, indent=4)

    def add_product(self):
        print("\n--- 📦 ADD NEW PRODUCT ---")
        p_id = input("Enter Product ID: ").strip()
        if p_id in self.products:
            print("⚠️ Product ID already exists!")
            return
        name = input("Enter Product Name: ").strip()
        try:
            qty = int(input("Enter Initial Quantity: "))
            price = float(input("Enter Price Per Unit ($): "))
            self.products[p_id] = {"name": name, "qty": qty, "price": price}
            self.save_data()
            print(f"✅ Successfully added {name}!")
        except ValueError:
            print("❌ Invalid number entered. Process cancelled.")

    def update_stock(self):
        print("\n--- 🔄 UPDATE STOCK QUANTITY ---")
        p_id = input("Enter Product ID: ").strip()
        if p_id not in self.products:
            print("❌ Product not found.")
            return
        try:
            new_qty = int(input(f"Enter units to add/subtract for {self.products[p_id]['name']}: "))
            self.products[p_id]['qty'] += new_qty
            self.save_data()
            print(f"✅ Stock updated. Current inventory: {self.products[p_id]['qty']} units.")
        except ValueError:
            print("❌ Invalid quantity formatting.")

    def view_inventory(self):
        print("\n--- 📋 CURRENT INVENTORY REPORT ---")
        if not self.products:
            print("No items currently tracked.")
            return
        print(f"{'ID':<10}{'Name':<20}{'Stock':<10}{'Price':<10}")
        print("-" * 50)
        for p_id, info in self.products.items():
            print(f"{p_id:<10}{info['name']:<20}{info['qty']:<10}${info['price']:<10.2f}")

    def record_sale(self):
        print("\n--- 🛒 RECORD NEW SALE ---")
        p_id = input("Enter Product ID: ").strip()
        if p_id not in self.products:
            print("❌ Item ID matching your search does not exist.")
            return
        try:
            sell_qty = int(input(f"Enter quantity of {self.products[p_id]['name']} sold: "))
            if sell_qty > self.products[p_id]['qty']:
                print(f"❌ Insufficient stock. Only {self.products[p_id]['qty']} available.")
                return
            self.products[p_id]['qty'] -= sell_qty
            total_earned = sell_qty * self.products[p_id]['price']
            sale_entry = {"date": datetime.now().strftime("%Y-%m-%d %H:%M"), "name": self.products[p_id]['name'], "qty": sell_qty, "total": total_earned}
            self.sales_log.append(sale_entry)
            self.save_data()
            print(f"💸 Sale processed! Total value earned: ${total_earned:.2f}")
        except ValueError:
            print("❌ Numeric input error.")

    def view_sales(self):
        print("\n--- 📈 HISTORICAL SALES REVENUE ---")
        if not self.sales_log:
            print("No sales tracked yet.")
            return
        total_revenue = 0
        for entry in self.sales_log:
            print(f"[{entry['date']}] Sold {entry['qty']}x {entry['name']} - Total: ${entry['total']:.2f}")
            total_revenue += entry['total']
        print("-" * 50)
        print(f"🏆 Total Portfolio Sales Revenue: ${total_revenue:.2f}")

def main():
    manager = InventorySystem()
    while True:
        print("\n=== SYSTEM MENU ===")
        print("1. Add New Product\n2. Update Existing Stock\n3. View Inventory Status\n4. Log Customer Purchase\n5. View Revenue Ledger\n6. Exit Terminal Application")
        choice = input("Select operation (1-6): ").strip()
        if choice == "1": manager.add_product()
        elif choice == "2": manager.update_stock()
        elif choice == "3": manager.view_inventory()
        elif choice == "4": manager.record_sale()
        elif choice == "5": manager.view_sales()
        elif choice == "6": 
            print("👋 System shutting down cleanly. Data saved securely."); break
        else: print("❌ Invalid selection option.")

if __name__ == "__main__":
    main()
