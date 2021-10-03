from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')
    start_joy_linux = LaunchConfiguration('start_joy_linux')




    return LaunchDescription([

        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim (Gazebo) time if true'
        ),
        DeclareLaunchArgument(
            'start_joy_linux',
            default_value='false',
            description='Start the joy_linux driver'
        ),
        Node(
            package='joy_linux',
            executable='joy_linux_node',
            parameters=[{
                'dev': '/dev/input/js0',
                'autorepeat_rate': 20.0,
                'use_sim_time': use_sim_time
            }],
            condition=IfCondition(start_joy_linux)
        ),
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            parameters=[{
                'enable_button': 4,
                'enable_turbo_button': 5,
                'axis_linear.x': 1,
                'scale_linear.x': 0.7,
                'scale_linear_turbo.x': 1.5,
                'axis_angular.yaw': 0,
                'scale_angular.yaw': 1.2,
                'scale_angular_turbo.yaw': 2.4,
                'use_sim_time': use_sim_time
            }]
        ),
        Node(
            package='twist_stamper',
            executable='twist_stamper',
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=[
                ('/cmd_vel_in', '/cmd_vel'),
                ('/cmd_vel_out', '/test_controller/cmd_vel'),
            ]
        )
    ])