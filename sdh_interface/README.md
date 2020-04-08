To Run the node correctly:

1. Start sdh bringup by roslaunch schunk_bringup schunk_bringup.launch.
2. Call init to start SDH-ROS interface: rosservice call /sdh_controller/init 
3. Run this node by rosrun sdh_interface sdh_interface_node.py

