# Robot OS - Architecture Implementation

## 📋 Overview

This implementation follows the **Target Design Architecture** outlined in `SYSTEM_DESIGN.md`. The codebase has been refactored from a monolithic structure to a layered, service-oriented architecture.

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    UI / Command Layer                        │
│                      (ui_engine.py)                          │
│                   [CLI Interactive Menu]                     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              Application Controller                          │
│                 (app_controller.py)                          │
│        [Orchestration & Business Logic]                      │
└──┬────────────────────┬────────────────────┬────────────────┘
   │                    │                    │
   ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Motion Service│  │Inventory Srv.│  │Vision Service│
│(locomotion)  │  │(db_manager)  │  │(vision_core) │
└──────────────┘  └──────────────┘  └──────────────┘
   │                    │                    │
   ▼                    ▼                    ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Motor Hardware│  │SQLite DB     │  │Camera/Sensors│
└──────────────┘  └──────────────┘  └──────────────┘
```

## 📁 Module Responsibilities

### **config.py** ⚙️

- GPIO pin configuration
- Database settings
- Operating modes definition
- Logging setup
- Motion parameters

### **locomotion.py** 🤖

- `RobotChassis` class
- Motor control API:
  - `move_forward(speed)`
  - `move_backward(speed)`
  - `turn_left(speed)`
  - `turn_right(speed)`
  - `stop()`
- Direct hardware abstraction

### **db_manager.py** 💾

- `VendingDB` class
- Inventory operations:
  - `add_or_update_item()`
  - `dispense_item()`
  - `get_inventory()`
  - `get_item()`
- SQLite persistence layer

### **vision_core.py** 👁️

- `VisionCore` class (currently simulated)
- Detection methods:
  - `detect()` - Object detection
  - `validate()` - Item validation
  - `detect_obstacles()` - Obstacle detection
  - `detect_user()` - User detection
  - `identify_item()` - Item recognition
  - `check_safety()` - Safety validation
- Can be extended with OpenCV/TensorFlow

### **app_controller.py** 🎮

- `AppController` class
- Central orchestrator
- Implements business logic:
  - Motion coordination
  - Inventory management
  - Error handling
  - Mode management
  - System status

### **ui_engine.py** 🖥️

- `UIEngine` class
- Interactive CLI interface
- Menus:
  - Motion Control Menu
  - Inventory Management Menu
  - System Status Display
  - Settings Menu
- Can be extended for touchscreen/web UI

### **main.py** 🚀

- Bootstrap/entry point
- System initialization
- Optional demo scenario
- Interactive session management

## 🚀 Getting Started

### Basic Usage

```python
# Run with interactive menu
python main.py
```

### Configuration Options in main.py

```python
ENABLE_VISION = False   # Enable vision system
RUN_DEMO = True         # Run demo scenario
INTERACTIVE = True      # Start interactive CLI
```

### Demo Scenario

The demo runs automatically (when `RUN_DEMO=True`) and demonstrates:

1. Stocking inventory items
2. Displaying inventory
3. Motion control (move forward)
4. Dispensing items
5. Emergency stop

## 📋 Example Usage

### Interactive Menu Flow

```
1. Motion Control
   ├─ Move Forward
   ├─ Move Backward
   ├─ Turn Left
   ├─ Turn Right
   ├─ Stop
   └─ Emergency Stop

2. Inventory Management
   ├─ View Inventory
   ├─ Stock Item
   └─ Dispense Item

3. System Status
   └─ Show running state, mode, inventory count

4. Settings
   ├─ Change Operating Mode
   └─ Emergency Stop
```

### Programmatic Usage

```python
from app_controller import AppController
from locomotion import RobotChassis
from db_manager import VendingDB

# Initialize services
motion = RobotChassis()
inventory = VendingDB()

# Create controller
controller = AppController(motion, inventory)

# Use the system
controller.move_forward(speed=0.8)
controller.stock_item("Water", 2.99, 10)
items = controller.get_inventory()
success, msg = controller.dispense_item("Water")
```

## 🔒 Error Handling

All layers implement comprehensive error handling:

- Hardware failures trigger automatic motor shutdown
- Database errors are logged and gracefully handled
- Vision system failures don't crash the system
- Application layer coordinates recovery

## 📊 Logging

Logs are generated at multiple levels:

- **Console**: Real-time output during execution
- **File**: `robot_os.log` with rotation (5MB max, 3 backups)
- **Levels**: DEBUG, INFO, WARNING, ERROR
- **Format**: `[timestamp] - [module] - [level] - [message]`

## 🔧 Design Decisions

1. **Service Isolation**: Each service (motion, inventory, vision) is independent
2. **Controller Coordination**: AppController acts as single point of orchestration
3. **Error Recovery**: All layers handle errors gracefully
4. **Extensibility**: UI can be swapped for touchscreen/web interface
5. **Configuration Centralization**: All settings in `config.py`
6. **Unified Logging**: Consistent logging across all modules

## 🔄 Data Flow Examples

### Motion Command Flow

```
User Input → UIEngine → AppController → RobotChassis → Motor Hardware
```

### Inventory Dispense Flow

```
User Input → UIEngine → AppController →
  [Check Inventory: AppController.get_inventory()]
  [Validate Stock: Business Logic]
  → VendingDB.dispense_item() → SQLite
```

## 🚀 Future Extensions

1. **Web UI**: Replace CLI with Flask/FastAPI web interface
2. **Real Vision**: Integrate OpenCV/YOLO for actual object detection
3. **Autonomous Mode**: Implement path planning and autonomous navigation
4. **Multi-User**: Add user authentication and role management
5. **Remote Control**: Add WebSocket/MQTT for remote operation
6. **Analytics**: Track inventory metrics and usage patterns

## ⚠️ Safety Considerations

- Emergency stop is available at any time (Ctrl+C in CLI)
- Motion failures auto-stop motors
- Vision system failures don't affect motion (graceful degradation)
- Inventory checks prevent dispensing out-of-stock items
- All GPIO operations wrapped in try-catch blocks

## 📝 Testing

### Test Motion Service

```bash
python locomotion.py
```

### Test Database Service

```bash
python db_manager.py
```

### Run Full System with Demo

```bash
python main.py  # With RUN_DEMO=True
```

## Raspberry Pi OS Deployment

### Install dependencies

```bash
sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run on the Pi

```bash
source .venv/bin/activate
python main.py --mode manual
```

Useful startup flags:

- `--vision` enables the vision layer in simulation mode.
- `--demo` runs the demo sequence before normal startup.
- `--no-interactive` runs headless for service mode.
- `--mode manual|autonomous|demo` sets the initial operating mode.

### Start at boot with systemd

Use [deploy/robot-os.service](deploy/robot-os.service) as the service template, then copy it to `/etc/systemd/system/robot-os.service` and update the paths if your project lives somewhere else.

```bash
sudo systemctl daemon-reload
sudo systemctl enable robot-os
sudo systemctl start robot-os
sudo systemctl status robot-os
```

### Setup script

If you want a one-shot install helper, use [scripts/setup_raspberry_pi_os.sh](scripts/setup_raspberry_pi_os.sh) on the Pi.
