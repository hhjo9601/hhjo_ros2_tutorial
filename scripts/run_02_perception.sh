#!/usr/bin/env bash
set -e

colcon build --packages-select hhjo_ros2_tutorial   
source ./scripts/env.sh

echo "[02] Running Fake Sensors + Perception"

sleep 2

ros2 run hhjo_ros2_tutorial fake_lidar &
LIDAR_PID=$!

ros2 run hhjo_ros2_tutorial fake_camera &
CAMERA_PID=$!

sleep 2

ros2 run hhjo_ros2_tutorial perception_node &
PERCEPTION_PID=$!

echo ""
echo "Running:"
echo " - fake_lidar (/scan)"
echo " - fake_camera (/camera/image_raw)"
echo " - perception_node (/perception/obstacle_direction)"
echo ""
echo "Check result:"
echo "  ros2 topic echo /perception/obstacle_direction"
echo ""
echo "Press Ctrl+C to stop all"

trap "echo 'Stopping...'; kill $LIDAR_PID $CAMERA_PID $PERCEPTION_PID; exit" SIGINT

wait