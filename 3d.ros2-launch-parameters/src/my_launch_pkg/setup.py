from setuptools import find_packages, setup

package_name = 'my_launch_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/pub_sub.launch.py'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sathish15g',
    maintainer_email='gsathishkumar15@gmail.com',
    description='ROS2 package demonstrating launch parameters with publisher and subscriber nodes',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'publisher.py = my_launch_pkg.publisher:main',
            'subscriber.py = my_launch_pkg.subscriber:main',
        ],
    },
)
