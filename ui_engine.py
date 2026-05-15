# ui_engine.py
"""
UI Engine - User Interface Layer for Robot OS.
Provides interaction layer for controlling the robot and managing inventory.
Currently implements a CLI interface; can be extended for touchscreen or web UI.
"""

import logging
from config import logger

class UIEngine:
    """
    User interface engine for Robot OS.
    Handles user input and displays system information.
    """
    
    def __init__(self, app_controller):
        """
        Initialize the UI engine.
        
        Args:
            app_controller: AppController instance for coordinating actions
        """
        self.controller = app_controller
        self.logger = logger
    
    # ============ MOTION CONTROL UI ============
    
    def show_motion_menu(self):
        """Display motion control menu."""
        print("\n" + "="*50)
        print("MOTION CONTROL MENU")
        print("="*50)
        print("1. Move Forward")
        print("2. Move Backward")
        print("3. Turn Left")
        print("4. Turn Right")
        print("5. Stop")
        print("6. Emergency Stop")
        print("0. Back to Main Menu")
        print("="*50)
    
    def handle_motion_input(self, choice):
        """Handle motion control input."""
        speed_options = {
            "1": 0.8,
            "2": 0.6,
            "3": 0.4,
        }
        
        if choice == "1":
            self.controller.move_forward(speed=0.8)
        elif choice == "2":
            self.controller.move_backward(speed=0.8)
        elif choice == "3":
            self.controller.turn_left(speed=0.6)
        elif choice == "4":
            self.controller.turn_right(speed=0.6)
        elif choice == "5":
            self.controller.emergency_stop()
        elif choice == "6":
            self.controller.emergency_stop()
            print("EMERGENCY STOP ACTIVATED!")
        else:
            print("Invalid choice")
    
    # ============ INVENTORY UI ============
    
    def show_inventory_menu(self):
        """Display inventory management menu."""
        print("\n" + "="*50)
        print("INVENTORY MANAGEMENT MENU")
        print("="*50)
        print("1. View Inventory")
        print("2. Stock Item")
        print("3. Dispense Item")
        print("0. Back to Main Menu")
        print("="*50)
    
    def display_inventory(self):
        """Display current inventory in a formatted table."""
        items = self.controller.get_inventory()
        
        if not items:
            print("\n[INVENTORY] No items in stock")
            return
        
        print("\n" + "="*60)
        print(f"{'Item Name':<25} {'Price':<10} {'Stock':<10}")
        print("-"*60)
        
        for item_name, price, stock in items:
            print(f"{item_name:<25} ${price:<9.2f} {stock:<10}")
        
        print("="*60)
    
    def handle_inventory_input(self, choice):
        """Handle inventory management input."""
        if choice == "1":
            self.display_inventory()
        elif choice == "2":
            self.stock_item_dialog()
        elif choice == "3":
            self.dispense_item_dialog()
        else:
            print("Invalid choice")
    
    def stock_item_dialog(self):
        """Interactive dialog to stock an item."""
        print("\n[INVENTORY] Stock Item")
        try:
            item_name = input("Enter item name: ").strip()
            if not item_name:
                print("Item name cannot be empty")
                return
            
            price = float(input("Enter price: $"))
            quantity = int(input("Enter quantity: "))
            
            if self.controller.stock_item(item_name, price, quantity):
                print(f"✓ Successfully stocked {quantity} units of {item_name}")
            else:
                print("✗ Failed to stock item")
        except ValueError as e:
            print(f"Invalid input: {e}")
    
    def dispense_item_dialog(self):
        """Interactive dialog to dispense an item."""
        print("\n[INVENTORY] Dispense Item")
        self.display_inventory()
        
        try:
            item_name = input("\nEnter item name to dispense: ").strip()
            if not item_name:
                print("Item name cannot be empty")
                return
            
            success, message = self.controller.dispense_item(item_name)
            if success:
                print(f"✓ {message}: {item_name}")
            else:
                print(f"✗ {message}")
        except Exception as e:
            print(f"Error: {e}")
    
    # ============ STATUS UI ============
    
    def show_status(self):
        """Display system status."""
        status = self.controller.get_status()
        
        print("\n" + "="*50)
        print("SYSTEM STATUS")
        print("="*50)
        print(f"Running: {'Yes' if status['running'] else 'No'}")
        print(f"Mode: {status['mode']}")
        print(f"Inventory Items: {status['inventory_count']}")
        print(f"Vision System: {'Available' if status['vision_available'] else 'Not Available'}")
        print("="*50)
    
    # ============ MAIN MENU ============
    
    def show_main_menu(self):
        """Display main menu."""
        print("\n" + "="*50)
        print("ROBOT OS MAIN MENU")
        print("="*50)
        print("1. Motion Control")
        print("2. Inventory Management")
        print("3. System Status")
        print("4. Settings")
        print("9. Exit")
        print("="*50)
    
    def show_settings_menu(self):
        """Display settings menu."""
        print("\n" + "="*50)
        print("SETTINGS MENU")
        print("="*50)
        print("1. Change Operating Mode")
        print("2. Emergency Stop")
        print("0. Back to Main Menu")
        print("="*50)
    
    def handle_settings_input(self, choice):
        """Handle settings input."""
        if choice == "1":
            print("\nAvailable modes: manual, autonomous, demo")
            mode = input("Enter operating mode: ").strip().lower()
            if self.controller.set_mode(mode):
                print(f"✓ Mode changed to: {mode}")
            else:
                print("✗ Invalid mode")
        elif choice == "2":
            if self.controller.emergency_stop():
                print("✓ Emergency stop activated")
            else:
                print("✗ Emergency stop failed")
    
    # ============ INTERACTIVE SESSION ============
    
    def run_interactive_session(self):
        """Run an interactive CLI session."""
        print("\n" + "="*50)
        print("Welcome to Robot OS Control Interface")
        print("="*50)
        
        self.controller.start()
        
        try:
            while True:
                self.show_main_menu()
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    while True:
                        self.show_motion_menu()
                        motion_choice = input("Enter your choice: ").strip()
                        if motion_choice == "0":
                            break
                        self.handle_motion_input(motion_choice)
                
                elif choice == "2":
                    while True:
                        self.show_inventory_menu()
                        inv_choice = input("Enter your choice: ").strip()
                        if inv_choice == "0":
                            break
                        self.handle_inventory_input(inv_choice)
                
                elif choice == "3":
                    self.show_status()
                
                elif choice == "4":
                    while True:
                        self.show_settings_menu()
                        settings_choice = input("Enter your choice: ").strip()
                        if settings_choice == "0":
                            break
                        self.handle_settings_input(settings_choice)
                
                elif choice == "9":
                    print("\n[SYSTEM] Shutting down Robot OS...")
                    self.controller.stop()
                    print("Goodbye!")
                    break
                
                else:
                    print("Invalid choice. Please try again.")
        
        except KeyboardInterrupt:
            print("\n\n[SYSTEM] Keyboard interrupt detected. Emergency stop!")
            self.controller.emergency_stop()
