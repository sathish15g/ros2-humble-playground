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

### Package creation
 ```
 ros2 pkg create temperature_publisher \
  --build-type ament_python \
  --dependencies rclpy sensor_msgs

 ```

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

**Screenshot:**

![Publisher Logs](../images/publisher%20logs.png)

---

## Verification & Testing

### 1. List Available Topics

```bash
ros2 topic list
```

**Screenshot:**

![Topic List](../images/Topic%20list.png)

### 2. Check Topic Information

```bash
ros2 topic info /my_temperature_topic
```

### 3. Echo Published Data

```bash
ros2 topic echo /my_temperature_topic
```

![Topic Echo](../images/topic%20echo.png)

---

## Design Choices

### Topic Name: `/my_temperature_topic`

| Aspect | Rationale |
|--------|-----------|
| **Naming** | Descriptive and sensor-specific |
| **Integration** | Easy to integrate with subscribers |

### Flow-Diagram using rqt_graph
```bash
sudo apt install ros-humble-rqt-graph
rqt_graph
```

![Topic Echo](../images/rosgraph-temp-publisher.png)


### Publishing Rate: 2 seconds

| Aspect | Rationale |
|--------|-----------|
| **Frequency** | Simulates real environmental sensor behavior |
| **Responsiveness** | Adequate for temperature monitoring applications |

### QoS Profile
QoS depth = 10
Suitable for sensor data

---

## Conclusion

This project demonstrates how to publish standardized temperature sensor data in ROS 2 using Python. It provides a strong foundation for working with:

- Real temperature sensors and telemetry
- Multi-node ROS systems
- Sensor data integration in robotics applications
- Message publishing patterns in ROS 2

The architecture can be extended with subscriber nodes.

---

## 👤 Author

**Sathish Kumar G**  
Robotics & ROS 2  

🔗 LinkedIn: https://www.linkedin.com/in/sathish15g/

## 📄 License

This project is licensed under the **Apache License 2.0**.  

You are free to use, modify, distribute, and sublicense this work under the terms of the license.  
For full license details, see the [LICENSE](../../LICENSE) file in this repository.

---