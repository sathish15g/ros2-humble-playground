# ROS 2 Temperature Publisher (sensor_msgs/Temperature)

## Overview

This project demonstrates a **ROS 2 Publisher node** that simulates a temperature sensor and publishes temperature data at a fixed interval using the **standard ROS message type `sensor_msgs/Temperature`**.

The node publishes temperature readings every **2 seconds**, which can be visualized or consumed by other ROS 2 nodes such as robot controllers, monitoring systems, or visualization tools.

---

## Objectives

- Understand and implement a **ROS 2 Publisher** using Python (`rclpy`)
- Publish sensor data using a **standard ROS 2 message type**
- Demonstrate periodic data publishing using `rclpy.Timer`
- Verify topic communication using ROS 2 CLI tools

---

## Software & Tools

| Component | Details |
|-----------|---------|
| **OS** | Ubuntu 22.04 |
| **ROS Distribution** | ROS 2 Humble Hawksbill |
| **Language** | Python |
| **Message Type** | `sensor_msgs/msg/Temperature` |
| **ROS Client Library** | `rclpy` |

---

## Message Type Used

### `sensor_msgs/Temperature`

```
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
float64 temperature   # Temperature in Celsius
float64 variance      # Variance of the measurement (0.0 = unknown)
```

This message type is recommended for temperature sensors in ROS-based systems.

---

## Project Structure

```
ros2-temp-pub-sub
└── temperature_publisher/
    ├── temperature_publisher/
    │   └── temperature_publisher_node.py
    ├── package.xml
    ├── setup.py
    ├── setup.cfg
    ├── resource/
    └── test/
```

---

## Build Instructions

### 1. Source ROS 2 Setup

```bash
source /opt/ros/humble/setup.bash
```
> **Note:** This is already configured in `.bashrc`

### 2. Navigate to Workspace

```bash
cd ~/ros/ros2-humble-playground/ros2-temp-pub-sub
```

### 3. Build the Workspace

```bash
colcon build
```

### 4. Source the Workspace

```bash
source install/setup.bash
```

---

## Running the Publisher Node

### Start the Publisher

```bash
ros2 run temperature_publisher temperature_publisher
```

### Expected Output

```
[INFO] [temperature_publisher]: Published Temperature: 28.7 °C
[INFO] [temperature_publisher]: Published Temperature: 29.2 °C
[INFO] [temperature_publisher]: Published Temperature: 28.9 °C
```

**Screenshot:**

![Publisher Logs](./temperature_publisher/images/publisher%20logs.png)

---

## Verification & Testing

### 1. List Available Topics

```bash
ros2 topic list
```

**Expected Output:**
```
/my_temperature_topic
```

![Topic List](./temperature_publisher/images/Topic%20list.png)

### 2. Check Topic Information

```bash
ros2 topic info /my_temperature_topic
```

**Expected Output:**
```
Type: sensor_msgs/msg/Temperature
Publisher count: 1
Subscriber count: 0
```

### 3. Echo Published Data

```bash
ros2 topic echo /my_temperature_topic
```

**Sample Output:**
```yaml
header:
  stamp:
    sec: 1715178301
    nanosec: 123456789
  frame_id: temperature_sensor_frame
temperature: 28.63
variance: 0.0
---
header:
  stamp:
    sec: 1715178303
    nanosec: 456789123
  frame_id: temperature_sensor_frame
temperature: 29.15
variance: 0.0
---
```

![Topic Echo](./temperature_publisher/images/topic%20echo.png)

---

## Design Choices

### Topic Name: `/my_temperature_topic`

| Aspect | Rationale |
|--------|-----------|
| **Naming** | Descriptive and sensor-specific |
| **Integration** | Easy to integrate with subscribers |

### Publishing Rate: 2 seconds

| Aspect | Rationale |
|--------|-----------|
| **Frequency** | Simulates real environmental sensor behavior |
| **Responsiveness** | Adequate for temperature monitoring applications |

### QoS Profile

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Queue Depth** | 10 | Suitable for periodic sensor data |
| **Reliability** | Best Effort | Prevents message loss if subscribers lag briefly |

---

## Troubleshooting

### Issue: `sensor_msgs not found`

**Solution:**
```bash
sudo apt install ros-humble-sensor-msgs
```

### Issue: Package not detected after build

**Solution:**
```bash
source install/setup.bash
```

### Issue: Topic not appearing in `ros2 topic list`

**Solution:**
1. Verify the node is running:
   ```bash
   ros2 node list
   ```
2. Check the node logs:
   ```bash
   ros2 run temperature_publisher temperature_publisher --verbose
   ```

---

## Debug Tools

Use these ROS 2 tools for debugging and monitoring:

```bash
# Check ROS 2 system health
ros2 doctor

# Get detailed topic information
ros2 topic info /my_temperature_topic

# List all active nodes
ros2 node list

# Get node information
ros2 node info /temperature_publisher
```

---

## Conclusion

This project demonstrates how to publish standardized temperature sensor data in ROS 2 using Python. It provides a strong foundation for working with:

- Real temperature sensors and telemetry
- Multi-node ROS systems
- Sensor data integration in robotics applications
- Message publishing patterns in ROS 2

The architecture can be extended with subscriber nodes, data logging, or integration with monitoring dashboards.
