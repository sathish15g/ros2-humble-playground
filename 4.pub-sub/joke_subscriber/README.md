# joke_subscriber ✅

**Short description**

`joke_subscriber` is a small ROS 2 node that listens to the `/programming_jokes` topic and logs/prints received jokes. It demonstrates a basic `rclpy` subscription with a `RELIABLE` QoS profile.

---

## 🔧 What the code does

- File: `joke_subscriber/joke_subscriber.py`
  - Defines a `JokeSubscriber` node that:
    - Subscribes to `String` messages on the `/programming_jokes` topic.
    - Logs received messages and prints a short reaction.
    - Uses a `QoSProfile` with `RELIABLE` reliability and `depth=10`.

---

## ▶️ Build & Run (recommended)

1. Build with colcon from your workspace root and source the install overlay:

```bash
colcon build --packages-select joke_subscriber

# Linux/macOS
. install/setup.bash

# Windows (PowerShell)
call install\setup.ps1
```

2. Run the node:

```bash
ros2 run joke_subscriber joke_subscriber
```

3. If you'd rather see the raw topic data from any publisher, use:

```bash
ros2 topic echo /programming_jokes std_msgs/msg/String
```

---

## 🧪 Run without building (dev / quick test)

```bash
python -m joke_subscriber.joke_subscriber
```

---

## ℹ️ Notes

- Topic: `/programming_jokes`
- Message type: `std_msgs/msg/String`
- QoS: RELIABLE, depth=10

---

If you want, I can add a small `launch` file that runs both `joke_publisher` and `joke_subscriber` together (and an example `ros2 launch` invocation). 🔧