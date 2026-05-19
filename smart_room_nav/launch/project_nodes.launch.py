from launch import LaunchDescription
from launch_ros.actions import Node
import os


def generate_launch_description():

    pkg_path = os.path.join(os.path.expanduser('~/ros2_ws/src/smart_room_nav'))
    room_yaml = os.path.join(pkg_path, 'config', 'room_poses.yaml')
    model_pkl = os.path.join(pkg_path, 'config', 'model.pkl')
    
    return LaunchDescription([

            Node(
                package='smart_room_nav',
                executable='input_node',
                name='input_node',
                output='screen'
            ),

            Node(
                package='smart_room_nav',
                executable='decision_node',
                name='decision_node',
                output='screen',
                parameters=[{'model_config': model_pkl}]
            ),

            Node(
                package='smart_room_nav',
                executable='navigator_node',
                name='navigator_node',
                output='screen',
                parameters=[{'room_yaml': room_yaml}]
            )
        ])