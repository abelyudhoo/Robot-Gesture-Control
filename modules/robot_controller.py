"""
Robot Controller Module
Mengontrol robot melalui komunikasi serial/Bluetooth
"""

import serial
import serial.tools.list_ports
import time

from config.settings import ROBOT_CONFIG, GESTURE_COMMANDS


class RobotController:
    """
    Class untuk mengontrol robot via serial/Bluetooth
    
    Attributes:
        port (str): Serial port untuk koneksi
        baud_rate (int): Baud rate komunikasi
        ser (serial.Serial): Object serial connection
        connected (bool): Status koneksi
    """
    
    def __init__(self, port=None, baud_rate=None, timeout=None):
        """
        Inisialisasi RobotController
        
        Args:
            port (str, optional): Serial port. Default dari config.
            baud_rate (int, optional): Baud rate. Default dari config.
            timeout (int, optional): Timeout. Default dari config.
        """
        self.port = port or ROBOT_CONFIG['port']
        self.baud_rate = baud_rate or ROBOT_CONFIG['baud_rate']
        self.timeout = timeout or ROBOT_CONFIG['timeout']
        
        self.ser = None
        self.connected = False
        self.last_command = None
        self.last_command_time = 0
        self.command_delay = ROBOT_CONFIG['command_delay']
    
    @staticmethod
    def list_available_ports():
        """
        List semua port serial yang tersedia
        
        Returns:
            list: List port yang tersedia
        """
        ports = serial.tools.list_ports.comports()
        available_ports = []
        
        for port in ports:
            available_ports.append({
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid
            })
        
        return available_ports
    
    def connect(self):
        """
        Koneksi ke robot
        
        Returns:
            bool: True jika berhasil connect
        """
        try:
            self.ser = serial.Serial(
                self.port, 
                self.baud_rate, 
                timeout=self.timeout
            )
            self.connected = True
            print(f"✅ Terhubung ke robot di {self.port}")
            
            # Kirim perintah STOP sebagai inisialisasi
            time.sleep(0.5)  # Tunggu serial ready
            self.send_command('S')
            
            return True
        except Exception as e:
            print(f"❌ Gagal koneksi ke {self.port}: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """
        Putuskan koneksi ke robot
        """
        if self.ser and self.ser.is_open:
            # Kirim STOP sebelum disconnect
            try:
                self.send_command('S')
                time.sleep(0.2)
            except:
                pass
            
            self.ser.close()
            self.connected = False
            print("🔌 Koneksi terputus")
    
    def send_command(self, command):
        """
        Kirim perintah ke robot
        
        Args:
            command (str): Perintah yang akan dikirim (F, B, L, R, S)
            
        Returns:
            bool: True jika berhasil mengirim
        """
        if not self.connected or not self.ser or not self.ser.is_open:
            return False
        
        # Hindari spam command yang sama dalam waktu singkat
        current_time = time.time()
        if (self.last_command == command and 
            current_time - self.last_command_time < self.command_delay):
            return False
        
        try:
            self.ser.write(command.encode())
            self.last_command = command
            self.last_command_time = current_time
            return True
        except Exception as e:
            print(f"❌ Error kirim perintah: {e}")
            return False
    
    def gesture_to_command(self, gestures):
        """
        Konversi gesture ke perintah robot
        
        Args:
            gestures (list): List gesture yang terdeteksi
            
        Returns:
            str: Perintah robot (F, B, L, R, S)
        """
        # Prioritas perintah (urutan penting!)
        priority_order = [
            'LAMBAI',           # STOP (prioritas tertinggi)
            'TANGAN_DI_WAJAH',  # MUNDUR
            'KEDUA_TANGAN',     # MAJU
            'TANGAN_KANAN',     # KANAN
            'TANGAN_KIRI',      # KIRI
            'NETRAL'            # STOP (default)
        ]
        
        for gesture in priority_order:
            if gesture in gestures:
                return GESTURE_COMMANDS.get(gesture, 'S')
        
        return 'S'  # Default: STOP
    
    def send_gesture_command(self, gestures):
        """
        Konversi gesture dan kirim perintah ke robot
        
        Args:
            gestures (list): List gesture yang terdeteksi
            
        Returns:
            tuple: (command, success)
        """
        command = self.gesture_to_command(gestures)
        success = self.send_command(command)
        return command, success
    
    def emergency_stop(self):
        """
        Kirim perintah STOP darurat
        
        Returns:
            bool: True jika berhasil
        """
        if self.connected and self.ser and self.ser.is_open:
            try:
                self.ser.write(b'S')
                return True
            except:
                return False
        return False
    
    def is_connected(self):
        """
        Cek status koneksi
        
        Returns:
            bool: True jika terhubung
        """
        return self.connected and self.ser and self.ser.is_open
    
    def __del__(self):
        """Destructor - pastikan koneksi ditutup"""
        self.disconnect()
