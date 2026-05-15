# db_manager.py
"""
Database Manager - Inventory Service for Robot OS.
Handles all SQLite database operations for inventory management.
"""

import sqlite3
from config import logger, DB_CONFIG

class VendingDB:
    """
    Inventory database manager using SQLite.
    Manages product stock, pricing, and dispensing operations.
    """
    
    def __init__(self, db_name=None):
        """
        Initialize the database manager.
        
        Args:
            db_name: Optional custom database filename
        """
        self.db_name = db_name or DB_CONFIG["db_name"]
        self.timeout = DB_CONFIG["timeout"]
        self._setup_database()

    def _setup_database(self):
        """Creates the inventory table if it doesn't exist yet."""
        try:
            conn = sqlite3.connect(self.db_name, timeout=self.timeout)
            cursor = conn.cursor()
            
            # Create a table with ID, Item Name, Price, and Stock Count
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item_name TEXT UNIQUE NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL
                )
            ''')
            conn.commit()
            conn.close()
            
            logger.info(f"✓ Database initialized: {self.db_name}")
            print("Database: Connected and Ready.")
        except Exception as e:
            logger.error(f"Error setting up database: {e}")
            raise

    def add_or_update_item(self, item_name, price, stock):
        """
        Inserts a new item or updates stock if it already exists.
        
        Args:
            item_name: Name of the item
            price: Price of the item
            stock: Quantity in stock
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_name, timeout=self.timeout)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO inventory (item_name, price, stock)
                VALUES (?, ?, ?)
                ON CONFLICT(item_name) 
                DO UPDATE SET stock = ?, price = ?
            ''', (item_name, price, stock, stock, price))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Item {item_name}: {stock} units @ ${price}")
            return True
        except Exception as e:
            logger.error(f"Error adding/updating item {item_name}: {e}")
            return False

    def dispense_item(self, item_name):
        """
        Reduces stock by 1 when an item is dispensed.
        
        Args:
            item_name: Name of the item to dispense
        
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_name, timeout=self.timeout)
            cursor = conn.cursor()
            
            # Check current stock
            cursor.execute(
                'SELECT stock FROM inventory WHERE item_name = ?',
                (item_name,)
            )
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                # Decrease stock by 1
                new_stock = result[0] - 1
                cursor.execute(
                    'UPDATE inventory SET stock = ? WHERE item_name = ?',
                    (new_stock, item_name)
                )
                conn.commit()
                conn.close()
                
                logger.info(f"Dispensed {item_name}. Remaining stock: {new_stock}")
                return True
            else:
                conn.close()
                logger.warning(f"Cannot dispense {item_name}: out of stock or not found")
                return False
        except Exception as e:
            logger.error(f"Error dispensing item {item_name}: {e}")
            return False

    def get_inventory(self):
        """
        Returns the full inventory list.
        
        Returns:
            List of tuples (item_name, price, stock)
        """
        try:
            conn = sqlite3.connect(self.db_name, timeout=self.timeout)
            cursor = conn.cursor()
            cursor.execute('SELECT item_name, price, stock FROM inventory')
            data = cursor.fetchall()
            conn.close()
            
            logger.debug(f"Retrieved {len(data)} inventory items")
            return data
        except Exception as e:
            logger.error(f"Error retrieving inventory: {e}")
            return []

    def get_item(self, item_name):
        """
        Get information about a specific item.
        
        Args:
            item_name: Name of the item
        
        Returns:
            Tuple (item_name, price, stock) or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_name, timeout=self.timeout)
            cursor = conn.cursor()
            cursor.execute(
                'SELECT item_name, price, stock FROM inventory WHERE item_name = ?',
                (item_name,)
            )
            result = cursor.fetchone()
            conn.close()
            
            return result
        except Exception as e:
            logger.error(f"Error retrieving item {item_name}: {e}")
            return None


# --- Quick Test Block ---
if __name__ == "__main__":
    db = VendingDB()
    
    # Stocking the robot
    print("\n[TEST] Stocking items...")
    db.add_or_update_item("Water Bottle", 2.99, 10)
    db.add_or_update_item("Snack Bar", 1.50, 5)
    
    print("\n[TEST] Current Inventory:")
    inventory = db.get_inventory()
    for item_name, price, stock in inventory:
        print(f"  {item_name}: ${price} ({stock} in stock)")
    
    # Simulating a purchase
    print("\n[TEST] Dispensing Water Bottle...")
    success = db.dispense_item("Water Bottle")
    if success:
        print("✓ Water Bottle dispensed!")
    
    print("\n[TEST] Updated Inventory:")
    inventory = db.get_inventory()
    for item_name, price, stock in inventory:
        print(f"  {item_name}: ${price} ({stock} in stock)")