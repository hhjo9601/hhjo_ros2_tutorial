import math

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Vector3


class DecisionNode(Node):
    def __init__(self):
        super().__init__('decision_node')

        self.create_subscription(
            String,
            '/perception/obstacle_direction',
            self.perception_callback,
            10
        )

        self.decision_pub = self.create_publisher(
            Vector3,
            '/decision/velocity_vector',
            10
        )

        self.get_logger().info('Decision node started')

    def perception_callback(self, msg: String):
        perception_result = msg.data

        vector = self.make_decision(perception_result)

        self.decision_pub.publish(vector)

        self.get_logger().info(
            f'perception={perception_result} '
            f'-> vector=(x={vector.x:.2f}, y={vector.y:.2f}, z={vector.z:.2f})'
        )

    def make_decision(self, perception_result: str) -> Vector3:
        vector = Vector3()

        # x: linear speed
        # z: angular direction
        # z > 0: turn left
        # z < 0: turn right

        if perception_result == 'clear':
            vector.x = 0.5
            vector.y = 0.0
            vector.z = 0.0

        elif perception_result == 'front_blocked_turn_left':
            vector.x = 0.2
            vector.y = 0.0
            vector.z = 0.8

        elif perception_result == 'front_blocked_turn_right':
            vector.x = 0.2
            vector.y = 0.0
            vector.z = -0.8

        elif perception_result == 'left_blocked':
            vector.x = 0.3
            vector.y = 0.0
            vector.z = -0.4

        elif perception_result == 'right_blocked':
            vector.x = 0.3
            vector.y = 0.0
            vector.z = 0.4

        elif perception_result == 'left_right_blocked':
            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.8

        elif perception_result == 'camera_object_detected_slow_down':
            vector.x = 0.2
            vector.y = 0.0
            vector.z = 0.0

        elif 'camera_object_detected' in perception_result:
            vector.x = 0.1
            vector.y = 0.0

            if 'turn_left' in perception_result:
                vector.z = 0.7
            elif 'turn_right' in perception_result:
                vector.z = -0.7
            elif 'left_blocked' in perception_result:
                vector.z = -0.4
            elif 'right_blocked' in perception_result:
                vector.z = 0.4
            else:
                vector.z = 0.0

        else:
            # Unknown state: stop for safety
            vector.x = 0.0
            vector.y = 0.0
            vector.z = 0.0

        return vector


def main(args=None):
    rclpy.init(args=args)
    node = DecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()