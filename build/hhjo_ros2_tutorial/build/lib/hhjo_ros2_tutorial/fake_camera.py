import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import numpy as np


class FakeCamera(Node):
    def __init__(self):
        super().__init__('fake_camera')

        self.publisher = self.create_publisher(Image, '/camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.publish_image)  # 10Hz

        self.get_logger().info('Fake Camera started')

    def publish_image(self):
        msg = Image()

        width = 320
        height = 240

        # RGB 이미지 생성
        image = np.zeros((height, width, 3), dtype=np.uint8)

        # 가운데 빨간 박스 (object)
        image[80:160, 120:200] = [255, 0, 0]

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'camera_link'

        msg.height = height
        msg.width = width
        msg.encoding = 'rgb8'
        msg.step = width * 3
        msg.data = image.tobytes()

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = FakeCamera()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()