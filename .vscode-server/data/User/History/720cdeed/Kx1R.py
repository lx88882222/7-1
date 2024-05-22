from setuptools import setup

package_name = 'learning'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mi',
    maintainer_email='mi@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'walktest = learning.walktest:main',
            'stand = learning.stand:main',
            'sit = learning.sit:main',
            'rgb = learning.rgb_cam_suber:main',
            'camera = learning.camera:main',
            'track = learning.track:main',
            'crash = learning.crash:main',
            'data_receive = learning.data_receive:main',
            'rotate_until_center1 = learning.rotate_until_center1',
            'walk_t_sec = learning.walk_t_sec:main',
            'goal = learning.goal:main',
            'rotate = learning.rotate:main',
            'get_data = learning.get_data:main',
            'move_x = learning.move_x:main',
            'keeper = learning.keeper:main',
            'main = learning.main_node:main'
        ],
    },
)
