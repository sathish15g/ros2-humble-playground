#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import math
import numpy as np
from datetime import datetime

class CoordinateTransformer2D(Node):
    """
    Real-time 2D coordinate transformation between two robots.
    Combines both TRANSLATION and ROTATION.
    """

    def __init__(self):
        super().__init__("coordinate_transformer_2d")

        # Subscribe to both turtle poses
        self.turtle1_pose_sub_ = self.create_subscription(
            Pose, "/turtle1/pose", self.turtle1_pose_callback, 10
        )
        self.turtle2_pose_sub_ = self.create_subscription(
            Pose, "/turtle2/pose", self.turtle2_pose_callback, 10
        )

        # Store latest poses
        self.robot_a_pose = Pose()
        self.robot_b_pose = Pose()
        self.first_update = True


    def turtle1_pose_callback(self, pose):
        """Callback for Robot A pose updates"""
        self.robot_a_pose = pose


    def turtle2_pose_callback(self, pose):
        """Callback for Robot B pose updates - performs transformation"""
        self.robot_b_pose = pose

        # Perform coordinate transformation
        self.compute_transformation()


    def compute_transformation(self):
        """Compute full 2D coordinate transformation"""

        # Extract positions
        x_a, y_a = self.robot_a_pose.x, self.robot_a_pose.y
        x_b, y_b = self.robot_b_pose.x, self.robot_b_pose.y
        theta_a = self.robot_a_pose.theta
        theta_b = self.robot_b_pose.theta

        # ===== TRANSLATION =====
        tx = x_b - x_a
        ty = y_b - y_a
        distance = math.sqrt(tx**2 + ty**2)
        direction = math.degrees(math.atan2(ty, tx))

        # ===== ROTATION =====
        theta_rad = theta_b - theta_a

        # Normalize angle to [-180, 180]
        while theta_rad > math.pi:
            theta_rad -= 2 * math.pi
        while theta_rad < -math.pi:
            theta_rad += 2 * math.pi

        theta_deg = math.degrees(theta_rad)

        # ===== ROTATION MATRIX =====
        cos_theta = math.cos(theta_rad)
        sin_theta = math.sin(theta_rad)

        # ===== HOMOGENEOUS TRANSFORMATION MATRIX =====
        T_matrix = np.array([
            [cos_theta, -sin_theta, tx],
            [sin_theta,  cos_theta, ty],
            [0,          0,         1]
        ])

        # ===== DISPLAY RESULTS =====
        self.display_transformation(
            x_a, y_a, theta_a, x_b, y_b, theta_b,
            tx, ty, distance, direction,
            theta_rad, theta_deg, T_matrix
        )


    def display_transformation(self, x_a, y_a, theta_a, x_b, y_b, theta_b,
                               tx, ty, distance, direction,
                               theta_rad, theta_deg, T_matrix):
        """Pretty-print transformation results"""

        timestamp = datetime.now().strftime("%H:%M:%S")

        print("\n" + "="*75)
        print(f"║ 2D COORDINATE TRANSFORMATION | {timestamp}")
        print("="*75)

        print("\n🤖 ROBOT POSITIONS & ORIENTATIONS:")
        print(f"   Robot A (Reference):")
        print(f"     Position: ({x_a:.3f}, {y_a:.3f})")
        print(f"     Heading:  {math.degrees(theta_a):.2f}°")

        print(f"\n   Robot B (Target):")
        print(f"     Position: ({x_b:.3f}, {y_b:.3f})")
        print(f"     Heading:  {math.degrees(theta_b):.2f}°")

        print("\n📍 TRANSLATION (A → B):")
        print(f"   Tx (East-West):    {tx:+.6f} meters")
        print(f"   Ty (North-South):  {ty:+.6f} meters")
        print(f"   Distance:          {distance:.6f} meters")
        print(f"   Direction:         {direction:.2f}° from East")

        print("\n🔄 ROTATION (A → B):")
        print(f"   θ (radians):  {theta_rad:+.6f} rad")
        print(f"   θ (degrees):  {theta_deg:+.2f}°")

        print("\n📐 ROTATION MATRIX:")
        print(f"   |{T_matrix[0,0]:+.6f}  {T_matrix[0,1]:+.6f}  {T_matrix[0,2]:+.6f}|")
        print(f"   |{T_matrix[1,0]:+.6f}  {T_matrix[1,1]:+.6f}  {T_matrix[1,2]:+.6f}|")
        print(f"   |{T_matrix[2,0]:+.6f}  {T_matrix[2,1]:+.6f}  {T_matrix[2,2]:+.6f}|")

        print("\n📊 INTERPRETATION:")
        if distance < 0.1:
            print("   ✓ Robots are at SAME POSITION")
        else:
            print(f"   ✓ Robot B is {distance:.3f}m away at {direction:.1f}° bearing")

        if abs(theta_deg) < 1:
            print("   ✓ Robots have SAME ORIENTATION")
        elif abs(theta_deg) < 90:
            print(f"   ✓ Robot B is {abs(theta_deg):.1f}° rotated")
        elif abs(theta_deg) < 180:
            print(f"   ✓ Robot B is {abs(theta_deg):.1f}° rotated (significant angle)")
        else:
            print(f"   ✓ Robot B is {abs(theta_deg):.1f}° rotated (nearly opposite)")

        print("="*75 + "\n")


    def transform_point(self, point_local):
        """
        Transform a point from Robot B's local frame to Robot A's global frame.

        Args:
            point_local: tuple (x, y) in Robot B's frame

        Returns:
            tuple (x, y) in Robot A's frame
        """
        # Create homogeneous point
        point_homogeneous = np.array([
            point_local[0],
            point_local[1],
            1
        ])

        # Get transformation matrix
        tx = self.robot_b_pose.x - self.robot_a_pose.x
        ty = self.robot_b_pose.y - self.robot_a_pose.y
        theta = self.robot_b_pose.theta - self.robot_a_pose.theta

        cos_theta = math.cos(theta)
        sin_theta = math.sin(theta)

        T_matrix = np.array([
            [cos_theta, -sin_theta, tx],
            [sin_theta,  cos_theta, ty],
            [0,          0,         1]
        ])

        # Transform
        point_global = T_matrix @ point_homogeneous

        return (point_global[0], point_global[1])

def main():
    rclpy.init()

    transformer = CoordinateTransformer2D()

    print("\n" + "🚀 "*10)
    print("Starting 2D Coordinate Transformer...")
    print("Listening for /turtle1/pose and /turtle2/pose")
    print("🚀 "*10 + "\n")

    rclpy.spin(transformer)

    transformer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()