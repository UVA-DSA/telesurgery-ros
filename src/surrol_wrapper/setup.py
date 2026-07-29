import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'surrol_wrapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    include_package_data=True,
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'param'), glob('param/*')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    ],
    package_data={'': ['py.typed'],
                  'dVTrainer': ['*.txt']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Aidan Liu',
    maintainer_email='aidan2023liu@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'surrol_wrapper = surrol_wrapper.surrol_wrapper:main'
        ],
    },
)
