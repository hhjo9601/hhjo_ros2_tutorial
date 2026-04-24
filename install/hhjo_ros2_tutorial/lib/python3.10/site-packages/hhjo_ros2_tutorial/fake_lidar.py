import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import random
import math

class FakeLidar(Node):
    def __init__(self):
        super().__init__('fake_lidar')

        self.pub = self.create_publisher(LaserScan, '/scan', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.num_points = 360
        self.min_range = 0.2
        self.max_range = 5.0

    def timer_callback(self):
        msg = LaserScan()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "base_scan"

        msg.angle_min = 0.0
        msg.angle_max = 2 * math.pi
        msg.angle_increment = (2 * math.pi) / self.num_points

        msg.range_min = self.min_range
        msg.range_max = self.max_range

        ranges = []
        for i in range(self.num_points):
            d = random.uniform(self.min_range, self.max_range)
            if 170 < i < 190:
                d = random.uniform(0.2, 1.0)
            ranges.append(d)

        msg.ranges = ranges
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = FakeLidar()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()