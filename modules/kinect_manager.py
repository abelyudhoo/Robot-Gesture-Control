"""
Kinect Manager Module
Mengelola Azure Kinect device dan body tracking
"""

import sys
sys.path.insert(1, '../../pyKinectAzure')
import pykinect_azure as pykinect

from config.settings import KINECT_CONFIG


class KinectManager:
    """
    Class untuk mengelola Azure Kinect device
    
    Attributes:
        device: Kinect device object
        body_tracker: Body tracker object
        is_initialized (bool): Status inisialisasi
    """
    
    def __init__(self):
        """Inisialisasi KinectManager"""
        self.device = None
        self.body_tracker = None
        self.is_initialized = False
    
    def initialize(self):
        """
        Inisialisasi Kinect device dan body tracker
        
        Returns:
            bool: True jika berhasil
        """
        try:
            print("🔧 Inisialisasi Azure Kinect libraries...")
            pykinect.initialize_libraries(track_body=True)
            print("✅ Libraries initialized")
            
            # Konfigurasi device
            device_config = pykinect.default_configuration
            
            # Set color resolution
            color_res = KINECT_CONFIG['color_resolution']
            if color_res == 'OFF':
                device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
            elif color_res == '720P':
                device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
            elif color_res == '1080P':
                device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
            
            # Set depth mode
            depth_mode = KINECT_CONFIG['depth_mode']
            if depth_mode == 'NFOV_UNBINNED':
                device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_UNBINNED
            elif depth_mode == 'WFOV_2X2BINNED':
                device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
            
            # Start device
            print("🔌 Menghubungkan ke Azure Kinect device...")
            self.device = pykinect.start_device(config=device_config)
            print("✅ Kinect device connected")
            
            # Start body tracker
            print("🏃 Memulai body tracker...")
            self.body_tracker = pykinect.start_body_tracker()
            print("✅ Body tracker started")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            print(f"❌ Error inisialisasi Kinect: {e}")
            self.is_initialized = False
            return False
    
    def get_frame(self):
        """
        Ambil frame dari Kinect
        
        Returns:
            tuple: (capture, body_frame) atau (None, None) jika gagal
        """
        if not self.is_initialized:
            return None, None
        
        try:
            capture = self.device.update()
            body_frame = self.body_tracker.update()
            return capture, body_frame
        except Exception as e:
            print(f"❌ Error mendapatkan frame: {e}")
            return None, None
    
    def get_depth_image(self, capture):
        """
        Ambil depth image dari capture
        
        Args:
            capture: Capture object dari Kinect
            
        Returns:
            tuple: (success, depth_color_image)
        """
        if capture is None:
            return False, None
        
        try:
            ret, depth_color_image = capture.get_colored_depth_image()
            return ret, depth_color_image
        except Exception as e:
            print(f"❌ Error mendapatkan depth image: {e}")
            return False, None
    
    def get_body_segmentation(self, body_frame):
        """
        Ambil body segmentation dari body frame
        
        Args:
            body_frame: Body frame object
            
        Returns:
            tuple: (success, body_image_color)
        """
        if body_frame is None:
            return False, None
        
        try:
            ret, body_image_color = body_frame.get_segmentation_image()
            return ret, body_image_color
        except Exception as e:
            print(f"❌ Error mendapatkan body segmentation: {e}")
            return False, None
    
    def get_num_bodies(self, body_frame):
        """
        Dapatkan jumlah body yang terdeteksi
        
        Args:
            body_frame: Body frame object
            
        Returns:
            int: Jumlah body terdeteksi
        """
        if body_frame is None:
            return 0
        
        try:
            return body_frame.get_num_bodies()
        except:
            return 0
    
    def get_body(self, body_frame, body_id=0):
        """
        Dapatkan body object berdasarkan ID
        
        Args:
            body_frame: Body frame object
            body_id (int): ID body yang ingin diambil
            
        Returns:
            Body object atau None
        """
        if body_frame is None:
            return None
        
        try:
            num_bodies = self.get_num_bodies(body_frame)
            if body_id < num_bodies:
                return body_frame.get_body(body_id)
        except Exception as e:
            print(f"❌ Error mendapatkan body: {e}")
        
        return None
    
    def cleanup(self):
        """Bersihkan resources Kinect"""
        print("🧹 Membersihkan Kinect resources...")
        
        try:
            if self.body_tracker:
                self.body_tracker.destroy()
        except:
            pass
        
        try:
            if self.device:
                self.device.close()
        except:
            pass
        
        self.is_initialized = False
        print("✅ Kinect resources dibersihkan")
    
    def __del__(self):
        """Destructor - pastikan cleanup dipanggil"""
        self.cleanup()
