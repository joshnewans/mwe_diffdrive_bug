This repo is to replicate a (possible) bug when simulating a differential drive robot with ROS 2 and Gazebo.


[![See video for example](https://img.youtube.com/vi/D3tFcviQr_k/0.jpg)](https://youtu.be/D3tFcviQr_k)



## Main Problem

There appears to be a synchronisation issue between the simulated sensor data and the reported odom tf.

The source of the issue could be (in order from most to least suspicious):
- Bad configuration
- `gazebo_ros2_control`
- `ros2_controllers/diff_drive_controller`
- `ros2_control`
- `gazebo_ros_plugins`
- Somewhere else

This is most visible when rotating on the spot. The lidar data "springs" in and out, and is at a constant(ish) offset while in constant motion. I do not believe the issue is due to wheel slip, the symptoms are too consistent and indicative of a timing issue, and I can't visually observe any slip when using the wireframe view in gazebo.

The issue is not apparent when using the `libgazebo_ros_diff_drive.so` plugin instead (which publishes a "totally correct" odom rather than an `diff_drive_controller`'s estimate?)


### Test environment
- ROS2 Foxy
- Tested with latest apt version and Github foxy branches (v0.8 of ros2_control)
- (Optional) `twist_stamper` (my own program) installed from `apt install ros-foxy-twist-stamper`


### Replicating the working (non ros2_control) system

- Launch `ros2 launch mwe_diffdrive_bug launch_gaz_control.launch.py`
- Send a `Twist` to `/cmd_vel` (e.g. with `teleop_twist_keyboard`)
- View the resulting LaserScan in RViz 

The room should stay perfectly aligned to the grid, even while rotating.


### Replicating the buggy system

- Launch `ros2 launch mwe_diffdrive_bug launch_ros2_control.launch.py`
- Start the controllers with `ros2 control load_controller --set-state start joint_state_broadcaster`
- and `ros2 control load_controller --set-state start test_controller`
- Send a `TwistStamped` message to `/test_controller/cmd_vel` (e.g. using `teleop_twist_keyboard` and `twist_stamper`)
- View in RViz


When stationary, the room should stay aligned to the grid. When rotation begins, the room will "spring" and then settle at an angle. Once rotation stops, the room will spring back to its original position (sometimes drifting over time)



## Possibly related problem

A possibly related issue is that when rotating with a depth camera, and the `points` topic displayed in RViz as a `PointCloud2`, the RGB and depth data is out of sync, causing a very disrupted view (and presumably causing similar issues with any nodes using the data?)