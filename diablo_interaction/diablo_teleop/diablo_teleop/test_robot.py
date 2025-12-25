#!/usr/bin/env python3
import rclpy
import time
import sys
from rclpy.node import Node
from motion_msgs.msg import MotionCtrl

print("=== Diablo Robot Auto Test ===")
print("Starting automated test sequence...")
print()

class TestRobotNode(Node):
    def __init__(self):
        super().__init__('diablo_test_node')
        self.publisher_ = self.create_publisher(MotionCtrl, "diablo/MotionCmd", 2)
        self.ctrl_msgs = MotionCtrl()

    def publish_command(self, forward=None, left=None, roll=None, up=None,
                       pitch=None, mode_mark=False, height_ctrl_mode=None,
                       pitch_ctrl_mode=None, roll_ctrl_mode=None, stand_mode=None,
                       jump_mode=False, dance_mode=None, duration=1.0):
        """
        发布控制命令并保持指定时间
        """
        # 设置消息内容
        self.ctrl_msgs.mode_mark = mode_mark
        self.ctrl_msgs.mode.jump_mode = jump_mode

        if dance_mode is not None:
            self.ctrl_msgs.mode.split_mode = dance_mode
        if forward is not None:
            self.ctrl_msgs.value.forward = forward
        if left is not None:
            self.ctrl_msgs.value.left = left
        if pitch is not None:
            self.ctrl_msgs.value.pitch = pitch
        if roll is not None:
            self.ctrl_msgs.value.roll = roll
        if up is not None:
            self.ctrl_msgs.value.up = up
        if height_ctrl_mode is not None:
            self.ctrl_msgs.mode.height_ctrl_mode = height_ctrl_mode
        if pitch_ctrl_mode is not None:
            self.ctrl_msgs.mode.pitch_ctrl_mode = pitch_ctrl_mode
        if roll_ctrl_mode is not None:
            self.ctrl_msgs.mode.roll_ctrl_mode = roll_ctrl_mode
        if stand_mode is not None:
            self.ctrl_msgs.mode.stand_mode = stand_mode

        # 发布命令指定时间
        start_time = time.time()
        while time.time() - start_time < duration:
            self.publisher_.publish(self.ctrl_msgs)
            time.sleep(0.05)

    def run_test_sequence(self):
        """
        执行完整的测试序列
        """
        print("Step 1: Standing up...")
        self.publish_command(mode_mark=True, stand_mode=True, up=1.0, duration=2.0)
        print("  ✓ Standing completed")

        print("Step 2: Crouching down...")
        self.publish_command(mode_mark=True, stand_mode=False, up=-0.5, duration=1.5)
        print("  ✓ Crouching completed")

        print("Step 3: Standing up again...")
        self.publish_command(mode_mark=True, stand_mode=True, up=1.0, duration=1.5)
        print("  ✓ Standing completed")

        print("Step 4: Turning left...")
        self.publish_command(roll=0.3, duration=1.5)
        print("  ✓ Left turn completed")

        print("Step 5: Turning right...")
        self.publish_command(roll=-0.3, duration=1.5)
        print("  ✓ Right turn completed")

        print("Step 6: Moving forward 0.5 meters...")
        self.publish_command(forward=0.5, duration=2.0)
        print("  ✓ Forward movement completed")

        print("Step 7: Looking up...")
        self.publish_command(pitch=0.3, duration=1.0)
        print("  ✓ Looking up completed")

        print("Step 8: Looking down...")
        self.publish_command(pitch=-0.3, duration=1.0)
        print("  ✓ Looking down completed")

        print()
        print("=== All tests completed successfully! ===")

def main(args=None):
    rclpy.init(args=args)

    test_node = TestRobotNode()

    try:
        test_node.run_test_sequence()
    except Exception as e:
        print(f"Error during test: {e}")
    finally:
        # 停止所有运动
        test_node.ctrl_msgs.mode_mark = False
        test_node.ctrl_msgs.value.forward = 0.0
        test_node.ctrl_msgs.value.left = 0.0
        test_node.ctrl_msgs.value.roll = 0.0
        test_node.ctrl_msgs.value.pitch = 0.0
        test_node.ctrl_msgs.value.up = 0.0
        test_node.publisher_.publish(test_node.ctrl_msgs)

        test_node.destroy_node()
        rclpy.shutdown()
        print("Node shutdown completed.")

if __name__ == '__main__':
    main()
