# joke_publisher ✅

**Short description**

`joke_publisher` is a small ROS 2 node that publishes a random programming joke to the `/programming_jokes` topic as a `std_msgs/msg/String` message every 5 seconds.

---

## 🔧 What the code does

- File: `joke_publisher/joke_publisher.py`
  - Defines a `JokePublisher` node that:
    - Creates a `String` publisher on topic `/programming_jokes`.
    - Selects a random joke from a built-in list and publishes it every 5 seconds.
    - Uses a `QoSProfile` with `RELIABLE` reliability and `depth=10`.
  - The script entry point is `main()` and the package registers a console script entry point (`joke_publisher = joke_publisher.joke_publisher:main`) in `setup.py`.

---

## ▶️ Build & Run (recommended)

1. Build the package with colcon from your workspace root and source the install overlay:

```bash
colcon build --packages-select joke_publisher

# Linux/macOS
. install/setup.bash

# Windows (PowerShell)
call install\setup.ps1
```

2. Run the publisher node:

```bash
ros2 run joke_publisher joke_publisher
```

3. Verify messages are being published:

```bash
ros2 topic echo /programming_jokes std_msgs/msg/String
```

---

## 🧪 Run without building (dev / quick test)

To quickly run the module directly (useful during development):

```bash
python -m joke_publisher.joke_publisher
```

Note: running this way does not register the package with the ROS 2 CLI tools (so `ros2 run` won’t find it), but it’s handy for quick debugging.

---

## 📖 Code snippet (publisher)

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
import random


class JokePublisher(Node):
    def __init__(self):
        super().__init__('joke_publisher')
        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            depth=10
        )

        self.publisher_ = self.create_publisher(
            String,
            '/programming_jokes',
            10,
            qos
        )

        self.jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I told my computer I needed a break… it froze.",
            "Why did the developer go broke? Because he used up all his cache.",
            "There are only 10 types of people in the world: those who understand binary and those who don’t.",
            "A SQL query walks into a bar and asks: 'Can I JOIN you?'"
        ]

        self.timer = self.create_timer(5.0, self.publish_joke)
        self.get_logger().info("🤖 Joke Publisher started!")

    def publish_joke(self):
        msg = String()
        msg.data = random.choice(self.jokes)
        self.publisher_.publish(msg)
        self.get_logger().info(f"🃏 Joke published: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = JokePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

---

## ℹ️ Notes & Troubleshooting

- Topic: `/programming_jokes`
- Message type: `std_msgs/msg/String`
- Publish interval: 5 seconds
- QoS: RELIABLE, depth=10

If you don't see messages:
- Ensure your terminal has the workspace `install` sourced (same overlay in both terminals).
- Use `ros2 topic list` and `ros2 topic info /programming_jokes` to inspect the topic and QoS settings.

---

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