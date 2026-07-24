# telesurgery-ros
Telesurgery stack integrated with ROS

# Setup

You will need:

- Ubuntu 24.04
- [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/install/linux-install)

## Conda
Create a conda instance with [Robostack](https://robostack.github.io/). This installs ROS2 Kilted into a conda instance.
`conda create -n ros_env -c conda-forge -c robostack-kilted ros-kilted-desktop`

Activate the instance

`conda activate ros_env`

Add the Robostack channel to the environment

`conda config --env --add channels robostack-kilted`
`conda install pip` (if somehow pip isn't installed)
`pip install colcon-common-extensions`

## pybullet-rendering

pybullet-rendering has not been updated for Python 3.12, but we can compile it from scratch.
I made a fork of the repository to make it compatible.

First update all git submodules: 
- `git submodule update --init`

Go to the bullet3 instance provided by telesurgery-qos-analysis, then install

- `cd ../../../../`
- `cd telesurgery-qos-analysis/SurRoL_dVTrainer/ext/bullet3` (go to the bullet3 that's provided by telesurgery-qos-analysis)
- `export BULLET_ROOT_DIR="$PWD"`
- `pip install pybullet` (don't need to build bullet3 from scratch)
- `cd ../../../../`
- `cd pybullet-rendering`
- `python setup.py install --bullet_dir "$BULLET_ROOT_DIR"`

## Other things to install

In the `ext/NetFI` directory:
- `git checkout ros2`
- `pip install -e .`
In the `ext/telesurgery-qos-analysis` directory:
- `cd SurRoL-dVTrainer/`
- `pip install -e .`
- `cd ext/panda3d-kivy/`
- `pip install .`

Additionally:
- `pip install torch lz4 obs-websocket-py`
- `pip install gym==0.15.6`
- `pip install kivymd==1.1.1`
- `sudo apt install xclip`

## Building

At project root and with the ros_env conda environment acitve, run:

`colcon build`

If you run into issues, a few good steps are to:
- `rm -rf build install log`
- Close and reopen the terminal and activate the conda instance again to clear environment variables

## Launching

`source install/setup.bash`
`ros2 launch telesurgery_launch <launch_file> <arguments>`

Use TAB to search launch files.

For example, `ros2 launch telesurgery_launch replay_ros_launch.py enable_fault_injector:=true`
