'''#!/usr/bin/env python3
import rclpy, yaml, os, math
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from ament_index_python.packages import get_package_share_directory

def quat_from_yaw(yaw):
    q = Quaternion()
    q.z = math.sin(yaw/2.0)
    q.w = math.cos(yaw/2.0)
    return q

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')

        self.navigator = BasicNavigator()
        self.declare_parameter('room_yaml', 'room_poses.yaml')
        room_yaml_name = self.get_parameter('room_yaml').get_parameter_value().string_value

        pkg = get_package_share_directory('smart_room_nav')
        room_yaml = os.path.join(pkg, 'config', room_yaml_name)

        with open(room_yaml, 'r') as f:
            self.room_data = yaml.safe_load(f)['rooms']

        # SUBSCRIBE FOR GOALS
        self.sub = self.create_subscription(String, 'target_room', self.cb, 10)

        # ✅ PUBLISH WHEN DONE
        #self.done_pub = self.create_publisher(Bool, 'goal_reached', 10)

        # Wait for Nav2
        self.get_logger().info('Waiting for Nav2...')
        self.navigator.waitUntilNav2Active()
        self.get_logger().info('Nav2 ACTIVE')


    def cb(self, msg: String):
        room = msg.data

        if room not in self.room_data:
            self.get_logger().warn(f'Unknown room: {room}')
            return

        info = self.room_data[room]

        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = float(info['x'])
        pose.pose.position.y = float(info['y'])
        pose.pose.orientation = quat_from_yaw(float(info['yaw']))

        self.get_logger().info(f'Navigating to {room}')
        self.navigator.goToPose(pose)
        result = self.navigator.getResult()
        self.get_logger().info(f'Result: {result}')

        if result == TaskResult.SUCCEEDED:
            self.get_logger().info(f"Result: {result}")

            msg_done = Bool()
            msg_done.data = True
            self.done_pub.publish(msg_done)


def main():
    rclpy.init()
    node = NavigatorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()'''


#!/usr/bin/env python3
import rclpy, yaml, os, math
from rclpy.node import Node
from std_msgs.msg import String, Bool
from geometry_msgs.msg import PoseStamped, Quaternion
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from ament_index_python.packages import get_package_share_directory

def quat_from_yaw(yaw):
    q = Quaternion()
    q.z = math.sin(yaw/2.0)
    q.w = math.cos(yaw/2.0)
    return q

class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')

        self.navigator = BasicNavigator()

        self.done_pub = self.create_publisher(Bool, 'goal_reached', 10)

        self.declare_parameter('room_yaml', 'room_poses.yaml')
        room_yaml_name = self.get_parameter('room_yaml').get_parameter_value().string_value

        pkg = get_package_share_directory('smart_room_nav')
        room_yaml = os.path.join(pkg, 'config', room_yaml_name)

        with open(room_yaml, 'r') as f:
            self.room_data = yaml.safe_load(f)['rooms']

        # SUBSCRIBE FOR GOALS
        self.sub = self.create_subscription(String, 'target_room', self.cb, 10)

        # Wait for Nav2
        self.get_logger().info('Waiting for Nav2...')
        self.navigator.waitUntilNav2Active()
        self.get_logger().info('Nav2 ACTIVE')

        self.init_timer = self.create_timer(5.0, self.publish_initial_goal)

    def cb(self, msg: String):
        room = msg.data

        if room not in self.room_data:
            self.get_logger().warn(f'Unknown room: {room}')
            return

        info = self.room_data[room]

        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.get_clock().now().to_msg()

        pose.pose.position.x = float(info['x'])
        pose.pose.position.y = float(info['y'])
        pose.pose.orientation = quat_from_yaw(float(info['yaw']))

        self.get_logger().info(f'Navigating to {room}')

        self.navigator.goToPose(pose)

        while not self.navigator.isTaskComplete():
            rclpy.spin_once(self, timeout_sec=0.1)

        result = self.navigator.getResult()

        self.get_logger().info(f'Result: {result}')

        # ✅ FIX 3: Trigger next goal ONLY on success
        if result == TaskResult.SUCCEEDED:
            self.get_logger().info("Goal reached → triggering next goal")

            msg_done = Bool()
            msg_done.data = True
            self.done_pub.publish(msg_done)

    def publish_initial_goal(self):
        msg = Bool()
        msg.data = True
        self.done_pub.publish(msg)
        self.get_logger().info("Initial goal trigger sent")

        # Stop timer after first run
        self.destroy_timer(self.init_timer)


def main():
    rclpy.init()
    node = NavigatorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()