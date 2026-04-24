from setuptools import find_packages, setup

package_name = 'hhjo_ros2_tutorial'

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
    maintainer='vertin',
    maintainer_email='jhh9601@naver.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fake_lidar = hhjo_ros2_tutorial.fake_lidar:main',
            'fake_camera = hhjo_ros2_tutorial.fake_camera:main',
            'perception_node = hhjo_ros2_tutorial.perception_node:main',
        ],
    },
)
