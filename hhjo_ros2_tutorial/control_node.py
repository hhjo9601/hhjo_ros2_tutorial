import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Vector3, Twist


class ControlNode(Node):
    def __init__(self):
        super().__init__('control_node')

        self.create_subscription(
            Vector3,
            '/decision/velocity_vector',
            self.decision_callback,
            10
        )

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Control node started')

    def decision_callback(self, msg: Vector3):
        cmd = Twist()

        # Vector3 → Twist 변환
        cmd.linear.x = msg.x
        cmd.linear.y = 0.0
        cmd.linear.z = 0.0

        cmd.angular.x = 0.0
        cmd.angular.y = 0.0
        cmd.angular.z = msg.z

        self.cmd_pub.publish(cmd)

        self.get_logger().info(
            f'cmd_vel published: linear.x={cmd.linear.x:.2f}, angular.z={cmd.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()