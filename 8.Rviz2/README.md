ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
ros2 launch slam_toolbox online_async_launch.py 
ros2 launch nav2_bringup rviz_launch.py 
ros2 run teleop_twist_keyboard teleop_twist_keyboard 
or 
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.5}}"

ros2 run tf2_tools view_frames


ros2 bag record -a -o rviz2_bag


Ctr+c to record

rviz2_bag/
  metadata.yaml
  chunk_0.db3

ros2 bag info rviz2_bag

ros2 bag play rviz2_bag 
