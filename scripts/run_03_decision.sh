#!/usr/bin/env bash
set -e

colcon build --packages-select hhjo_ros2_tutorial   
source ./scripts/env.sh

# 로그 폴더 생성
LOG_DIR="./scripts/logs/run_03/run_03_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

echo "[03] Running with logs → $LOG_DIR"

# 실행 함수
run_node () {
    local name=$1
    shift
    echo "[RUN] $name"
    "$@" > "$LOG_DIR/${name}.log" 2>&1 &
    pids+=($!)
}

pids=()

sleep 2

run_node lidar ros2 run hhjo_ros2_tutorial fake_lidar
run_node camera ros2 run hhjo_ros2_tutorial fake_camera

sleep 2

run_node perception ros2 run hhjo_ros2_tutorial perception_node

sleep 2

run_node decision ros2 run hhjo_ros2_tutorial decision_node

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