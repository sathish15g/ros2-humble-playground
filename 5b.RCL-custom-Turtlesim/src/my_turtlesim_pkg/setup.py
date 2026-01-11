from setuptools import find_packages, setup

package_name = 'my_turtlesim_pkg'

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
    description='A custom turtlesim package with various movement nodes',
    license='Apache License 2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'turtle_linear_move = my_turtlesim_pkg.turtle_linear_move:main',
            'turtle_angular_move = my_turtlesim_pkg.turtle_angular_move:main',
            'turtle_square_move = my_turtlesim_pkg.turtle_square_move:main',
            'turtle_motion_controller = my_turtlesim_pkg.turtle_motion_controller:main',
        ],
    },
)
