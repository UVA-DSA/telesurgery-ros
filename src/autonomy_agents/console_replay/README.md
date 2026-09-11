# Console Replay Node

Takes a replay file as input and sends its data over UDP or ROS2.
This only sends byte arrays, not structured data.

If sending over ROS2, send this to the Network Interface node,
where it will be reformatted into a structured ROS message.

If sending over UDP, the Network Interface node can be skipped altogether.