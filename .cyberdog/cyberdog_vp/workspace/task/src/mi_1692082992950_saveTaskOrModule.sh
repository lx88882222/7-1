# Copyright (c) 2023 Beijing Xiaomi Mobile Software Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# !/bin/sh
export ROS_VERSION=2
export ROS_PYTHON_VERSION=3
export ROS_LOCALHOST_ONLY=0
export ROS_DISTRO=galactic
export ROS_DOMAIN_ID=42
export LD_LIBRARY_PATH=/usr/lib/aarch64-linux-gnu/gazebo-11/plugins:/opt/ros2/galactic/opt/yaml_cpp_vendor/lib:/opt/ros2/galactic/opt/rviz_ogre_vendor/lib:/opt/ros2/galactic/lib:/opt/ros2/cyberdog/lib
export PYTHONPATH=/opt/ros2/cyberdog/lib/python3.6/site-packages:/opt/ros2/galactic/lib/python3.6/site-packages
export AMENT_PREFIX_PATH=/opt/ros2/cyberdog:/opt/ros2/galactic
export CMAKE_PREFIX_PATH=/opt/ros2/cyberdog:/opt/ros2/galactic
export COLCON_PREFIX_PATH=/opt/ros2/cyberdog:/opt/ros2/galactic
export PATH=/opt/ros2/galactic/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
export PKG_CONFIG_PATH=/opt/ros2/galactic/lib/aarch64-linux-gnu/pkgconfig:/opt/ros2/galactic/lib/pkgconfig
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///etc/mi/cyclonedds.xml
export DISPLAY=:0
export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:/usr/include/python3.6/
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
export USER=mi
python3 /home/mi/.cyberdog/cyberdog_vp/workspace/task/src/mi_1692082992950_saveTaskOrModule.py cyberdog_vp_task:=mi_1692082992950_saveTaskOrModule > /home/mi/.cyberdog/cyberdog_vp/workspace/log/mi_1692082992950_saveTaskOrModule.log 2>&1

