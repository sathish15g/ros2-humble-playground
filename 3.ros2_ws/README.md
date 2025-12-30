# ROS 2 Python Publisher–Subscriber (Full Learning Context)

This document captures the **complete learning journey** for building and testing a  
ROS 2 Python **Subscriber node** using `LaserScan`.

It covers:
- Core ROS 2 concepts  
- Package creation  
- Common mistakes and errors  
- Correct build–run workflow  
- Testing using ROS 2 CLI  

**Target audience:** Beginners learning ROS 2 (Humble+)

---

## 1. Core Concepts

### 1.1 What is a Node?
A **node** is a single executable process in ROS that performs a specific task.

**Examples:**
- Camera driver  
- Lidar processor  
- Obstacle detector  
- Robot controller  

---

### 1.2 Publisher
A **publisher** sends messages on a topic.

**Examples:**
- A camera node publishing images  
- A lidar node publishing `LaserScan` data  

---

### 1.3 Subscriber
A **subscriber** listens to a topic and reacts when data arrives.

**Example:**
- Obstacle detector subscribing to `/laser_scan`

---

### 1.4 Topic
A **topic** is a named channel used for communication.

**Example:**  
`/laser_scan`

---

### 1.5 Message
A **message** defines the structure of data exchanged between nodes.

**Example:**  
`sensor_msgs/msg/LaserScan`

---

## 2. Why ROS 2 Package is Mandatory

ROS 2 **does NOT run standalone Python files**.

To execute your code, use:

```
ros2 run <package> <executable>
```

Your code must therefore reside inside a ROS 2 package containing:

- `package.xml`
- `setup.py`
- Proper folder structure

---

## 3. Creating the ROS 2 Python Package

### Command Used

```
ros2 pkg create example_program --build-type ament_python --dependencies rclpy sensor_msgs
```

### What This Command Does

| Part                  | Meaning                                      |
|-----------------------|----------------------------------------------|
| `ros2 pkg create`     | Create a ROS 2 package                       |
| `example_program`     | Package name                                 |
| `ament_python`        | Python-based package configuration           |
| `rclpy`               | ROS 2 Python client library                  |
| `sensor_msgs`         | Provides message types like `LaserScan`, `Image` |

---

## 4. Workspace Structure

```
ros2_ws/
├── src/
│   └── example_program/
│       ├── example_program/
│       │   ├── __init__.py
│       │   └── obstacle_detector.py
│       ├── package.xml
│       ├── setup.py
│       ├── setup.cfg
│       └── resource/
│           └── example_program
├── build/
├── install/
└── log/
```


---

## 5. Subscriber Node Code

**File:** `obstacle_detector.py`

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan

class ObstacleDetector(Node):
    def __init__(self):
        super().__init__('obstacle_detector')
        self.subscription = self.create_subscription(
            LaserScan,
            'laser_scan',
            self.laser_callback,
            10
        )

    def laser_callback(self, msg):
        self.get_logger().info("Laser data received")

def main():
    rclpy.init()
    node = ObstacleDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```


---

## 6. Registering the Executable

**File:** `setup.py`

```python
entry_points={
    'console_scripts': [
        'obstacle_detector = example_program.obstacle_detector:main',
    ],
},
```

This allows the node to be launched using:

```
ros2 run example_program obstacle_detector
```


---

## 7. Build Process (Correct Way)

### ❌ Common Mistake

```
./setup.py
```

**Reason:** `setup.py` is **not** a shell script and shouldn't be executed directly.

### ✅ Correct Workflow

```
cd ~/ros2_ws
colcon build
source install/setup.bash
```


---

## 8. Running the Node

Run the node using:

```
ros2 run example_program obstacle_detector
```

**Expected behavior:**
- Node starts successfully
- Waits for `/laser_scan` messages  

---

## 9. Testing Without Real Hardware (Using CLI)

### 9.1 Open a New Terminal

```
source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash
```

### 9.2 Publish Fake LaserScan Data

```
ros2 topic pub -r 5 /laser_scan sensor_msgs/msg/LaserScan "{}"
```

### 9.3 Expected Output

In the subscriber terminal:

```
[INFO] [obstacle_detector]: Laser data received
```

---

## 10. Debugging Tools

### List All Topics

```
ros2 topic list
```

### Get Information About a Topic

```
ros2 topic info /laser_scan
```

### Echo Messages From a Topic

```
ros2 topic echo /laser_scan
```
