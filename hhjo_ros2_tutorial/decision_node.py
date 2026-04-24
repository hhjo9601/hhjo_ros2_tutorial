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

        # Camera position priority
        if 'camera_object_left' in perception_result:
            vector.x = 0.05
            vector.z = 2.0
            return vector

        if 'camera_object_right' in perception_result:
            vector.x = 0.05
            vector.z = -2.0
            return vector

        if 'camera_object_center' in perception_result:
            vector.x = 0.0
            vector.z = 0.0
            return vector

        # LiDAR fallback
        if perception_result == 'clear':
            vector.x = 0.5
            vector.z = 0.0

        elif 'front_blocked_turn_left' in perception_result:
            vector.x = 0.2
            vector.z = 1.2

        elif 'front_blocked_turn_right' in perception_result:
            vector.x = 0.2
            vector.z = -1.2

        elif 'left_blocked' in perception_result:
            vector.x = 0.3
            vector.z = -0.8

        elif 'right_blocked' in perception_result:
            vector.x = 0.3
            vector.z = 0.8

        elif 'left_right_blocked' in perception_result:
            vector.x = 0.0
            vector.z = 1.5

        else:
            vector.x = 0.0
            vector.z = 0.0

        return vector

    def handle_camera_only(self, result: str) -> Vector3:
        vector = Vector3()

        vector.x = 0.2

        if 'left' in result:
            vector.z = 1.2
        elif 'right' in result:
            vector.z = -1.2
        elif 'center' in result:
            vector.x = 0.05
            vector.z = 0.0
        else:
            vector.z = 0.0

        return vector

    def handle_lidar_camera_fusion(self, result: str) -> Vector3:
        vector = Vector3()

        vector.x = 0.1

        if 'front_blocked_turn_left' in result:
            vector.z = 0.7
        elif 'front_blocked_turn_right' in result:
            vector.z = -0.7
        elif 'left_blocked' in result:
            vector.z = -0.4
        elif 'right_blocked' in result:
            vector.z = 0.4
        elif 'left_right_blocked' in result:
            vector.z = 0.8
        else:
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