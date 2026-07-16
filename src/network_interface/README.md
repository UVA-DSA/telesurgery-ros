# Network Interface Node

This accepts either ROS2 ITPRaw messages (byte arrays) or UDP, and **only** outputs ROS2 ITP messages.

If the first module that will receive information on the PSM side is expecting UDP packets,
do NOT route information through this node since it does not output UDP. 
Only use if the next node is expecting ROS2 structured ITP messages.