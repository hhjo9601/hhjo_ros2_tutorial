# ROS2 Autonomous Driving Tutorial (using Chat GPT)

This repository documents a step-by-step learning process of building an autonomous driving pipeline using ROS2, starting from fake sensors to full simulation with Gazebo and Nav2.

---

## Timeline

### 1. Fake Sensors

- Implemented a fake LiDAR publisher
- Implemented a fake camera publisher
- Learned ROS2 topic publishing and visualization
- Topics:
  - `/scan`
  - `/camera/image_raw`

### structure
fake_lidar  → /scan
fake_camera → /camera/image_raw

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

### structure
fake_lidar  → /scan
fake_camera → /camera/image_raw
          ↓
perception_node
          ↓
/perception/obstacle_direction

---

## Acknowledgements

This project was developed as part of a learning process using ROS2, with assistance from ChatGPT for problem-solving, system design, and iterative development.