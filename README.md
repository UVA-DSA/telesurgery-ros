# telesurgery-ros
Telesurgery stack integrated with ROS

# Setup

You will need:

- Ubuntu 24.04 or later
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install)

## Conda
Create a conda instance with [Robostack](https://robostack.github.io/). This installed ROS2 Kilted into a conda instance.
`conda create -n ros_env -c conda-forge -c robostack-kilted ros-kilted-desktop`

Activate the instance

`conda activate ros_env`

Add the robostack channel to the environment

`conda config --env --add channels robostack-kilted`
`conda install pip` (if somehow pip isn't installed)

## pybullet-rendering

pybullet-rendering has not been updated for Python 3.12, but we can compile it from scratch.









