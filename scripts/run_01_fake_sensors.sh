#!/usr/bin/env bash
set -e

colcon build --packages-select hhjo_ros2_tutorial   
source ./scripts/env.sh

echo "[01] Running Fake Sensors + Visualization"

sleep 2
# -------------------------------
# Fake Sensors
# -------------------------------
ros2 run hhjo_ros2_tutorial fake_lidar &
LIDAR_PID=$!

sleep 2

ros2 run hhjo_ros2_tutorial fake_camera &
CAMERA_PID=$!

# # -------------------------------
# # Visualization (RViz)
# # -------------------------------
sleep 2 # sensors 올라올 시간

rviz2 &
RVIZ_PID=$!

# ==========================================================
# RViz Setup Guide (Manual Steps)
# ==========================================================
#
# 1. Set Fixed Frame:
#    - Top left → "Global Options"
#    - Set "Fixed Frame" → base_scan
#
# 2. Add LiDAR Visualization:
#    - Click "Add"
#    - Select "LaserScan"
#    - Topic → /scan
#
# 3. Add Camera Visualization:
#    - Click "Add"
#    - Select "Image"
#    - Topic → /camera/image_raw
#
# 4. Verify:
#    - You should see a 2D scan (arc or points)
#    - You should see a red box image (fake object)
# ----------------------------------------------------------
# Optional (Camera Visualization):
#
# ----------------------------------------------------------
# Debug Commands:
#
#   ros2 topic list
#   ros2 topic echo /scan
#   ros2 topic echo /camera/image_raw
#
# ==========================================================

echo ""
echo "Press Ctrl+C to stop all"

trap "echo 'Stopping...'; kill $LIDAR_PID $CAMERA_PID $RVIZ_PID; exit" SIGINT

wait