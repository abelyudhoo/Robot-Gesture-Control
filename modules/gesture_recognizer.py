"""
Gesture Recognition Module
Mendeteksi gerakan tubuh dari keypoints Azure Kinect
"""

from collections import deque
import numpy as np
import sys
sys.path.insert(1, '../../pyKinectAzure')

from config.settings import GESTURE_CONFIG, JOINT_MAP


class GestureRecognizer:
    """
    Class untuk mengenali gerakan berdasarkan keypoints tubuh
    
    Attributes:
        buffer_size (int): Ukuran buffer untuk analisis temporal
        keypoints_buffer (deque): Buffer untuk menyimpan keypoints
        gesture_history (deque): History gesture yang terdeteksi
    """
    
    def __init__(self, buffer_size=None):
        """
        Inisialisasi GestureRecognizer
        
        Args:
            buffer_size (int, optional): Ukuran buffer. Default dari config.
        """
        if buffer_size is None:
            buffer_size = GESTURE_CONFIG['buffer_size']
            
        self.buffer_size = buffer_size
        self.keypoints_buffer = deque(maxlen=buffer_size)
        self.gesture_history = deque(maxlen=30)
        
        # Load threshold dari config
        self.raise_threshold = GESTURE_CONFIG['raise_threshold']
        self.wave_threshold = GESTURE_CONFIG['wave_threshold']
        self.face_distance_threshold = GESTURE_CONFIG['face_distance_threshold']
        self.confidence_threshold = GESTURE_CONFIG['confidence_threshold']
    
    def extract_keypoints(self, body):
        """
        Ekstrak keypoints penting dari body object
        
        Args:
            body: Body object dari Azure Kinect
            
        Returns:
            dict: Dictionary berisi keypoints dengan struktur:
                  {'joint_name': {'x': float, 'y': float, 'z': float, 'confidence': int}}
        """
        joints = body.joints
        keypoints = {}
        
        for name, joint_id in JOINT_MAP.items():
            if joints[joint_id] is not None:
                pos = joints[joint_id].position
                conf = joints[joint_id].confidence_level
                keypoints[name] = {
                    'x': pos.x,
                    'y': pos.y,
                    'z': pos.z,
                    'confidence': conf
                }
            else:
                keypoints[name] = None
        
        return keypoints
    
    def is_right_hand_raised(self, keypoints):
        """
        Deteksi apakah tangan kanan terangkat
        
        Args:
            keypoints (dict): Dictionary keypoints
            
        Returns:
            bool: True jika tangan kanan terangkat
        """
        if (keypoints['right_wrist'] is None or 
            keypoints['right_shoulder'] is None or
            keypoints['nose'] is None):
            return False
        
        if keypoints['right_wrist']['confidence'] < self.confidence_threshold:
            return False
        
        wrist_y = keypoints['right_wrist']['y']
        shoulder_y = keypoints['right_shoulder']['y']
        nose_y = keypoints['nose']['y']
        
        # Tangan dianggap terangkat jika pergelangan tangan
        # lebih tinggi dari bahu dan mendekati hidung
        return (wrist_y < shoulder_y - self.raise_threshold and 
                wrist_y < nose_y + 50)
    
    def is_left_hand_raised(self, keypoints):
        """
        Deteksi apakah tangan kiri terangkat
        
        Args:
            keypoints (dict): Dictionary keypoints
            
        Returns:
            bool: True jika tangan kiri terangkat
        """
        if (keypoints['left_wrist'] is None or 
            keypoints['left_shoulder'] is None or
            keypoints['nose'] is None):
            return False
        
        if keypoints['left_wrist']['confidence'] < self.confidence_threshold:
            return False
        
        wrist_y = keypoints['left_wrist']['y']
        shoulder_y = keypoints['left_shoulder']['y']
        nose_y = keypoints['nose']['y']
        
        return (wrist_y < shoulder_y - self.raise_threshold and 
                wrist_y < nose_y + 50)
    
    def is_both_hands_raised(self, keypoints):
        """
        Deteksi apakah kedua tangan terangkat
        
        Args:
            keypoints (dict): Dictionary keypoints
            
        Returns:
            bool: True jika kedua tangan terangkat
        """
        return (self.is_right_hand_raised(keypoints) and 
                self.is_left_hand_raised(keypoints))
    
    def detect_waving(self, hand='right'):
        """
        Deteksi lambaian tangan (memerlukan data temporal)
        
        Args:
            hand (str): 'right' atau 'left'
            
        Returns:
            bool: True jika terdeteksi lambaian
        """
        if len(self.keypoints_buffer) < 10:
            return False
        
        wrist_key = f'{hand}_wrist'
        
        # Ambil posisi x pergelangan tangan dari buffer
        x_positions = []
        for kp in self.keypoints_buffer:
            if kp[wrist_key] is not None:
                x_positions.append(kp[wrist_key]['x'])
        
        if len(x_positions) < 10:
            return False
        
        # Hitung variasi posisi (standar deviasi)
        std_x = np.std(x_positions)
        
        # Deteksi perubahan arah (zero-crossing)
        differences = np.diff(x_positions)
        sign_changes = np.sum(np.diff(np.sign(differences)) != 0)
        
        # Lambaian terdeteksi jika ada variasi tinggi dan perubahan arah
        return std_x > self.wave_threshold and sign_changes >= 3
    
    def is_hand_near_face(self, keypoints, hand='right'):
        """
        Deteksi tangan di dekat wajah
        
        Args:
            keypoints (dict): Dictionary keypoints
            hand (str): 'right' atau 'left'
            
        Returns:
            bool: True jika tangan dekat wajah
        """
        wrist_key = f'{hand}_wrist'
        
        if (keypoints[wrist_key] is None or 
            keypoints['nose'] is None):
            return False
        
        wrist_pos = keypoints[wrist_key]
        nose_pos = keypoints['nose']
        
        # Hitung jarak 3D
        distance = np.sqrt(
            (wrist_pos['x'] - nose_pos['x'])**2 +
            (wrist_pos['y'] - nose_pos['y'])**2 +
            (wrist_pos['z'] - nose_pos['z'])**2
        )
        
        return distance < self.face_distance_threshold
    
    def recognize_gesture(self, body):
        """
        Fungsi utama untuk mengenali gerakan
        
        Args:
            body: Body object dari Azure Kinect
            
        Returns:
            list: List gesture yang terdeteksi
        """
        keypoints = self.extract_keypoints(body)
        
        # Simpan ke buffer untuk analisis temporal
        self.keypoints_buffer.append(keypoints)
        
        gestures = []
        
        # Prioritas deteksi (urutan penting!)
        # 1. Kedua tangan terangkat (prioritas tertinggi)
        if self.is_both_hands_raised(keypoints):
            gestures.append("KEDUA_TANGAN")
        # 2. Tangan kanan atau kiri terangkat
        elif self.is_right_hand_raised(keypoints):
            gestures.append("TANGAN_KANAN")
        elif self.is_left_hand_raised(keypoints):
            gestures.append("TANGAN_KIRI")
        
        # 3. Deteksi lambaian (STOP - prioritas tinggi)
        if self.detect_waving('right') or self.detect_waving('left'):
            gestures.append("LAMBAI")
        
        # 4. Deteksi tangan di wajah (MUNDUR)
        if (self.is_hand_near_face(keypoints, 'right') or 
            self.is_hand_near_face(keypoints, 'left')):
            gestures.append("TANGAN_DI_WAJAH")
        
        # Default: NETRAL
        if not gestures:
            gestures.append("NETRAL")
        
        # Simpan ke history
        self.gesture_history.append(gestures)
        
        return gestures
    
    def get_gesture_statistics(self):
        """
        Dapatkan statistik gesture yang terdeteksi
        
        Returns:
            dict: Dictionary berisi statistik gesture
        """
        if not self.gesture_history:
            return {}
        
        stats = {}
        total = len(self.gesture_history)
        
        # Hitung frekuensi setiap gesture
        for gestures in self.gesture_history:
            for gesture in gestures:
                if gesture not in stats:
                    stats[gesture] = 0
                stats[gesture] += 1
        
        # Konversi ke persentase
        for gesture in stats:
            stats[gesture] = (stats[gesture] / total) * 100
        
        return stats
    
    def reset(self):
        """Reset buffer dan history"""
        self.keypoints_buffer.clear()
        self.gesture_history.clear()
