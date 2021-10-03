import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

import xacro


def generate_launch_description():


    pkg_path = os.path.join(get_package_share_directory('mwe_diffdrive_bug'))




    xacro_file = os.path.join(pkg_path,'description','robot_gaz_control.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)


    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_config.toxml(), 'use_sim_time': True}]
    )


    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
            launch_arguments={
                'world': os.path.join(pkg_path, 'worlds','test_world.world')
            }.items()
            )



    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')


    return LaunchDescription([
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
    ])