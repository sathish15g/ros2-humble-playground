from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # Declare and Define launch configurations for parameters
    topic_name_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='/frequency_chatter',
        description='Topic name for publisher and subscriber'
    )
    frequency_arg = DeclareLaunchArgument(
        'frequency',
        default_value='2.0',
        description='Publishing frequency in Hz'
    )

    frequency = LaunchConfiguration('frequency', default='2.0')
    topic_name = LaunchConfiguration('topic_name', default='/frequency_chatter')

    # Create publisher node with parameters
    publisher_node = Node(
        package='my_launch_pkg',
        executable='publisher.py',
        name='frequency_publisher',
        parameters=[{
            'frequency': ParameterValue(frequency, value_type=float),
            'topic_name': ParameterValue(topic_name, value_type=str)
        }]
    )

    # Create subscriber node with parameters
    subscriber_node = Node(
        package='my_launch_pkg',
        executable='subscriber.py',
        name='frequency_subscriber',
        parameters=[{
            'topic_name': ParameterValue(topic_name, value_type=str)
        }]
    )

    return LaunchDescription([
        topic_name_arg,
        frequency_arg,
        publisher_node,
        subscriber_node
    ])