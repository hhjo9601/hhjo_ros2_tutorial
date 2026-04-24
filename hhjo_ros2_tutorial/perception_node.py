import math
import numpy as np

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String


class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        self.front_threshold = 1.2

        self.camera_red_detected = False
        self.camera_red_ratio = 0.0
        self.camera_object_position = 'none'

        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.perception_pub = self.create_publisher(
            String,
            '/perception/obstacle_direction',
            10
        )

        self.get_logger().info('Perception node started')

    def image_callback(self, msg: Image):
        if msg.encoding != 'rgb8':
            self.get_logger().warn(f'Unsupported image encoding: {msg.encoding}')
            return

        image = np.frombuffer(msg.data, dtype=np.uint8)
        image = image.reshape((msg.height, msg.width, 3))

        red = image[:, :, 0]
        green = image[:, :, 1]
        blue = image[:, :, 2]

        red_mask = (red > 150) & (green < 80) & (blue < 80)

        red_pixels = np.where(red_mask)
        red_count = len(red_pixels[0])

        self.camera_red_ratio = float(red_count) / float(msg.height * msg.width)
        self.camera_red_detected = self.camera_red_ratio > 0.03

        if not self.camera_red_detected:
            self.camera_object_position = 'none'
            return

        avg_x = float(np.mean(red_pixels[1]))

        if avg_x < msg.width / 3:
            self.camera_object_position = 'left'
        elif avg_x > msg.width * 2 / 3:
            self.camera_object_position = 'right'
        else:
            self.camera_object_position = 'center'

    def scan_callback(self, msg: LaserScan):
        left = self.get_min_range(msg, math.radians(30), math.radians(90))
        front = self.get_min_range(msg, math.radians(-30), math.radians(30))
        right = self.get_min_range(msg, math.radians(-90), math.radians(-30))

        lidar_result = self.decide_lidar_direction(left, front, right)
        fusion_result = self.fuse_result(lidar_result)

        out = String()
        out.data = fusion_result
        self.perception_pub.publish(out)

        self.get_logger().info(
            f'left={left:.2f}, front={front:.2f}, right={right:.2f}, '
            f'camera_detected={self.camera_red_detected}, '
            f'camera_pos={self.camera_object_position}, '
            f'red_ratio={self.camera_red_ratio:.3f} -> {fusion_result}'
        )

    def get_min_range(self, msg: LaserScan, start_angle: float, end_angle: float) -> float:
        values = []

        for i, distance in enumerate(msg.ranges):
            angle = msg.angle_min + i * msg.angle_increment

            if start_angle <= angle <= end_angle:
                if math.isfinite(distance) and msg.range_min <= distance <= msg.range_max:
                    values.append(distance)

        if not values:
            return float('inf')

        return min(values)

    def decide_lidar_direction(self, left: float, front: float, right: float) -> str:
        left_blocked = left < self.front_threshold
        front_blocked = front < self.front_threshold
        right_blocked = right < self.front_threshold

        if front_blocked:
            if left > right:
                return 'front_blocked_turn_left'
            return 'front_blocked_turn_right'

        if left_blocked and right_blocked:
            return 'left_right_blocked'

        if left_blocked:
            return 'left_blocked'

        if right_blocked:
            return 'right_blocked'

        return 'clear'

    def fuse_result(self, lidar_result: str) -> str:
        if not self.camera_red_detected:
            return lidar_result

        if lidar_result == 'clear':
            return f'camera_object_{self.camera_object_position}_slow_down'

        return f'{lidar_result}_camera_object_{self.camera_object_position}'


def main(args=None):
    rclpy.init(args=args)
    node = PerceptionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
        