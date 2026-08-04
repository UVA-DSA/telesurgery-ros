from setuptools import find_packages, setup

package_name = 'recovery'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
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
            'fault_recovery_state_machine = recovery.fault_recovery_state_machine:main',
            'autonomy_engine = recovery.autonomy_engine:main',
            'network_monitor = recovery.network_monitor:main',
            'activity_recognition = recovery.activity_recognition:main',
        ],
    },
)
