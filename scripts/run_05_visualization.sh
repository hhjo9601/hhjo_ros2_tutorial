#!/usr/bin/env bash
set -e

colcon build --packages-select hhjo_ros2_tutorial
source ./scripts/env.sh

LOG_DIR="./scripts/logs/run_05/run_05_$(date +%Y%m%d_%H%M_%S)"
mkdir -p "$LOG_DIR"

echo "[05] Running Fake Sensors + Perception + Decision + Control"
echo "[LOG] $LOG_DIR"

pids=()

run_node() {
    local name=$1
    shift

    echo "[RUN] $name"
    "$@" > "$LOG_DIR/${name}.log" 2>&1 &
    pids+=($!)
}

sleep 2

run_node lidar ros2 run hhjo_ros2_tutorial fake_lidar
run_node camera ros2 run hhjo_ros2_tutorial fake_camera

sleep 2

run_node perception ros2 run hhjo_ros2_tutorial perception_node

sleep 2

run_node decision ros2 run hhjo_ros2_tutorial decision_node

sleep 2

run_node control ros2 run hhjo_ros2_tutorial control_node

sleep 2

run_node visualization ros2 run hhjo_ros2_tutorial visualization_node

rviz2 &
pids+=($!)

echo ""
echo "Running:"
echo " - fake_lidar          (/scan)"
echo " - fake_camera         (/camera/image_raw)"
echo " - perception_node     (/perception/obstacle_direction)"
echo " - decision_node       (/decision/velocity_vector)"
echo " - control_node        (/cmd_vel)"
echo " - visualization_node  (/visualization/status_marker, /visualization/velocity_marker)"
echo ""
echo "Logs:"
echo "  tail -f $LOG_DIR/*.log"
echo ""
echo "RViz Setup:"
echo "  Fixed Frame → base_scan"
echo "  Add → LaserScan → /scan"
echo "  Add → Marker → /visualization/status_marker"
echo "  Add → Marker → /visualization/velocity_marker"
echo ""
echo "Camera View:"
echo "  ros2 run rqt_image_view rqt_image_view"
echo "  Select topic → /camera/image_raw"
echo ""
echo "Press Ctrl+C to stop all"

cleanup() {
    echo "Stopping..."

    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
        fi
    done

    exit 0
}

trap cleanup SIGINT SIGTERM

wait