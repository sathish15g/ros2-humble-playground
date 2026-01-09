# ROS 2 Actions and Parameters – Complete Guide

*(Explanation, Code, Build & Testing)*

## 1. Overview

ROS 2 provides different communication and configuration mechanisms:

- **Actions** → For long-running tasks with feedback and cancellation
- **Parameters** → For configuring node behavior dynamically

This document demonstrates both concepts together using Python (rclpy).

## 2. ROS 2 Actions

### What is an Action?

An Action is used when:

- Execution takes time
- Feedback is required
- The task can be cancelled
- Actions are asynchronous.

### Action Communication Flow

```
Client ----> Goal
Server ----> Feedback (while running)
Server ----> Result (when finished)
Client ----> Cancel (optional)
```

### When to Use Actions

- Robot navigation
- Arm movement
- Trajectory execution
- Map building

### Action Components

| Component | Purpose          |
|-----------|------------------|
| Goal      | Input to the task |
| Feedback  | Progress updates |
| Result    | Final output     |

## 3. ROS 2 Parameters

### What are Parameters?

Parameters are runtime configurable values for nodes.

They:

- Avoid hard-coded values
- Allow tuning without restarting nodes
- Control behavior (speed, frequency, mode, etc.)

### Parameter Characteristics

- Declared inside nodes
- Can be changed at runtime
- Support multiple data types

## 4. Create ROS 2 Package

### Workspace Setup

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
```

### Package Creation Command

```bash
ros2 pkg create ros2_demo \
  --build-type ament_python \
  --dependencies rclpy action_tutorials_interfaces
```

## 5. Package Structure

```
ros2_demo/
├── package.xml
├── setup.py
├── setup.cfg
├── launch/
│   └── demo_launch.py
├── ros2_demo/
│   ├── __init__.py
│   ├── fibonacci_action_server.py
│   ├── fibonacci_action_client.py
│   └── param_node.py
```

from rclpy.node import Node
from rclpy.action import ActionServer
from action_tutorials_interfaces.action import Fibonacci
import rclpy
import time


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')

        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',  # ✅ SAME NAME
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback = Fibonacci.Feedback()
        sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            sequence.append(sequence[i] + sequence[i - 1])

            feedback.partial_sequence = sequence   # ✅ FIX
            goal_handle.publish_feedback(feedback)

            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = sequence
        return result




def main():
    rclpy.init()
    node = FibonacciActionServer()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    node = FibonacciActionServer()
    rclpy.spin(node)
    rclpy.shutdown()
```

*See: [fibonacci_action_server.py](ros2_demo/fibonacci_action_server.py)*

### Fibonacci Action Client

**fibonacci_action_client.py**

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from action_tutorials_interfaces.action import Fibonacci


class FibonacciActionClient(Node):

    def __init__(self):
        super().__init__('fibonacci_action_client')

        self._client = ActionClient(self, Fibonacci, 'fibonacci')

        # ✅ SEND GOAL AUTOMATICALLY
        self.send_goal()

    def send_goal(self):
        goal_msg = Fibonacci.Goal()
        goal_msg.order = 10

        self.get_logger().info('Waiting for action server...')
        self._client.wait_for_server()

        self.get_logger().info('Sending goal...')
        self._send_goal_future = self._client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(
            f'Feedback: {feedback_msg.feedback.partial_sequence}'
        )


    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        self.destroy_node()



def main():
    rclpy.init()
    node = FibonacciActionClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

*See: [fibonacci_action_client.py](ros2_demo/fibonacci_action_client.py)*

## 7. Parameter Node Code

### Parameter Example Node

**param_node.py**

```python
import rclpy
from rclpy.node import Node


class ParamNode(Node):
    def __init__(self):
        super().__init__('param_node')

        self.declare_parameter('robot_speed', 1.0)
        speed = self.get_parameter('robot_speed').value

        self.get_logger().info(f'Robot speed: {speed}')


def main():
    rclpy.init()
    node = ParamNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

*See: [param_node.py](ros2_demo/param_node.py)*

## 8. setup.py Configuration

```python
from setuptools import setup

