'''#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Bool
import joblib
import os
import random

class InputNode(Node):
    def __init__(self):
        super().__init__('input_node')

        # Load model.pkl (for mappings only)
        model_path = os.path.expanduser('~/ros2_ws/src/smart_room_nav/config/model.pkl')
        if not os.path.exists(model_path):
            self.get_logger().error(f"Model file not found at (model_path)")
            exit(1)
        

        bundle = joblib.load(model_path)
        self.mappings = bundle["mappings"]

        # Build encoders
        self.encoders = {}
        for col, categories in self.mappings.items():
            self.encoders[col] = {name: i for i, name in enumerate(categories)}

        # Publisher
        self.pub = self.create_publisher(Int32MultiArray, 'task_conditions', 10)

        timer_period = 5.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    
    def timer_callback(self):
       
        # Random selection
        time_of_day = random.choice(self.mappings['Time of Day'])
        task_type = random.choice(self.mappings['Task Type'])
        room_status = random.choice(self.mappings['Room status'])

        # Encode
        encoded = [
            self.encoders['Time of Day'][time_of_day],
            self.encoders['Task Type'][task_type],
            self.encoders['Room status'][room_status],
        ]

        msg = Int32MultiArray()
        msg.data = encoded
        self.pub.publish(msg)

        self.get_logger().info(
            f"Generated: {time_of_day}, {task_type}, {room_status} -> Encoded {encoded}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = InputNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()'''

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, Bool
import joblib
import os
import random

class InputNode(Node):
    def __init__(self):
        super().__init__('input_node')

        # Load model.pkl
        model_path = os.path.expanduser('~/ros2_ws/src/smart_room_nav/config/model.pkl')
        if not os.path.exists(model_path):
            self.get_logger().error(f"Model file not found at {model_path}")
            exit(1)

        bundle = joblib.load(model_path)
        self.mappings = bundle["mappings"]

        # Build encoders
        self.encoders = {}
        for col, categories in self.mappings.items():
            self.encoders[col] = {name: i for i, name in enumerate(categories)}

        # Publisher
        self.pub = self.create_publisher(Int32MultiArray, 'task_conditions', 10)

        # ✅ Subscriber → trigger next goal
        self.sub = self.create_subscription(
            Bool,
            'goal_reached',
            self.trigger_callback,
            10
        )

        self.get_logger().info("Input node ready. Waiting for goal_reached signal...")

    def trigger_callback(self, msg):
        if not msg.data:
            return

        self.get_logger().info("Trigger received → generating new goal")

        # Random selection
        time_of_day = random.choice(self.mappings['Time of Day'])
        task_type = random.choice(self.mappings['Task Type'])
        room_status = random.choice(self.mappings['Room status'])

        # Encode
        encoded = [
            self.encoders['Time of Day'][time_of_day],
            self.encoders['Task Type'][task_type],
            self.encoders['Room status'][room_status],
        ]

        msg_out = Int32MultiArray()
        msg_out.data = encoded
        self.pub.publish(msg_out)

        self.get_logger().info(
            f"Generated: {time_of_day}, {task_type}, {room_status} -> Encoded {encoded}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = InputNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()