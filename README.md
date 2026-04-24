# ROS2 Autonomous Driving Tutorial

This repository documents a step-by-step learning process of building an autonomous driving pipeline using ROS2, starting from fake sensors to full simulation with Gazebo and Nav2.

## Quick start

If you want to run the complete pipeline from start to finish:

```bash
./scripts/run_05_visualization.sh
```

For more detailed explanation, please refer to **Timeline Section**.

---

## Timeline

### 1. Fake Sensors

- Implemented a fake LiDAR publisher
- Implemented a fake camera publisher
- Learned ROS2 topic publishing and visualization
- Topics:
  - `/scan`
  - `/camera/image_raw`

## Pipeline Structure

```text
fake_lidar         fake_camera
    ↓                  ↓
  /scan        /camera/image_raw
```

#### Run

```bash
./scripts/run_01_fake_sensors.sh
```

---

### 2. Perception

- Subscribed to fake LiDAR and fake camera topics
- Divided LiDAR scan data into three regions:
  - left
  - front
  - right
- Detected obstacle direction using minimum LiDAR distance
- Detected a red object from the fake camera image
- Fused LiDAR and camera results into a single perception output
- Published perception result to `/perception/obstacle_direction`

Topics:

- Input:
  - `/scan`
  - `/camera/image_raw`
- Output:
  - `/perception/obstacle_direction`

#### Run

```bash
./scripts/run_02_perception.sh
```

Pipeline Structure:

```text
fake_lidar         fake_camera
    ↓                  ↓
  /scan        /camera/image_raw
        \        /
         \      /
      perception_node
            ↓
/perception/obstacle_direction
```
---

### 3. Decision

- Subscribed to perception output
- Converted perception result into a velocity vector
- Used rule-based decision logic
- Published decision result to `/decision/velocity_vector`

Topics:

- Input:
  - `/perception/obstacle_direction`
- Output:
  - `/decision/velocity_vector`

Pipeline Structure:

```text
fake_lidar         fake_camera
    ↓                  ↓
  /scan        /camera/image_raw
        \        /
         \      /
      perception_node
            ↓
/perception/obstacle_direction
            ↓
       decision_node
            ↓
 /decision/velocity_vector
```

---

### 4. Control

- Subscribed to decision output
- Converted velocity vector into ROS2 velocity command
- Published robot command to `/cmd_vel`

Topics:

- Input:
  - `/decision/velocity_vector`
- Output:
  - `/cmd_vel`

Pipeline Structure:

```text
fake_lidar         fake_camera
    ↓                  ↓
  /scan        /camera/image_raw
        \        /
         \      /
      perception_node
            ↓
/perception/obstacle_direction
            ↓
       decision_node
            ↓
 /decision/velocity_vector
            ↓
       control_node
            ↓
         /cmd_vel
```

---

### 5. Control + Visualization

- Subscribed to decision output
- Converted velocity vector into ROS2 velocity command
- Published robot command to `/cmd_vel`
- Visualized perception, decision, and control outputs using RViz markers

Topics:

- Input:
  - `/decision/velocity_vector`
  - `/perception/obstacle_direction`
  - `/cmd_vel`
- Output:
  - `/cmd_vel`
  - `/visualization/status_marker`
  - `/visualization/velocity_marker`

Pipeline Structure:

```text
fake_lidar         fake_camera
    ↓                  ↓
  /scan        /camera/image_raw
        \        /
         \      /
      perception_node
            ↓
/perception/obstacle_direction
            ↓
       decision_node
            ↓
 /decision/velocity_vector
            ↓
       control_node
            ↓
         /cmd_vel
            ↓
   visualization_node
            ↓
/visualization/status_marker
/visualization/velocity_marker
```

---
### Acknowledgements

This project was developed as part of a learning process using ROS2, with assistance from ChatGPT for problem-solving, system design, and iterative development.