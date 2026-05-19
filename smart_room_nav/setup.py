from setuptools import find_packages, setup

package_name = 'smart_room_nav'

setup(
    name='smart_room_nav',
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/project_nodes.launch.py']),
        ('share/' + package_name + '/config', ['config/room_poses.yaml', 'config/model_path.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sparsh05',
    maintainer_email='sparsh05@todo.todo',
    description='Smart room navigation with Decision Tree + Nav2',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'input_node = smart_room_nav.input_node:main',
            'decision_node = smart_room_nav.decision_node:main',
            'navigator_node = smart_room_nav.navigator_node:main',
            'pose_recorder = smart_room_nav.pose_recorder:main',
        ],
    },
)

