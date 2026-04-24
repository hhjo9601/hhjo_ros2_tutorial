import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from geometry_msgs.msg import Vector3, Twist, Point
from visualization_msgs.msg import Marker


class VisualizationNode(Node):
    def __init__(self):
        super().__init__('visualization_node')

        self.perception_result = 'waiting'
        self.decision_vector = Vector3()
        self.cmd_vel = Twist()

        self.create_subscription(
            String,
            '/perception/obstacle_direction',
            self.perception_callback,
            10
        )

        self.create_subscription(
            Vector3,
            '/decision/velocity_vector',
            self.decision_callback,
            10
        )

        self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_callback,
            10
        )

        self.status_pub = self.create_publisher(
            Marker,
            '/visualization/status_marker',
            10
        )

        self.vector_pub = self.create_publisher(
            Marker,
            '/visualization/velocity_marker',
            10
        )

        self.timer = self.create_timer(0.2, self.publish_markers)

        self.get_logger().info('Visualization node started')

    def perception_callback(self, msg: String):
        self.perception_result = msg.data

    def decision_callback(self, msg: Vector3):
        self.decision_vector = msg

    def cmd_callback(self, msg: Twist):
        self.cmd_vel = msg

    def publish_markers(self):
        self.publish_status_text()
        self.publish_velocity_arrow()

    def publish_status_text(self):
        marker = Marker()
        marker.header.frame_id = 'base_link'
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = 'status'
        marker.id = 0
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        marker.pose.position.x = 0.0
        marker.pose.position.y = 0.0
        marker.pose.position.z = 1.2

        marker.scale.z = 0.22

        marker.color.r = 0.1
        marker.color.g = 0.2
        marker.color.b = 0.9
        marker.color.a = 1.0

        marker.text = (
            f'Perception: {self.perception_result}\n'
            f'Decision Vector: x={self.decision_vector.x:.2f}, z={self.decision_vector.z:.2f}\n'
            f'CmdVel: linear.x={self.cmd_vel.linear.x:.2f}, angular.z={self.cmd_vel.angular.z:.2f}'
        )

        self.status_pub.publish(marker)

    def publish_velocity_arrow(self):
        marker = Marker()
        marker.header.frame_id = 'base_link'
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = 'velocity'
        marker.id = 1
        marker.type = Marker.ARROW
        marker.action = Marker.ADD

        marker.scale.x = 0.05
        marker.scale.y = 0.10
        marker.scale.z = 0.10

        marker.color.r = 0.0
        marker.color.g = 0.8
        marker.color.b = 0.2
        marker.color.a = 1.0

        start = Point()
        start.x = 0.0
        start.y = 0.0
        start.z = 0.2

        end = Point()
        end.x = max(self.cmd_vel.linear.x, 0.05)
        end.y = self.cmd_vel.angular.z * 0.4
        end.z = 0.2

        marker.points = [start, end]

        self.vector_pub.publish(marker)


def main(args=None):
    rclpy.init(args=args)
    node = VisualizationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()