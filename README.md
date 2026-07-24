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

First update all git submodules: 
- `git submodule update --init`
- `cd ext/pybullet-rendering`
- `git submodule update --init` (again)

Next, update pybind11 within pybullet-rendering:
- `cd src/deps/pybind11`
- `git checkout v2.13.6`

Then install. First go to the bullet3 instance provided by telesurgery-qos-analysis:

- `cd ../../../../`
- `cd telesurgery-qos-analysis/SurRoL_dVTrainer/ext/bullet3` (go to the bullet3 that's given in telesurgery-qos-analysis)
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













