import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class FakeCamera(Node):
    def __init__(self):
        super().__init__('fake_camera')

        self.publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.publish_image)

        self.frame_count = 0
        self.box_x = 40
        self.direction = 1

        self.get_logger().info('Fake Camera started')

    def publish_image(self):
        msg = Image()

        width = 320
        height = 240

        image = np.zeros((height, width, 3), dtype=np.uint8)

        box_w = 80
        box_h = 80
        box_y1 = 80
        box_y2 = box_y1 + box_h

        self.box_x += self.direction * 5

        if self.box_x <= 0:
            self.box_x = 0
            self.direction = 1

        if self.box_x + box_w >= width:
            self.box_x = width - box_w
            self.direction = -1

        box_x1 = self.box_x
        box_x2 = self.box_x + box_w

        image[box_y1:box_y2, box_x1:box_x2] = [255, 0, 0]

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'

        msg.height = height
        msg.width = width
        msg.encoding = 'rgb8'
        msg.step = width * 3
        msg.data = image.tobytes()

        self.publisher.publish(msg)

        self.frame_count += 1
        if self.frame_count % 10 == 0:
            center_x = box_x1 + box_w // 2
            self.get_logger().info(
                f'Published camera image: red_box_center_x={center_x}, direction={self.direction}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = FakeCamera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()