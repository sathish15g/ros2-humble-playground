#!/usr/bin/env python3

import numpy as np
import math
from datetime import datetime

class Drone3D:
    """Represents a 3D drone with position and orientation"""

    def __init__(self, name, x=0, y=0, z=0, roll=0, pitch=0, yaw=0):
        """
        Initialize a 3D drone

        Args:
            name: Drone name
            x, y, z: Position in 3D space
            roll, pitch, yaw: Euler angles in radians
        """
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.roll = roll      # φ (phi) - rotation around X-axis
        self.pitch = pitch    # θ (theta) - rotation around Y-axis
        self.yaw = yaw        # ψ (psi) - rotation around Z-axis


    def get_rotation_matrix_x(self, angle):
        """Rotation matrix around X-axis (Roll)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return np.array([
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ])


    def get_rotation_matrix_y(self, angle):
        """Rotation matrix around Y-axis (Pitch)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return np.array([
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ])


    def get_rotation_matrix_z(self, angle):
        """Rotation matrix around Z-axis (Yaw)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return np.array([
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ])


    def get_rotation_matrix_3d(self):
        """
        Get combined 3D rotation matrix (ZYX order)
        R_total = Rz(yaw) × Ry(pitch) × Rx(roll)
        """
        Rx = self.get_rotation_matrix_x(self.roll)
        Ry = self.get_rotation_matrix_y(self.pitch)
        Rz = self.get_rotation_matrix_z(self.yaw)

        return Rz @ Ry @ Rx


    def get_transformation_matrix_4x4(self):
        """Get 4×4 homogeneous transformation matrix"""
        R = self.get_rotation_matrix_3d()

        T = np.eye(4)
        T[0:3, 0:3] = R
        T[0, 3] = self.x
        T[1, 3] = self.y
        T[2, 3] = self.z

        return T

class CoordinateTransformer3D:
    """Transforms coordinates between two 3D drones"""

    def __init__(self, drone_a, drone_b):
        """
        Initialize transformer

        Args:
            drone_a: Reference drone (origin of transformation)
            drone_b: Target drone (subject of transformation)
        """
        self.drone_a = drone_a
        self.drone_b = drone_b


    def compute_transformation(self):
        """Compute 3D coordinate transformation"""

        # Translation
        tx = self.drone_b.x - self.drone_a.x
        ty = self.drone_b.y - self.drone_a.y
        tz = self.drone_b.z - self.drone_a.z
        distance_3d = math.sqrt(tx**2 + ty**2 + tz**2)

        # Rotation (Euler angles)
        delta_roll = self.drone_b.roll - self.drone_a.roll
        delta_pitch = self.drone_b.pitch - self.drone_a.pitch
        delta_yaw = self.drone_b.yaw - self.drone_a.yaw

        # Normalize angles to [-π, π]
        delta_roll = self.normalize_angle(delta_roll)
        delta_pitch = self.normalize_angle(delta_pitch)
        delta_yaw = self.normalize_angle(delta_yaw)

        # Create temporary drone for relative rotation
        delta_drone = Drone3D(
            "delta",
            0, 0, 0,
            delta_roll, delta_pitch, delta_yaw
        )

        R_matrix = delta_drone.get_rotation_matrix_3d()

        # Create transformation matrix
        T_matrix = np.eye(4)
        T_matrix[0:3, 0:3] = R_matrix
        T_matrix[0, 3] = tx
        T_matrix[1, 3] = ty
        T_matrix[2, 3] = tz

        return {
            'translation': (tx, ty, tz),
            'distance_3d': distance_3d,
            'rotation_euler': (delta_roll, delta_pitch, delta_yaw),
            'rotation_matrix': R_matrix,
            'transformation_matrix': T_matrix
        }


    @staticmethod
    def normalize_angle(angle):
        """Normalize angle to [-π, π]"""
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle


    def display_transformation(self):
        """Pretty-print 3D transformation"""
        result = self.compute_transformation()

        tx, ty, tz = result['translation']
        distance = result['distance_3d']
        roll_deg, pitch_deg, yaw_deg = [
            math.degrees(a) for a in result['rotation_euler']
        ]
        R = result['rotation_matrix']
        T = result['transformation_matrix']

        timestamp = datetime.now().strftime("%H:%M:%S")

        print("\n" + "="*80)
        print(f"║ 3D COORDINATE TRANSFORMATION | {timestamp}")
        print("="*80)

        print("\n🚁 DRONE POSITIONS & ORIENTATIONS:")
        print(f"\n   {self.drone_a.name} (Reference):")
        print(f"     Position:    ({self.drone_a.x:.3f}, {self.drone_a.y:.3f}, {self.drone_a.z:.3f})")
        print(f"     Roll:  {math.degrees(self.drone_a.roll):+.2f}°  "
              f"Pitch: {math.degrees(self.drone_a.pitch):+.2f}°  "
              f"Yaw: {math.degrees(self.drone_a.yaw):+.2f}°")

        print(f"\n   {self.drone_b.name} (Target):")
        print(f"     Position:    ({self.drone_b.x:.3f}, {self.drone_b.y:.3f}, {self.drone_b.z:.3f})")
        print(f"     Roll:  {math.degrees(self.drone_b.roll):+.2f}°  "
              f"Pitch: {math.degrees(self.drone_b.pitch):+.2f}°  "
              f"Yaw: {math.degrees(self.drone_b.yaw):+.2f}°")

        print("\n📍 TRANSLATION:")
        print(f"   Tx (East-West):    {tx:+.6f} meters")
        print(f"   Ty (North-South):  {ty:+.6f} meters")
        print(f"   Tz (Up-Down):      {tz:+.6f} meters")
        print(f"   3D Distance:       {distance:.6f} meters")

        print("\n🔄 ROTATION (Euler Angles):")
        print(f"   Roll (φ) around X-axis:   {roll_deg:+.2f}°")
        print(f"   Pitch (θ) around Y-axis:  {pitch_deg:+.2f}°")
        print(f"   Yaw (ψ) around Z-axis:    {yaw_deg:+.2f}°")

        print("\n📐 3×3 ROTATION MATRIX:")
        for row in R:
            print(f"   |{row[0]:+.6f}  {row[1]:+.6f}  {row[2]:+.6f}|")

        print("\n📐 4×4 TRANSFORMATION MATRIX (Homogeneous):")
        for row in T:
            print(f"   |{row[0]:+.6f}  {row[1]:+.6f}  {row[2]:+.6f}  {row[3]:+.6f}|")

        print("\n📊 INTERPRETATION:")
        if distance < 0.1:
            print("   ✓ Drones are at SAME LOCATION")
        else:
            print(f"   ✓ Drone B is {distance:.3f}m away in 3D space")

        print("="*80 + "\n")


    def transform_point_3d(self, point_local):
        """
        Transform a 3D point from Drone B's frame to Drone A's frame

        Args:
            point_local: tuple (x, y, z) in Drone B's frame

        Returns:
            tuple (x, y, z) in Drone A's frame
        """
        result = self.compute_transformation()
        T = result['transformation_matrix']

        point_homo = np.array([point_local[0], point_local[1], point_local[2], 1])
        point_global = T @ point_homo

        return (point_global[0], point_global[1], point_global[2])

# ============ EXAMPLE USAGE ============

if __name__ == '__main__':

    print("\n" + "🚁 "*15)
    print("3D DRONE COORDINATE TRANSFORMATION DEMO")
    print("🚁 "*15 + "\n")

    # ===== TIME: t=0 seconds =====
    print("\n" + "⏱️  "*20)
    print("TIME: t = 0 seconds")
    print("⏱️  "*20)

    drone_a = Drone3D(
        "Drone-A",
        x=0, y=0, z=0,
        roll=0, pitch=0, yaw=0
    )

    drone_b = Drone3D(
        "Drone-B",
        x=3, y=4, z=5,
        roll=math.radians(10),
        pitch=math.radians(20),
        yaw=math.radians(45)
    )

    transformer = CoordinateTransformer3D(drone_a, drone_b)
    transformer.display_transformation()

    # Example: Transform a point
    point_in_b = (1, 0, 0)  # Forward in Drone B's frame
    point_in_a = transformer.transform_point_3d(point_in_b)
    print(f"Point {point_in_b} in Drone-B frame → {point_in_a} in Drone-A frame\n")

    # ===== TIME: t=5 seconds =====
    print("\n" + "⏱️  "*20)
    print("TIME: t = 5 seconds (Drones moving & rotating!)")
    print("⏱️  "*20)

    drone_a.x = 2
    drone_a.y = 1
    drone_a.z = 0.5
    drone_a.yaw = math.radians(30)

    drone_b.x = 7
    drone_b.y = 6
    drone_b.z = 8
    drone_b.roll = math.radians(15)
    drone_b.pitch = math.radians(30)
    drone_b.yaw = math.radians(120)

    transformer.display_transformation()

    # ===== TIME: t=10 seconds =====
    print("\n" + "⏱️  "*20)
    print("TIME: t = 10 seconds (Drones further apart!)")
    print("⏱️  "*20)

    drone_a.z = 2
    drone_b.z = 12
    drone_b.pitch = math.radians(45)

    transformer.display_transformation()

    print("\n✓ 3D Transformation Demo Complete!\n")