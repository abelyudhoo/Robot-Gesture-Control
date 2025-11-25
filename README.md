# Robot Gesture Control System

Sistem kontrol robot menggunakan gesture recognition berbasis Azure Kinect Body Tracking SDK.

## 📋 Daftar Isi

- [Fitur](#fitur)
- [Persyaratan](#persyaratan)
- [Instalasi](#instalasi)
- [Konfigurasi](#konfigurasi)
- [Penggunaan](#penggunaan)
- [Struktur Project](#struktur-project)
- [Mapping Gerakan](#mapping-gerakan)
- [Troubleshooting](#troubleshooting)
- [Lisensi](#lisensi)

## ✨ Fitur

- ✅ **Deteksi Gesture Real-time** - Mengenali 5+ gerakan tubuh
- ✅ **Kontrol Robot Otomatis** - Kirim perintah ke robot via serial/Bluetooth
- ✅ **Visualisasi Interaktif** - Tampilan skeleton dan info gesture
- ✅ **Modular Architecture** - Kode terstruktur dan mudah di-maintain
- ✅ **Konfigurasi Fleksibel** - Mudah disesuaikan tanpa ubah kode
- ✅ **Multi-person Support** - Dapat mendeteksi beberapa orang (fokus pada orang pertama)

## 🔧 Persyaratan

### Hardware
- **Azure Kinect DK** - Kamera depth dengan body tracking
- **Robot** dengan koneksi serial/Bluetooth (Arduino, ESP32, dll)
- **PC/Laptop** dengan:
  - USB 3.0 port
  - Windows 10/11
  - GPU NVIDIA (recommended untuk body tracking)

### Software
- **Python 3.8+**
- **Azure Kinect SDK v1.4.1**
- **Azure Kinect Body Tracking SDK v1.1.2**
- **CUDA Toolkit 11.x** (untuk GPU acceleration)
- **cuDNN 8.x**

### Python Libraries
```
opencv-python>=4.5.0
numpy>=1.19.0
pyserial>=3.5
pykinect-azure
```

## 📦 Instalasi

### 1. Install Azure Kinect SDK

Download dan install dari:
- [Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK/releases)
- [Azure Kinect Body Tracking SDK](https://github.com/microsoft/Azure-Kinect-Body-Tracking/releases)

### 2. Install CUDA dan cuDNN (untuk GPU)

Download dari [NVIDIA Developer](https://developer.nvidia.com/):
- CUDA Toolkit 11.x
- cuDNN 8.x

### 3. Install Python Dependencies

```bash
cd robot_gesture_control
pip install -r requirements.txt
```

### 4. Install pyKinectAzure

Pastikan folder `pyKinectAzure` ada di parent directory:
```
UAS/
├── pyKinectAzure/
└── robot_gesture_control/
```

## ⚙️ Konfigurasi

Edit file `config/settings.py` untuk menyesuaikan:

### Robot Settings
```python
ROBOT_CONFIG = {
    'port': 'COM5',        # Ganti dengan port robot Anda
    'baud_rate': 9600,     # Sesuaikan dengan robot
    ...
}
```

### Gesture Threshold
```python
GESTURE_CONFIG = {
    'raise_threshold': 100,    # Sensitivitas angkat tangan (mm)
    'wave_threshold': 80,      # Sensitivitas lambaian
    ...
}
```

## 🚀 Penggunaan

### Menjalankan Program

```bash
cd robot_gesture_control
python main.py
```

### Kontrol Keyboard

| Tombol | Fungsi |
|--------|--------|
| **Q** | Keluar dari program |
| **C** | Toggle koneksi robot |
| **D** | Toggle tampilan gesture |
| **F** | Toggle tampilan FPS |
| **S** | Emergency STOP |

### Workflow

1. Program akan otomatis menghubungkan ke Kinect
2. Sistem akan mencoba connect ke robot (jika gagal, lanjut mode simulasi)
3. Berdiri di depan kamera Kinect
4. Lakukan gerakan untuk mengontrol robot
5. Lihat visualisasi gesture dan perintah robot di layar

## 📁 Struktur Project

```
robot_gesture_control/
├── main.py                      # Program utama
├── requirements.txt             # Python dependencies
├── README.md                    # Dokumentasi utama
│
├── config/                      # Konfigurasi
│   └── settings.py             # Settings untuk semua modul
│
├── modules/                     # Modul utama
│   ├── __init__.py             # Module exports
│   ├── gesture_recognizer.py  # Deteksi gesture
│   ├── robot_controller.py    # Kontrol robot
│   ├── kinect_manager.py      # Manajemen Kinect
│   └── visualizer.py          # Visualisasi
│
└── docs/                        # Dokumentasi tambahan
    ├── API.md                  # API Reference
    ├── GESTURES.md             # Panduan gesture
    └── ARCHITECTURE.md         # Arsitektur sistem
```

## 🤚 Mapping Gerakan

| Gesture | Perintah Robot | Kode |
|---------|----------------|------|
| 🙌 **Kedua Tangan Terangkat** | MAJU | F |
| ✋ **Tangan Kanan Terangkat** | BELOK KANAN | R |
| ✋ **Tangan Kiri Terangkat** | BELOK KIRI | L |
| 👋 **Lambai Tangan** | STOP | S |
| 🤚 **Tangan di Wajah** | MUNDUR | B |
| 😐 **Netral** | STOP | S |

### Prioritas Perintah

Jika beberapa gesture terdeteksi bersamaan, prioritas:
1. **LAMBAI** (STOP) - Prioritas tertinggi
2. **TANGAN_DI_WAJAH** (MUNDUR)
3. **KEDUA_TANGAN** (MAJU)
4. **TANGAN_KANAN/KIRI** (BELOK)
5. **NETRAL** (STOP)

## 🔍 Troubleshooting

### Kinect Tidak Terdeteksi

**Solusi:**
1. Pastikan Kinect terhubung ke USB 3.0 (bukan 2.0)
2. Cek di Device Manager apakah driver terinstall
3. Jalankan `k4aviewer.exe` untuk test:
   ```
   "C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4aviewer.exe"
   ```

### Robot Tidak Terhubung

**Solusi:**
1. Cek port di Device Manager (Windows)
2. Update `ROBOT_CONFIG['port']` di `config/settings.py`
3. Pastikan baud rate sesuai dengan robot
4. Test koneksi dengan serial monitor

### Error: `np.object` Deprecated

**Solusi:**
Fix file pyKinectAzure dengan Find & Replace:
- Find: `dtype=np.object`
- Replace: `dtype=object`

### Body Tracking Lambat

**Solusi:**
1. Pastikan CUDA dan cuDNN terinstall
2. Update driver GPU NVIDIA
3. Kurangi `buffer_size` di config

### Gesture Tidak Terdeteksi

**Solusi:**
1. Sesuaikan threshold di `config/settings.py`
2. Pastikan lighting cukup
3. Jarak optimal: 1.5 - 3 meter dari Kinect
4. Berdiri menghadap kamera

## 🛠️ Customization

### Menambah Gesture Baru

1. Tambahkan metode deteksi di `modules/gesture_recognizer.py`
2. Update `recognize_gesture()` untuk memanggil metode baru
3. Tambahkan mapping di `config/settings.py`:
   ```python
   GESTURE_COMMANDS['GESTURE_BARU'] = 'X'
   GESTURE_COLORS['GESTURE_BARU'] = (B, G, R)
   ```

### Mengubah Perintah Robot

Edit `GESTURE_COMMANDS` di `config/settings.py`:
```python
GESTURE_COMMANDS = {
    'KEDUA_TANGAN': 'F',  # Ubah sesuai protokol robot
    ...
}
```

## 📊 Performance

- **FPS**: 20-30 FPS (dengan GPU)
- **Latency**: < 100ms (gesture detection)
- **Akurasi**: 90%+ (kondisi ideal)

## 🤝 Kontribusi

Contributions are welcome! Please:
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 👨‍💻 Author

- **Abel Yudho**
- Email: abel.ae813@gmail.com
- GitHub: [@abelyudhoo](https://github.com/abelyudhoo)

## 🙏 Acknowledgments

- [Microsoft Azure Kinect SDK](https://github.com/microsoft/Azure-Kinect-Sensor-SDK)
- [pyKinectAzure](https://github.com/ibaiGorordo/pyKinectAzure)
- OpenCV Community



**Happy Coding! 🚀**
