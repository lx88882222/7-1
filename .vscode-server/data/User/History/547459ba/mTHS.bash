# realsense2_camera.bash
ros2 launch realsense2_camera on_dog.py >/dev/null 2>&1 &
ros2 lifecycle set /camera/camera configure
ros2 lifecycle set /camera/camera activate
