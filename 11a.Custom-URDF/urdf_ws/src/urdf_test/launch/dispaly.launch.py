import launch
from launch import LaunchDescription
import launch_ros
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

import os

def generate_launch_description():
    urdf_file = PathJoinSubstitution([
        FindPackageShare('urdf_test'),
        'urdf',
        'model.urdf'
    ])

    robot_description = Command(['cat ', urdf_file])

    parameters = {'robot_description': robot_description}


    parameters = {'robot_description': robot_description}

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[parameters]
    )
    
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[parameters],
        condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    )

    joint_state_publisher_node_gui = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        parameters=[parameters],
        condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
    )

    rviz_node = launch_ros.actions.Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Flag to enable joint_state_publisher_gui'
        ),
        launch.actions.DeclareLaunchArgument(
            'model',
            default_value=urdf_file,
            description='Absolute path to robot urdf file'
        ),
        robot_state_publisher_node,
        joint_state_publisher_node,
        joint_state_publisher_node_gui,
        rviz_node
    ])