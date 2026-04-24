#!/usr/bin/env bash
set -e

colcon build --packages-select hhjo_ros2_tutorial
source ./scripts/env.sh

LOG_DIR="./scripts/logs/run_04/run_04_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

echo "[04] Running Fake Sensors + Perception + Decision + Control"
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

echo ""
echo "Running:"
echo " - fake_lidar      (/scan)"
echo " - fake_camera     (/camera/image_raw)"
echo " - perception_node (/perception/obstacle_direction)"
echo " - decision_node   (/decision/velocity_vector)"
echo " - control_node    (/cmd_vel)"
echo ""
echo "Check output:"
echo "  ros2 topic echo /cmd_vel"
echo ""
echo "Logs:"
echo "  tail -f $LOG_DIR/*.log"
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