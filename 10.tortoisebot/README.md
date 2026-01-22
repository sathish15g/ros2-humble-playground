# 🐢 TortoiseBot – What, Why, How

This README provides a **clear understanding of TortoiseBot**, its purpose, architecture, how to use it with **ROS 2**, and **common issues with fixes** encountered during setup (especially simulation and LiDAR-related problems).

---

## 📌 What is TortoiseBot?

**TortoiseBot** is an **open-source mobile robot platform** designed for:

* Learning **ROS 2** concepts
* Navigation and SLAM experiments
* Simulation using **Gazebo**
* Visualization using **RViz2**

It is widely used in **education, robotics training, and research** as a practical alternative to TurtleBot with more extensibility.

---

## 🎯 Why TortoiseBot?

TortoiseBot is used because:

* ✅ ROS 2–native architecture
* ✅ Supports **Gazebo simulation + real hardware**
* ✅ Modular packages (bringup, navigation, SLAM, control)
* ✅ Affordable hardware (for real robot)
* ✅ Ideal for understanding **TF, sensors, Nav2, SLAM**

It bridges the gap between **theory and real-world robotics**.

---

## 🧱 High-Level Architecture

```
TortoiseBot
│
├── tortoisebot_description   → URDF / robot model
├── tortoisebot_gazebo        → Simulation world & plugins
├── tortoisebot_control       → Controllers & velocity control
├── tortoisebot_slam          → SLAM (mapping)
├── tortoisebot_navigation    → Nav2 stack
├── tortoisebot_bringup       → Launch files (single entry point)
├── tortoisebot_imu           → IMU drivers
├── tortoisebot_firmware      → Hardware interface
└── ydlidar_ros2_driver       → LiDAR driver (external dependency)
```

---

## ⚙️ How TortoiseBot Works (Simulation Flow)

1. **Gazebo** simulates:

   * Robot movement
   * Sensors (LiDAR, IMU)

2. **ROS 2 nodes** publish:

   * `/scan` (LiDAR)
   * `/odom` (odometry)
   * `/tf` (transforms)

3. **SLAM / Navigation** consumes sensor data

4. **RViz2** visualizes:

   * Robot model
   * Laser scans
   * Map and TF tree

---

## 🚀 How to Run TortoiseBot (Simulation)

### Build workspace (recommended during development)

```bash
cd ~/roboai_ws
colcon build --symlink-install
source install/setup.bash
```

### Launch robot

```bash
ros2 launch tortoisebot_bringup autobringup.launch.py \
  use_sim_time:=True exploration:=False
```

---

## 🔗 Understanding `--symlink-install`

### What it does

* Creates **symbolic links** instead of copying files to `install/`
* Runtime directly uses files from `src/`

### Why it is useful

* No rebuild needed after editing:

  * Launch files
  * Python nodes
  * YAML configs
  * URDF / RViz files

**Recommended for development, not required for production builds.**

---

## 🐞 Common Issues & Fixes

### ❌ Issue 1: `package 'ydlidar_ros2_driver' not found`

**Reason**: LiDAR driver dependency missing

**Fix**:

```bash
cd ~/roboai_ws/src
git clone https://github.com/YDLIDAR/ydlidar_ros2_driver.git
cd ~/roboai_ws
rosdep install --from-paths src -y --ignore-src
```

---

### ❌ Issue 2: `cannot find -lydlidar_sdk`

**Error**:

```
/usr/bin/ld: cannot find -lydlidar_sdk
```

**Root cause**:

* SDK built but **not installed system-wide**   

**Correct fix**:

```bash
cd ~/roboai_ws/src/tortoisebot/YDLidar-SDK/
mkdir -p build && cd build
cmake ..
make
sudo make install
sudo ldconfig
```

Then rebuild:

```bash
cd ~/roboai_ws
rm -rf build install log
colcon build --symlink-install
```

---

### ❌ Issue 3: RViz shows no laser / robot movement

**Possible causes**:

* Missing `/scan` topic
* TF not published
* Fixed Frame mismatch

**Quick checks**:

```bash
ros2 topic list | grep scan
ros2 run tf2_tools view_frames
```

In RViz:

* Fixed Frame → `odom` or `map`

---

## 🧠 Key Learning Outcomes

By working with TortoiseBot, you learn:

* ROS 2 workspace & colcon
* TF tree and coordinate frames
* Gazebo ↔ ROS integration
* SLAM & Navigation basics
* Debugging real-world ROS issues

---

## 📚 Recommended Next Steps

* Visualize TF properly in RViz2
* Tune LiDAR & Nav2 parameters
* Try **mapping first**, then navigation
* Disable hardware drivers for pure simulation

---

## ✅ Summary

TortoiseBot is an **excellent ROS 2 learning platform**. Understanding:

* *what it is*
* *why it’s used*
* *how it works*
* *how to debug it*

will give you **strong ROS 2 fundamentals** applicable to any mobile robot.

---

Happy Robotics 🤖🐢
