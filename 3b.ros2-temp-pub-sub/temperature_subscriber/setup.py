from setuptools import find_packages, setup

package_name = 'temperature_subscriber'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sathish15g',
    maintainer_email='gsathishkumar15@gmail.com',
    description='ROS 2 Temperature Subscriber Node using sensor_msgs/Temperature',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'temperature_subscriber = temperature_subscriber.temprature_subscriber_node:main',
        ],
    },
)