package_name = 'ros2_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sathish Kumar G',
    description='ROS 2 Actions and Parameters Demo',
    license='Apache License 2.0',
    entry_points={
        'console_scripts': [
            'fibonacci_action_server = ros2_demo.fibonacci_action_server:main',
            'fibonacci_action_client = ros2_demo.fibonacci_action_client:main',
            'param_node = ros2_demo.param_node:main',
        ],
    },
)
```

*See: [setup.py](setup.py)*

## 9. Build the Package

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## 10. Run & Test

### Run Action Server

```bash
ros2 run ros2_demo fibonacci_action_server
```

### Run Action Client

```bash
ros2 run ros2_demo fibonacci_action_client
```

### Inspect Actions

```bash
ros2 action list
ros2 action info /fibonacci
```

### Run Parameter Node

```bash
ros2 run ros2_demo param_node
```

### Parameter Testing

```bash
ros2 param list /param_node
ros2 param get /param_node robot_speed
ros2 param set /param_node robot_speed 3.5
```

## 11. Comparison Summary

| Feature      | Topic | Service | Action | Parameter |
|--------------|-------|---------|--------|-----------|
| Use case     | Streaming | Request/Reply | Long task | Configuration |
| Feedback     | ❌    | ❌      | ✅     | ❌        |
| Cancel       | ❌    | ❌      | ✅     | N/A       |
| Runtime change | N/A | ❌      | ✅     | ✅        |

## 12. One-Line Exam Definitions

- **Action**: Asynchronous communication for long-running tasks with feedback.
- **Parameter**: Runtime configurable value for node behavior.
- **Service**: Synchronous request-response mechanism.
- **Topic**: Continuous data streaming.

## 13. Real-World Analogy

| ROS 2      | Example                  |
|------------|--------------------------|
| Topic      | Radio broadcast          |
| Service    | Phone call               |
| Action     | Food delivery with tracking |
| Parameter  | App settings             |



## 14. ROS 2 Launch File

### What is a Launch File?

A launch file is used to:

- Start multiple nodes together
- Pass parameters at startup
- Control execution from one command

ROS 2 uses Python-based launch files.

### Why Use Launch Files?

- Avoid running multiple terminals
- Pass parameters cleanly
- Standardized startup process
- Production-ready deployment

## 15. Launch File Structure

Create a new folder inside your package:

```bash
mkdir -p ros2_demo/launch
```

File name: `ros2_demo/launch/demo_launch.py`

## 16. Launch File Code

**demo_launch.py**

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        Node(
            package='ros2_demo',
            executable='fibonacci_action_server',
            name='fibonacci_action_server'
        ),

        Node(
            package='ros2_demo',
            executable='fibonacci_action_client',
            name='fibonacci_action_client'
        ),

        Node(
            package='ros2_demo',
            executable='param_node',
            name='param_node',
            parameters=[{'robot_speed': 2.0}]
        ),
    ])
```

*See: [demo_launch.py](ros2_demo/launch/demo_launch.py)*

## Code Fixes (2026-01-07)

A small code fix was applied; please review and verify the following files for the change:

- `fibonacci_action_server.py`: [ros2_demo/ros2_demo/fibonacci_action_server.py](ros2_demo/ros2_demo/fibonacci_action_server.py)
- `fibonacci_action_client.py`: [ros2_demo/ros2_demo/fibonacci_action_client.py](ros2_demo/ros2_demo/fibonacci_action_client.py)
- `param_node.py`: [ros2_demo/ros2_demo/param_node.py](ros2_demo/ros2_demo/param_node.py)
- `demo_launch.py`: [ros2_demo/launch/demo_launch.py](ros2_demo/launch/demo_launch.py)

Quick verification steps:

```bash
colcon build
source install/setup.bash
ros2 launch ros2_demo demo_launch.py
```

If you want, I can run a quick build and launch to sanity-check the fix — tell me to proceed.


## 17. Update setup.py to Install Launch Files

Add this inside setup():

```python
import os
from glob import glob
```

### Modified setup.py

```python
from setuptools import setup
import os
from glob import glob

package_name = 'ros2_demo'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sathish Kumar G',
    description='ROS 2 Actions, Parameters and Launch Demo',
    license='Apache License 2.0',
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    entry_points={
        'console_scripts': [
            'fibonacci_action_server = ros2_demo.fibonacci_action_server:main',
            'fibonacci_action_client = ros2_demo.fibonacci_action_client:main',
            'param_node = ros2_demo.param_node:main',
        ],
    },
)
```

*See: [setup.py](setup.py)*

## 18. Build Again

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## 19. Run Using Launch File

### Single Command Execution

```bash
ros2 launch ros2_demo demo_launch.py
```

This will:

- Start Fibonacci Action Server
- Start Fibonacci Action Client
- Start Parameter Node with `robot_speed = 2.0`

## 20. Verify After Launch

### Check Running Nodes

```bash
ros2 node list
```

### Check Actions

```bash
ros2 action list
```

### Check Parameters

```bash
ros2 param list /param_node
ros2 param get /param_node robot_speed
```

### Change Parameter at Runtime

```bash
ros2 param set /param_node robot_speed 4.5
```

## 21. Launch File with Parameters vs CLI

| Method          | Usage                          |
|-----------------|--------------------------------|
| CLI             | Quick testing                  |
| Launch file     | Production / deployment        |
| YAML parameters | Large configurations           |

## 22. Final Folder Structure

```
ros2_demo/
├── launch/
│   └── demo_launch.py
├── ros2_demo/
│   ├── fibonacci_action_server.py
│   ├── fibonacci_action_client.py
│   └── param_node.py
├── package.xml
├── setup.py
```

## 23. One-Line Summary (Exam Ready)

- **Action**: Long-running task with feedback and cancellation
- **Parameter**: Runtime node configuration
- **Launch file**: Starts multiple nodes with configuration