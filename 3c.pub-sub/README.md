# ros2 Pub-Sub examples (joke_publisher & joke_subscriber) ✅

**Overview**

This folder contains two small ROS 2 example packages demonstrating a publisher/subscriber pattern using `rclpy`:

- `joke_publisher` — publishes a random programming joke to `/programming_jokes` every 5 seconds.
- `joke_subscriber` — listens on `/programming_jokes` and prints/logs incoming jokes.

Both use `std_msgs/msg/String` and a `RELIABLE` QoS with `depth=10`.

---

## 📦 Packages

- `joke_publisher` — publisher node (`joke_publisher/joke_publisher.py`).
- `joke_subscriber` — subscriber node (`joke_subscriber/joke_subscriber.py`).

Each package contains its own `setup.py` and can be run as a console script (registered in `entry_points`). See the package-level READMEs for details.

---

## 🛠️ Prerequisites

- ROS 2 Humble installed and sourced
- colcon installed for building workspaces
- Python 3 and `rclpy` (installed as part of ROS 2)

---

## ▶️ Build & Run (recommended)

1. From the workspace root (where this folder lives), build both example packages:

```bash
# Build both example packages
colcon build --packages-select joke_publisher joke_subscriber

# Linux/macOS
. install/setup.bash

# Windows (PowerShell)
call install\setup.ps1
```

2. Run the publisher in one terminal:

```bash
ros2 run joke_publisher joke_publisher
```

3. Run the subscriber in another terminal:

```bash
ros2 run joke_subscriber joke_subscriber
```

4. (Optional) View raw messages with:

```bash
ros2 topic echo /programming_jokes std_msgs/msg/String
```

---

## 🧪 Quick dev run (no build)

For quick development or debugging you can run the modules directly (they require `rclpy` on your Python path):

```bash
python -m joke_publisher.joke_publisher
python -m joke_subscriber.joke_subscriber
```

Note: running this way is fine for testing but does not register the package with ROS 2 CLI tools.

---

## ✅ Tests

Run package tests with `colcon`:

```bash
colcon test --packages-select joke_publisher joke_subscriber
colcon test-result --verbose
```

---

## 🔧 Troubleshooting

- No topic visible: make sure your workspace `install` is sourced in the terminal (`. install/setup.bash` or `call install\setup.ps1`).
- Confirm topic presence and details:

```bash
ros2 topic list
ros2 topic info /programming_jokes
```

- If using `python -m` for dev runs, ensure `rclpy` is available in the same Python environment.

---

## 📚 Additional info

- Package-level READMEs:
  - `joke_publisher/README.md` — contains publisher details, code snippets, and run examples.
  - `joke_subscriber/README.md` — (added) contains subscriber details and usage examples.

---

## 👤 Author

**Sathish Kumar G**  
Robotics & ROS 2  

🔗 LinkedIn: https://www.linkedin.com/in/sathish15g/

## 📄 License

This project is licensed under the **Apache License 2.0**.  

You are free to use, modify, distribute, and sublicense this work under the terms of the license.  
For full license details, see the [LICENSE](../LICENSE) file in this repository.

---
