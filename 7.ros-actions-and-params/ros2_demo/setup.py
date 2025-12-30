from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'ros2_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # 👇 ADD THIS FOR LAUNCH FILES
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sathish',
    maintainer_email='gsathishkumar15@gmail.com',
    description='ROS 2 Actions and Parameters Demo',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fibonacci_action_server = ros2_demo.fibonacci_action_server:main',
            'fibonacci_action_client = ros2_demo.fibonacci_action_client:main',
            'param_node = ros2_demo.param_node:main',
        ],
    },
)
