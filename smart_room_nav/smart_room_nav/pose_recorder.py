#!/usr/bin/env python3
import rclpy, yaml, os
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from ament_index_python.packages import get_package_share_directory

class PoseRecorder(Node):
    def __init__(self):
        super().__init__('pose_recorder')
        self.declare_parameter('label', '')
        self.declare_parameter('out', 'room_poses.yaml')
        self.label = self.get_parameter('label').get_parameter_value().string_value
        self.out = self.get_parameter('out').get_parameter_value().string_value
        self.sub = self.create_subscription(PoseStamped, '/goal_pose', self.cb, 10)
        self.get_logger().info(f'Waiting for a 2D Nav Goal in RViz2 to record as "{self.label}"…')

    def cb(self, msg: PoseStamped):
        entry = {
            'x': msg.pose.position.x,
            'y': msg.pose.position.y,
            'yaw': yaw_from_quat(msg.pose.orientation.z, msg.pose.orientation.w)  # planar yaw
        }
        data = {}
        if os.path.exists(self.out):
            with open(self.out, 'r') as f:
                try:
                    data = yaml.safe_load(f) or {}
                except Exception:
                    data = {}
        if 'rooms' not in data: data['rooms'] = {}
        data['rooms'][self.label] = entry
        with open(self.out, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False)
        self.get_logger().info(f'Saved "{self.label}": {entry} to {self.out}')
        rclpy.shutdown()

def yaw_from_quat(z, w):
    # Assuming planar orientation (x=y=0); yaw from (z,w)
    # yaw = 2*atan2(z, w)
    import math
    return 2.0 * math.atan2(z, w)

def main():
    rclpy.init()
    rclpy.spin(PoseRecorder())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
