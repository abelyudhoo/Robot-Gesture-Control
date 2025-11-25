"""
Visualizer Module
Menampilkan visualisasi untuk gesture recognition
"""

import cv2
import time

from config.settings import (
    DISPLAY_CONFIG, 
    GESTURE_COLORS, 
    COMMAND_NAMES
)


class Visualizer:
    """
    Class untuk visualisasi gesture recognition
    
    Attributes:
        window_name (str): Nama window OpenCV
        show_gestures (bool): Toggle tampilan gesture
        fps_display (bool): Toggle tampilan FPS
    """
    
    def __init__(self, window_name=None):
        """
        Inisialisasi Visualizer
        
        Args:
            window_name (str, optional): Nama window. Default dari config.
        """
        self.window_name = window_name or DISPLAY_CONFIG['window_name']
        self.show_gestures = DISPLAY_CONFIG['show_gestures']
        self.fps_display = DISPLAY_CONFIG['fps_display']
        
        # FPS calculation
        self.fps = 0
        self.fps_counter = 0
        self.fps_start_time = time.time()
        
        # Create window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
    
    def update_fps(self):
        """Update perhitungan FPS"""
        self.fps_counter += 1
        
        if self.fps_counter >= 30:
            elapsed = time.time() - self.fps_start_time
            self.fps = 30 / elapsed if elapsed > 0 else 0
            self.fps_counter = 0
            self.fps_start_time = time.time()
    
    def combine_images(self, depth_image, body_image, alpha=0.6, beta=0.4):
        """
        Gabungkan depth image dengan body segmentation
        
        Args:
            depth_image: Depth color image
            body_image: Body segmentation image
            alpha (float): Weight untuk depth image
            beta (float): Weight untuk body image
            
        Returns:
            Combined image
        """
        if depth_image is None or body_image is None:
            return depth_image if depth_image is not None else body_image
        
        try:
            return cv2.addWeighted(depth_image, alpha, body_image, beta, 0)
        except:
            return depth_image
    
    def draw_gestures(self, image, gestures, body_id=0):
        """
        Gambar info gesture di image
        
        Args:
            image: Image untuk digambar
            gestures (list): List gesture yang terdeteksi
            body_id (int): ID body
            
        Returns:
            Image dengan gesture info
        """
        if not self.show_gestures or image is None:
            return image
        
        y_offset = 60 + (body_id * 120)
        
        # Background box untuk readability
        box_height = len(gestures) * 25 + 30
        cv2.rectangle(
            image,
            (10, y_offset - 25),
            (400, y_offset + box_height),
            (0, 0, 0),
            -1
        )
        
        # Body ID header
        cv2.putText(
            image,
            f"Body {body_id}:",
            (15, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )
        
        # Display setiap gesture
        for i, gesture in enumerate(gestures):
            color = GESTURE_COLORS.get(gesture, (255, 255, 255))
            cv2.putText(
                image,
                f"  - {gesture}",
                (15, y_offset + 25 + (i * 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )
        
        return image
    
    def draw_robot_command(self, image, command, connected, gestures=None):
        """
        Gambar info perintah robot
        
        Args:
            image: Image untuk digambar
            command (str): Perintah robot (F, B, L, R, S)
            connected (bool): Status koneksi robot
            gestures (list, optional): List gesture untuk positioning
            
        Returns:
            Image dengan command info
        """
        if image is None:
            return image
        
        # Hitung posisi berdasarkan jumlah gesture
        num_gestures = len(gestures) if gestures else 1
        cmd_offset = 60 + (num_gestures * 30) + 20
        
        cmd_name = COMMAND_NAMES.get(command, "UNKNOWN")
        cmd_color = (0, 255, 0) if connected else (0, 0, 255)
        
        # Background box
        cv2.rectangle(
            image,
            (10, cmd_offset - 10),
            (400, cmd_offset + 30),
            (0, 0, 0),
            -1
        )
        
        # Command text
        cv2.putText(
            image,
            f"PERINTAH: {cmd_name} ({command})",
            (15, cmd_offset + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            cmd_color,
            2
        )
        
        return image
    
    def draw_status(self, image, frame_number, connected):
        """
        Gambar status bar
        
        Args:
            image: Image untuk digambar
            frame_number (int): Nomor frame
            connected (bool): Status koneksi robot
            
        Returns:
            Image dengan status bar
        """
        if image is None:
            return image
        
        status_color = (0, 255, 0) if connected else (0, 0, 255)
        status_text = "TERHUBUNG" if connected else "TERPUTUS"
        
        info_parts = [f"Frame: {frame_number}", f"Robot: {status_text}"]
        
        if self.fps_display:
            info_parts.insert(1, f"FPS: {self.fps:.1f}")
        
        info_text = " | ".join(info_parts)
        
        # Background box
        cv2.rectangle(
            image,
            (5, 5),
            (len(info_text) * 11, 45),
            (0, 0, 0),
            -1
        )
        
        # Status text
        cv2.putText(
            image, 
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status_color,
            2
        )
        
        return image
    
    def show(self, image):
        """
        Tampilkan image
        
        Args:
            image: Image untuk ditampilkan
        """
        if image is not None:
            cv2.imshow(self.window_name, image)
    
    def wait_key(self, delay=1):
        """
        Tunggu input keyboard
        
        Args:
            delay (int): Delay dalam ms
            
        Returns:
            int: Key code yang ditekan
        """
        return cv2.waitKey(delay)
    
    def toggle_gestures(self):
        """Toggle tampilan gesture"""
        self.show_gestures = not self.show_gestures
        return self.show_gestures
    
    def toggle_fps(self):
        """Toggle tampilan FPS"""
        self.fps_display = not self.fps_display
        return self.fps_display
    
    def cleanup(self):
        """Tutup semua window"""
        cv2.destroyAllWindows()
    
    def __del__(self):
        """Destructor - pastikan window ditutup"""
        self.cleanup()
