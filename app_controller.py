# app_controller.py
"""
Application Controller - Central orchestrator for Robot OS.
Coordinates interactions between UI, Motion Service, Inventory Service, and Vision Service.
Enforces business rules and manages error handling.
"""

import logging
from config import logger, DEFAULT_MODE, OperatingMode

class AppController:
    """
    Central application controller that coordinates all subsystems.
    Acts as a facade to motion, inventory, and vision services.
    """
    
    def __init__(self, motion_service, inventory_service, vision_service=None):
        """
        Initialize the application controller.
        
        Args:
            motion_service: RobotChassis instance for hardware control
            inventory_service: VendingDB instance for inventory management
            vision_service: Optional VisionCore instance for computer vision
        """
        self.motion = motion_service
        self.inventory = inventory_service
        self.vision = vision_service
        self.mode = DEFAULT_MODE
        self.is_running = False
        
        logger.info(f"AppController initialized in {self.mode} mode")
    
    # ============ OPERATIONAL CONTROL ============
    
    def start(self):
        """Start the robot system."""
        self.is_running = True
        logger.info("Robot system started")
    
    def stop(self):
        """Stop the robot system and perform emergency stop."""
        self.is_running = False
        try:
            self.motion.stop()
            logger.info("Robot system stopped gracefully")
        except Exception as e:
            logger.error(f"Error during stop: {e}")
    
    def set_mode(self, mode):
        """Change operating mode."""
        if mode not in [OperatingMode.MANUAL, OperatingMode.AUTONOMOUS, OperatingMode.DEMO]:
            logger.warning(f"Invalid mode: {mode}")
            return False
        self.mode = mode
        logger.info(f"Operating mode changed to: {mode}")
        return True
    
    # ============ MOTION CONTROL ============
    
    def move_forward(self, speed=0.8, duration=None):
        """
        Move the robot forward.
        
        Args:
            speed: Movement speed (0.0 to 1.0)
            duration: Optional duration in seconds
        """
        try:
            self.motion.move_forward(speed=speed)
            logger.info(f"Moving forward at {speed*100}% speed")
            return True
        except Exception as e:
            logger.error(f"Error moving forward: {e}")
            self.motion.stop()
            return False
    
    def move_backward(self, speed=0.8):
        """Move the robot backward."""
        try:
            self.motion.move_backward(speed=speed)
            logger.info(f"Moving backward at {speed*100}% speed")
            return True
        except Exception as e:
            logger.error(f"Error moving backward: {e}")
            self.motion.stop()
            return False
    
    def turn_left(self, speed=0.6):
        """Turn the robot left."""
        try:
            self.motion.turn_left(speed=speed)
            logger.info(f"Turning left at {speed*100}% speed")
            return True
        except Exception as e:
            logger.error(f"Error turning left: {e}")
            self.motion.stop()
            return False
    
    def turn_right(self, speed=0.6):
        """Turn the robot right."""
        try:
            self.motion.turn_right(speed=speed)
            logger.info(f"Turning right at {speed*100}% speed")
            return True
        except Exception as e:
            logger.error(f"Error turning right: {e}")
            self.motion.stop()
            return False
    
    def emergency_stop(self):
        """Perform an emergency stop."""
        try:
            self.motion.stop()
            logger.warning("Emergency stop triggered")
            return True
        except Exception as e:
            logger.error(f"Error during emergency stop: {e}")
            return False
    
    # ============ INVENTORY MANAGEMENT ============
    
    def get_inventory(self):
        """Get current inventory status."""
        try:
            items = self.inventory.get_inventory()
            logger.debug(f"Inventory retrieved: {len(items)} items")
            return items
        except Exception as e:
            logger.error(f"Error retrieving inventory: {e}")
            return []
    
    def stock_item(self, item_name, price, quantity):
        """Add or update an item in inventory."""
        try:
            self.inventory.add_or_update_item(item_name, price, quantity)
            logger.info(f"Stocked {quantity} units of {item_name} at ${price}")
            return True
        except Exception as e:
            logger.error(f"Error stocking item {item_name}: {e}")
            return False
    
    def dispense_item(self, item_name):
        """
        Dispense an item from inventory.
        Applies business logic before dispensing (checks stock, etc.)
        """
        try:
            # Check if item exists and has stock
            inventory = self.inventory.get_inventory()
            item = next((i for i in inventory if i[0] == item_name), None)
            
            if not item:
                logger.warning(f"Item {item_name} not found in inventory")
                return False, "Item not found"
            
            if item[2] <= 0:
                logger.warning(f"Item {item_name} is out of stock")
                return False, "Out of stock"
            
            # Perform dispensing
            success = self.inventory.dispense_item(item_name)
            if success:
                logger.info(f"Item {item_name} dispensed successfully")
                return True, "Dispensed"
            else:
                return False, "Dispensing failed"
        except Exception as e:
            logger.error(f"Error dispensing item {item_name}: {e}")
            return False, str(e)
    
    # ============ VISION INTEGRATION ============
    
    def detect_object(self):
        """Detect objects using vision system."""
        if not self.vision:
            logger.warning("Vision system not available")
            return None
        
        try:
            detection = self.vision.detect()
            logger.debug(f"Vision detection: {detection}")
            return detection
        except Exception as e:
            logger.error(f"Error in vision detection: {e}")
            return None
    
    def validate_item_selection(self, item_data):
        """Validate item selection using vision."""
        if not self.vision:
            logger.warning("Vision system not available for validation")
            return True  # Skip validation if no vision
        
        try:
            valid = self.vision.validate(item_data)
            logger.debug(f"Item validation result: {valid}")
            return valid
        except Exception as e:
            logger.error(f"Error validating item: {e}")
            return False
    
    # ============ STATUS AND DIAGNOSTICS ============
    
    def get_status(self):
        """Get complete system status."""
        status = {
            "running": self.is_running,
            "mode": self.mode,
            "inventory_count": len(self.get_inventory()),
            "vision_available": self.vision is not None,
        }
        return status
