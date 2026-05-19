# Smart-room-navigation using ROS2, Nav2 and ML

AI-powered Turtlebot3 house world room navigation system built using ROS2, Nav2, Gazebo, and TurtleBot3. The robot autonomously predicts target rooms using a Decision Tree ML model and navigates between custom room poses in a simulated smart home environment.

## Features

- Autonomous indoor room navigation
- Decision Tree based room prediction
- ROS2 Humble + Nav2 integration
- TurtleBot3 simulation in Gazebo
- Custom room pose mapping
- RViz2 visualization and localization
- Multi-node ROS2 architecture

---

## Tech Stack

- ROS2 Humble
- Nav2
- Gazebo
- TurtleBot3
- RViz2
- Python
- Scikit-learn

---

## Project Structure

```text
smart-room-navigation/
├── smart_room_nav/
│   ├── launch/
│   ├── config/
│   ├── resource/
│   ├── smart_room_nav/
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
│
├── nav_map/
│   ├── my_housemap.yaml
│   └── my_housemap.pgm
│
├── dataset/
│   └── smart_room_dataset.xlsx
│
└── README.md
```

---

## Workflow

1. Input node generates task conditions  
2. Decision node predicts the target room using a trained ML model  
3. Navigator node sends goal poses to Nav2  
4. TurtleBot3 autonomously navigates to the predicted room  

---

## Installation

Install required ROS2 packages:

```bash
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-nav2-bringup
sudo apt install ros-humble-turtlebot3*
sudo apt install ros-humble-turtlebot3-gazebo
```

Clone the repository and build the workspace:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

---

## Running the Project

### Terminal 1 — Gazebo

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```

### Terminal 2 — Nav2 + RViz

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=~/nav_map/my_housemap.yaml
```

### Terminal 3 — Project Nodes

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch smart_room_nav project_nodes.launch.py
```

---

## Mapping

### Start Cartographer SLAM

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_cartographer cartographer.launch.py use_sim_time:=True
```

### Teleop Keyboard

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

### Save Map

```bash
ros2 run nav2_map_server map_saver_cli -f ~/nav_map/my_housemap
```

---

## Machine Learning

The Decision Tree model was trained using a custom dataset containing:

- Time of Day
- Task Type
- Room Status
- Target Room

Dataset and trained model are included in the repository.

---

## Simulation

Screenshots from the project:

- Gazebo house world

  <img width="1855" height="1035" alt="image" src="https://github.com/user-attachments/assets/48dc89f8-2e6f-4567-a135-818f26149504" />

- RViz navigation

  <img width="1855" height="1035" alt="image" src="https://github.com/user-attachments/assets/440161f1-3117-48c5-87b8-dd89ac25daff" />

- Gazebo + Cartographer + Teleop

  <img width="1855" height="1035" alt="image" src="https://github.com/user-attachments/assets/395022f6-cdd0-43c2-a8fa-6318af519338" />

- Saved map

  <img width="819" height="600" alt="Screenshot from 2025-09-06 11-04-54" src="https://github.com/user-attachments/assets/5fcc6e4b-4a5c-4b60-8b88-fbc1f7cfaf4c" />

- Navigation path planning

  <img width="1855" height="1035" alt="image" src="https://github.com/user-attachments/assets/f3308a89-f0a7-4059-b7f0-902ace91db88" />
  <img width="1855" height="1035" alt="image" src="https://github.com/user-attachments/assets/60b24732-2f88-4893-8216-de8f593c3e5b" />


---

## Future Improvements

- Voice command integration
- Real robot deployment
- Dynamic obstacle avoidance
- Deep learning based prediction

---

## Credits

Built using ROS2 Humble, Nav2, Gazebo, and TurtleBot3.
