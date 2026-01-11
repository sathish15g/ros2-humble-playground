# Robot Motion Control Using ROS 2

## Introduction

Robot motion control involves directing a robot's movement through commands that specify velocities and directions. It is essential for applications ranging from autonomous navigation to industrial automation, ensuring precise and safe robot operations.

Publishing to `/cmd_vel` is crucial as it sends velocity commands (linear and angular) to the robot's base controller, enabling real-time movement adjustments. Without proper `/cmd_vel` publishing, the robot cannot execute desired trajectories.

The goal of this project is to implement a ROS 2 node that makes a robot (simulated turtle in turtlesim) move in a square path by publishing appropriate velocity commands.

## Materials & Tools Used

- **ROS 2 (Humble)**: The robotics middleware for node communication and message passing.
- **Python**: Programming language used for implementing the ROS 2 node with `rclpy`.
- **Turtlesim**: A simple simulator for testing robot motion control in ROS 2.
- **Gazebo (optional)**: Advanced simulator for more complex robot environments (not used in this basic implementation).

## Methodology

### Steps to Create a Publisher Node in ROS 2

1. Initialize a ROS 2 node using `rclpy.init()` and create a node class inheriting from `Node`.
2. Create a publisher for the `/turtle1/cmd_vel` topic with message type `geometry_msgs/msg/Twist`.
3. Implement functions for linear and angular motion.
4. Use a loop to execute the square movement sequence.
5. Publish zero velocities to stop the robot after completion.

### Twist Message Explanation

The `Twist` message contains two main components:
- **Linear velocities**: `linear.x`, `linear.y`, `linear.z` (m/s) – controls forward/backward and lateral movement.
- **Angular velocities**: `angular.x`, `angular.y`, `angular.z` (rad/s) – controls rotation around axes.

For 2D movement (like turtlesim), primarily use `linear.x` for forward speed and `angular.z` for turning.

### Logic of Moving in a Square Path

- Use a loop that runs 4 times (one for each side).
- In each iteration:
  - Move linearly forward for a fixed duration.
  - Rotate angularly by ~90 degrees for a fixed duration.
- Control timing using `time.sleep()` to maintain consistent movement periods.
- Publish velocities continuously during each motion phase.

### Timing Control

- `time.sleep(0.1)` is used in a loop to publish commands at 10 Hz during movement.
- Duration parameters (e.g., 2.0 seconds for linear, 1.0 second for angular) ensure approximate distances and angles.

## Problem-Solving Approach

### Common Issues and Fixes

- **Incorrect Timing**: Robot moves too fast/slow or turns inaccurately.
  - **Fix**: Adjust duration and speed parameters; test incrementally.
- **Overshooting Turns**: Turtle rotates more than 90 degrees.
  - **Fix**: Reduce angular speed or duration; use pose feedback for precise control.
- **Node Not Publishing**: Commands not reaching turtlesim.
  - **Fix**: Verify topic names, check ROS 2 logs with `ros2 topic echo /turtle1/cmd_vel`.

### Tuning Techniques

- Start with low speeds and short durations for testing.
- Use ROS 2 logging (`self.get_logger().info()`) to monitor movement phases.
- Adjust parameters based on observed behavior in turtlesim.

### Tips for Precise Movement and Debugging

- Publish at consistent rates (e.g., 10 Hz) to avoid jerky motion.
- Use `ros2 topic hz /turtle1/cmd_vel` to verify publishing frequency.
- Implement pose subscription for closed-loop control if needed.

## Diagrams/Flowcharts

### Flowchart of Movement Loop

```
Start
  |
  v
Initialize Node and Publisher
  |
  v
Loop 4 times:
  |
  +--> Move Linear (publish linear.x, duration)
  |     |
  |     v
  +--> Rotate Angular (publish angular.z, duration)
  |
  v
Publish Zero Velocities (Stop)
  |
  v
End
```

*(Placeholder: Insert flowchart image here, e.g., images/flowchart_square_movement.png)*

### Diagram of Square Path

```
   +----> (Linear Move)
   |     |
   |     v
   ^     +
   |     |
   +-----+ (Angular Rotate 90°)
     ^
     |
     (Repeat 4 times)
```

*(Placeholder: Insert square path diagram here, e.g., images/square_path_diagram.png)*

![Turtle Moving in Square](images/motion%20controller.png)

## Testing & Results

### Testing Procedure

- Launch turtlesim: `ros2 run turtlesim turtlesim_node`
- Run the motion control node: `ros2 run <package> <node>`
- Observe the turtle tracing a square in the simulator window.
- Check terminal logs for movement confirmations.

### Results

*(Placeholder: Insert screenshot of turtlesim showing square path, e.g., images/turtlesim_square_result.png)*

### Sample Terminal Logs

```
[INFO] [turtle_square_move]: Moving forward...
[INFO] [turtle_square_move]: Rotating 90 degrees...
[INFO] [turtle_square_move]: Moving forward...
[INFO] [turtle_square_move]: Rotating 90 degrees...
[INFO] [turtle_square_move]: Moving forward...
[INFO] [turtle_square_move]: Rotating 90 degrees...
[INFO] [turtle_square_move]: Moving forward...
[INFO] [turtle_square_move]: Rotating 90 degrees...
[INFO] [turtle_square_move]: Square completed
```

*(Placeholder: Insert screenshot of logs, e.g., images/terminal_logs.png)*

## Conclusion

This project demonstrated key ROS 2 concepts including publishing to `/cmd_vel`, using the `Twist` message for velocity control, implementing movement logic with loops and timing, and debugging motion issues. The turtle successfully traced a square path, showcasing basic robot motion control.

Potential extensions include:
- Implementing triangular or circular paths by adjusting movement sequences.
- Adding obstacle avoidance using laser scan data.
- Integrating autonomous path planning with navigation stacks like Nav2.
