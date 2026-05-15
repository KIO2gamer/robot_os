# main.py
"""
Main Entry Point for Robot OS.
Bootstraps the application with all subsystems and starts the UI.
"""

import argparse
from time import sleep

from config import logger, OperatingMode
from locomotion import RobotChassis
from db_manager import VendingDB
from vision_core import VisionCore
from app_controller import AppController
from ui_engine import UIEngine


def parse_arguments():
    """Parse command-line arguments for Raspberry Pi OS deployment."""
    parser = argparse.ArgumentParser(description="Robot OS")
    parser.add_argument(
        "--vision",
        action="store_true",
        help="Enable the vision subsystem",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the demo scenario before starting",
    )
    parser.add_argument(
        "--no-interactive",
        action="store_true",
        help="Run without the interactive CLI",
    )
    parser.add_argument(
        "--mode",
        choices=["manual", "autonomous", "demo"],
        default="manual",
        help="Set the operating mode",
    )
    return parser.parse_args()


def initialize_subsystems(enable_vision=False):
    """
    Initialize all robot subsystems.
    
    Args:
        enable_vision: Whether to enable the vision system
    
    Returns:
        Tuple of (motion_service, inventory_service, vision_service)
    """
    logger.info("Initializing Robot OS subsystems...")
    
    try:
        # Initialize hardware services
        motion_service = RobotChassis()
        logger.info("✓ Motion service initialized")
        
        # Initialize database service
        inventory_service = VendingDB()
        logger.info("✓ Inventory service initialized")
        
        # Initialize vision service (optional)
        vision_service = None
        if enable_vision:
            vision_service = VisionCore(enable_camera=False)  # False for simulation mode
            logger.info("✓ Vision service initialized")
        
        logger.info("All subsystems initialized successfully")
        return motion_service, inventory_service, vision_service
    
    except Exception as e:
        logger.error(f"Error initializing subsystems: {e}")
        raise


def demo_scenario(controller):
    """
    Run a demo scenario to test the system.
    
    Args:
        controller: AppController instance
    """
    logger.info("Starting demo scenario...")
    print("\n" + "="*60)
    print("ROBOT OS DEMO SCENARIO")
    print("="*60)
    
    try:
        # Demo 1: Stock some items
        print("\n[DEMO] Stocking inventory...")
        controller.stock_item("Water Bottle", 2.99, 10)
        controller.stock_item("Snack Bar", 1.50, 5)
        controller.stock_item("Coffee", 3.50, 8)
        
        # Demo 2: Display inventory
        print("\n[DEMO] Current inventory:")
        controller.get_inventory()  # This will log via controller
        
        # Demo 3: Motion test
        print("\n[DEMO] Testing motion controls...")
        controller.move_forward(speed=0.6)
        sleep(2)
        
        # Demo 4: Dispense an item
        print("\n[DEMO] Dispensing an item...")
        success, message = controller.dispense_item("Water Bottle")
        if success:
            print(f"✓ {message}: Water Bottle")
        else:
            print(f"✗ Error: {message}")
        
        # Demo 5: Emergency stop
        print("\n[DEMO] Testing emergency stop...")
        controller.emergency_stop()
        
        print("\n" + "="*60)
        print("Demo scenario completed!")
        print("="*60 + "\n")
    
    except Exception as e:
        logger.error(f"Error during demo scenario: {e}")
        controller.emergency_stop()


def main(enable_vision=False, run_demo=False, interactive=True, mode="manual"):
    """
    Main entry point for Robot OS.
    
    Args:
        enable_vision: Whether to enable the vision system
        run_demo: Whether to run a demo scenario before interactive mode
        interactive: Whether to start interactive CLI session
        mode: Initial operating mode
    """
    logger.info("="*60)
    logger.info("Robot OS Starting")
    logger.info("="*60)
    
    # Initialize subsystems
    motion_service, inventory_service, vision_service = initialize_subsystems(
        enable_vision=enable_vision
    )
    
    # Create the application controller
    controller = AppController(motion_service, inventory_service, vision_service)
    controller.set_mode(mode)
    
    try:
        # Run demo if requested
        if run_demo:
            demo_scenario(controller)
        
        # Start interactive session if requested
        if interactive:
            ui = UIEngine(controller)
            ui.run_interactive_session()
        else:
            # Just keep the system running
            controller.start()
            logger.info("Robot OS running (non-interactive mode)")
            logger.info("Press Ctrl+C to stop")
            
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                logger.info("Stopping Robot OS...")
    
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        controller.emergency_stop()
    
    finally:
        controller.stop()
        logger.info("Robot OS shutdown")


if __name__ == "__main__":
    args = parse_arguments()
    
    main(
        enable_vision=args.vision,
        run_demo=args.demo,
        interactive=not args.no_interactive,
        mode=args.mode,
    )