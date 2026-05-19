#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray, String
import joblib
import os

class DecisionNode(Node):
    def __init__(self):
        super().__init__('decision_node')

        # Load config param (path to model.pkl)
        model_config = self.declare_parameter('model_config', '').get_parameter_value().string_value
        if not model_config:
            self.get_logger().error("No model_config param provided")
            exit(1)

        model_path = model_config
        if not os.path.isabs(model_path):
            # try relative to package config dir
            model_path = os.path.join(os.path.dirname(__file__), '..', 'config', model_config)

        self.get_logger().info(f"Loading model from {model_path}")

        bundle = joblib.load(model_path)

        if isinstance(bundle, dict):
            # Expected bundle with model + mappings
            self.model = bundle["model"]
            self.mappings = bundle["mappings"]
            self.target_labels = self.mappings["Target Room"]
        else:
            # Fallback: got a bare model, no mappings
            self.get_logger().warn("Loaded a bare model without mappings. Using default labels [kitchen, bedroom, living_room].")
            self.model = bundle
            self.mappings = {"Target Room": ["kitchen", "bedroom", "living_room"]}
            self.target_labels = self.mappings["Target Room"]

        self.sub = self.create_subscription(Int32MultiArray, 'task_conditions', self.callback, 10)
        self.pub = self.create_publisher(String, 'target_room', 10)

    def callback(self, msg):
        features = [msg.data]
        pred_num = self.model.predict(features)[0]
        room_name = self.target_labels[pred_num]
 
        room_name = room_name.replace(" ", "_").lower()
        

        self.get_logger().info(f"Predicted room: {room_name}")
        out = String()
        out.data = room_name
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

