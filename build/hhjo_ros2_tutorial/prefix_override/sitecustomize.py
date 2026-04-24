import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/vertin/ros_hhjo/exp_ws/src/hhjo_ros2_tutorial/install/hhjo_ros2_tutorial'
