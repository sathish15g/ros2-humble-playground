from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    fibonacci_server = Node(
        package='ros2_demo',
        executable='fibonacci_action_server',
        name='fibonacci_action_server'
    )

    fibonacci_client = Node(
        package='ros2_demo',
        executable='fibonacci_action_client',
        name='fibonacci_action_client'
    )

    param_node = Node(
        package='ros2_demo',
        executable='param_node',
        name='param_node',
        parameters=[
            {'robot_speed': 2.0}
        ]
    )

    return LaunchDescription([
        fibonacci_server,
        fibonacci_client,
        param_node
    ])
