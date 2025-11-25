"""
Configuration settings untuk Robot Gesture Control System
"""

# ============================================================================
# KINECT SETTINGS
# ============================================================================
KINECT_CONFIG = {
    'color_resolution': 'OFF',  # OFF, 720P, 1080P, etc.
    'depth_mode': 'WFOV_2X2BINNED',  # NFOV_UNBINNED, WFOV_2X2BINNED, etc.
}

# ============================================================================
# GESTURE RECOGNITION SETTINGS
# ============================================================================
GESTURE_CONFIG = {
    'buffer_size': 15,              # Jumlah frame untuk analisis temporal
    'raise_threshold': 100,         # mm - threshold tangan terangkat
    'wave_threshold': 80,           # mm - threshold variasi untuk lambai
    'face_distance_threshold': 200, # mm - threshold tangan di wajah
    'confidence_threshold': 1,      # Minimal confidence level (0=none, 1=low, 2=high)
}

# ============================================================================
# ROBOT CONTROLLER SETTINGS
# ============================================================================
ROBOT_CONFIG = {
    'port': 'COM5',                 # Serial port untuk robot (GANTI SESUAI SISTEM ANDA!)
    'baud_rate': 9600,              # Baud rate komunikasi
    'timeout': 1,                   # Timeout koneksi (detik)
    'command_delay': 0.5,           # Delay antar perintah (detik)
}

# ============================================================================
# GESTURE TO COMMAND MAPPING
# ============================================================================
GESTURE_COMMANDS = {
    'KEDUA_TANGAN': 'F',        # Forward/Maju
    'TANGAN_KANAN': 'R',        # Right/Kanan
    'TANGAN_KIRI': 'L',         # Left/Kiri
    'LAMBAI': 'S',              # Stop
    'TANGAN_DI_WAJAH': 'B',     # Backward/Mundur
    'NETRAL': 'S',              # Stop (default)
}

# ============================================================================
# DISPLAY SETTINGS
# ============================================================================
DISPLAY_CONFIG = {
    'window_name': 'Kontrol Robot dengan Gesture',
    'show_gestures': True,
    'fps_display': True,
}

# ============================================================================
# COLOR CODES (BGR format)
# ============================================================================
GESTURE_COLORS = {
    'KEDUA_TANGAN': (0, 255, 255),      # Kuning - MAJU
    'TANGAN_KANAN': (0, 255, 0),        # Hijau - KANAN
    'TANGAN_KIRI': (255, 0, 0),         # Biru - KIRI
    'LAMBAI': (255, 0, 255),            # Magenta - STOP
    'TANGAN_DI_WAJAH': (0, 165, 255),   # Orange - MUNDUR
    'NETRAL': (128, 128, 128),          # Abu - NETRAL
}

# ============================================================================
# COMMAND NAMES
# ============================================================================
COMMAND_NAMES = {
    'F': 'MAJU',
    'B': 'MUNDUR',
    'L': 'KIRI',
    'R': 'KANAN',
    'S': 'STOP',
}

# ============================================================================
# JOINT MAPPING (Azure Kinect Body Tracking)
# ============================================================================
JOINT_MAP = {
    'pelvis': 0,
    'spine_navel': 1,
    'spine_chest': 2,
    'neck': 3,
    'left_shoulder': 5,
    'left_elbow': 6,
    'left_wrist': 7,
    'left_hand': 8,
    'right_shoulder': 12,
    'right_elbow': 13,
    'right_wrist': 14,
    'right_hand': 15,
    'head': 26,
    'nose': 27,
}
