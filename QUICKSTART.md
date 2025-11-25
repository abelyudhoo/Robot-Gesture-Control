# Quick Start Guide

## Instalasi Cepat

### 1. Install Dependencies
```bash
# Install Azure Kinect SDK
Download dari: https://github.com/microsoft/Azure-Kinect-Sensor-SDK/releases

# Install Body Tracking SDK  
Download dari: https://github.com/microsoft/Azure-Kinect-Body-Tracking/releases

# Install Python packages
cd robot_gesture_control
pip install -r requirements.txt
```

### 2. Konfigurasi Robot Port

Edit `config/settings.py`:
```python
ROBOT_CONFIG = {
    'port': 'COM5',  # <- GANTI INI!
    ...
}
```

Cara cek port:
- **Windows**: Device Manager → Ports (COM & LPT)
- **Linux**: `ls /dev/ttyUSB*` atau `ls /dev/ttyACM*`

### 3. Jalankan Program

```bash
python main.py
```

## Kontrol Dasar

| Gesture | Perintah |
|---------|----------|
| 🙌 Kedua tangan | MAJU |
| ✋ Tangan kanan | KANAN |
| ✋ Tangan kiri | KIRI |
| 👋 Lambaian | STOP |
| 🤚 Tangan di wajah | MUNDUR |

## Keyboard Shortcuts

- **Q** - Quit
- **C** - Connect/Disconnect robot
- **D** - Toggle gesture display
- **F** - Toggle FPS display
- **S** - Emergency STOP

## Troubleshooting Cepat

### Kinect tidak terdeteksi
```bash
# Test dengan k4aviewer
"C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4aviewer.exe"
```

### Robot tidak terhubung
1. Cek port di Device Manager
2. Update `config/settings.py`
3. Test dengan serial monitor

### Gesture tidak terdeteksi
- Jarak optimal: 1.5 - 2.5 meter
- Pastikan lighting cukup
- Hadap langsung ke kamera

## Next Steps

- Baca [README.md](README.md) untuk dokumentasi lengkap
- Lihat [GESTURES.md](docs/GESTURES.md) untuk panduan gesture
- Cek [API.md](docs/API.md) untuk referensi API
- Pelajari [ARCHITECTURE.md](docs/ARCHITECTURE.md) untuk arsitektur sistem
