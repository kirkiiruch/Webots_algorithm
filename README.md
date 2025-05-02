# 🤖 Three-Wheeled Robot Controller in Webots

## 📜 Description

This project implements a controller for a three-wheeled robot in the Webots simulation environment. It includes pathfinding algorithms and turning utilities to enable the robot to navigate within a predefined world (`zad4.wbt`).

## 📁 Project Structure

```
my_project/
├── controllers/
│   └── three_wheeled_robot_controller/
│       ├── path_finder.py              # Pathfinding algorithms
│       ├── turn_utils.py               # Turning utilities
│       ├── three_wheeled_robot_controller.py  # Main robot controller
│       └── .idea/                      # PyCharm project settings
├── worlds/
│   ├── zad4.wbt                        # Webots simulation world
│   └── .zad4.wbproj                    # Webots project file
```

## 🚀 How to Run

1. Open Webots.
2. Load the `zad4.wbt` world from the `my_project/worlds/` directory.
3. Assign the `three_wheeled_robot_controller` controller to the robot in the simulation.
4. Start the simulation.

## ⚙️ Requirements

- [Webots](https://cyberbotics.com/)
- Python 3.10+
- PyCharm (optional, for development)

