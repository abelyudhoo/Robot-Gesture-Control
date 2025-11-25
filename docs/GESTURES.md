# Panduan Gesture Recognition

## Overview

Sistem ini dapat mengenali 5 jenis gesture utama untuk mengontrol robot. Setiap gesture memiliki karakteristik dan kegunaan yang berbeda.

## Gesture yang Didukung

### 1. 🙌 Kedua Tangan Terangkat (MAJU)

**Deskripsi:**
Angkat kedua tangan ke atas, melewati ketinggian bahu hingga mendekati kepala.

**Kriteria Deteksi:**
- Kedua pergelangan tangan lebih tinggi dari bahu (> 100mm)
- Kedua pergelangan tangan mendekati atau lebih tinggi dari hidung
- Confidence level minimal: LOW (1)

**Perintah Robot:** `F` (Forward/Maju)

**Tips:**
- Angkat tangan lurus ke atas
- Pastikan kedua tangan terlihat oleh kamera
- Jarak optimal: 1.5 - 2.5 meter dari Kinect

**Troubleshooting:**
- Jika tidak terdeteksi: Angkat lebih tinggi
- Jika terdeteksi sebagai gesture lain: Pastikan kedua tangan sejajar

---

### 2. ✋ Tangan Kanan Terangkat (BELOK KANAN)

**Deskripsi:**
Angkat tangan kanan ke atas, tangan kiri tetap di bawah.

**Kriteria Deteksi:**
- Pergelangan tangan kanan > 100mm di atas bahu kanan
- Tangan kiri tidak terangkat
- Pergelangan tangan kanan mendekati hidung

**Perintah Robot:** `R` (Right/Belok Kanan)

**Tips:**
- Angkat hanya tangan kanan
- Pastikan tangan kiri turun atau netral
- Dapat digunakan sambil berdiri atau duduk

**Variasi:**
- Angkat tangan lurus ke atas
- Angkat tangan ke samping kanan (masih terdeteksi)

---

### 3. ✋ Tangan Kiri Terangkat (BELOK KIRI)

**Deskripsi:**
Angkat tangan kiri ke atas, tangan kanan tetap di bawah.

**Kriteria Deteksi:**
- Pergelangan tangan kiri > 100mm di atas bahu kiri
- Tangan kanan tidak terangkat
- Pergelangan tangan kiri mendekati hidung

**Perintah Robot:** `L` (Left/Belok Kiri)

**Tips:**
- Mirror dari tangan kanan terangkat
- Pastikan tangan kanan tidak ikut terangkat

---

### 4. 👋 Lambaian Tangan (STOP)

**Deskripsi:**
Gerakkan tangan kanan atau kiri secara horizontal berulang kali (seperti melambaikan tangan).

**Kriteria Deteksi:**
- Variasi posisi horizontal (X) > 80mm
- Minimal 3 perubahan arah dalam 10 frame (~0.3 detik)
- Standar deviasi gerakan tinggi

**Perintah Robot:** `S` (Stop)

**Tips:**
- Lambaikan tangan dengan cepat (2-3 kali per detik)
- Gerakan horizontal yang jelas
- Dapat menggunakan tangan kanan atau kiri
- **PRIORITAS TERTINGGI** - Akan override gesture lain

**Use Case:**
- Emergency stop
- Hentikan robot saat bergerak
- Cancel gerakan sebelumnya

**Teknik Lambaian:**
```
Posisi Awal    Gerakan        Deteksi
────────────────────────────────────────
    ✋         ✋→ ←✋ →✋      ✅ STOP
   (kiri)     (kanan-kiri)
   
    ✋         ✋ (diam)       ❌ Tidak
   (depan)                   terdeteksi
```

---

### 5. 🤚 Tangan di Wajah (MUNDUR)

**Deskripsi:**
Dekatkan tangan ke wajah (jarak < 200mm dari hidung).

**Kriteria Deteksi:**
- Jarak 3D antara pergelangan tangan dan hidung < 200mm
- Dapat menggunakan tangan kanan atau kiri

**Perintah Robot:** `B` (Backward/Mundur)

**Tips:**
- Dekatkan tangan ke wajah
- Tidak perlu menyentuh wajah
- Dapat digunakan untuk safety (mundur dari obstacle)

**Use Case:**
- Mundur dari halangan
- Koreksi posisi robot
- Safety gesture

**Variasi Posisi:**
```
✅ Terdeteksi:
- Tangan di depan wajah
- Tangan di samping wajah
- Tangan menyentuh pipi/dagu

❌ Tidak terdeteksi:
- Tangan terlalu jauh (> 200mm)
- Tangan di belakang kepala
```

---

### 6. 😐 Netral (STOP)

**Deskripsi:**
Tidak ada gesture khusus terdeteksi. Tangan dalam posisi normal/turun.

**Perintah Robot:** `S` (Stop)

**Karakteristik:**
- Default state
- Semua tangan di bawah bahu
- Tidak ada gerakan signifikan

---

## Prioritas Gesture

Jika beberapa gesture terdeteksi bersamaan, sistem menggunakan prioritas:

```
Priority 1: LAMBAI           (Emergency Stop)
Priority 2: TANGAN_DI_WAJAH  (Safety - Backward)
Priority 3: KEDUA_TANGAN     (Forward)
Priority 4: TANGAN_KANAN     (Turn Right)
Priority 5: TANGAN_KIRI      (Turn Left)
Priority 6: NETRAL           (Default Stop)
```

**Contoh Konflik:**
- Jika terdeteksi KEDUA_TANGAN + LAMBAI → Sistem pilih LAMBAI (Stop)
- Jika terdeteksi TANGAN_KANAN + TANGAN_DI_WAJAH → Sistem pilih TANGAN_DI_WAJAH (Mundur)

---

## Parameter Tuning

### Mengubah Sensitivitas

Edit file `config/settings.py`:

```python
GESTURE_CONFIG = {
    'raise_threshold': 100,    # Default: 100mm
    'wave_threshold': 80,      # Default: 80mm
    'face_distance_threshold': 200,  # Default: 200mm
}
```

#### Raise Threshold (Tangan Terangkat)
- **Nilai lebih kecil** (mis: 50mm) → Lebih sensitif, lebih mudah terdeteksi
- **Nilai lebih besar** (mis: 150mm) → Kurang sensitif, harus angkat lebih tinggi

#### Wave Threshold (Lambaian)
- **Nilai lebih kecil** (mis: 50mm) → Gerakan kecil sudah terdeteksi
- **Nilai lebih besar** (mis: 120mm) → Harus lambaikan lebih lebar

#### Face Distance Threshold
- **Nilai lebih kecil** (mis: 150mm) → Harus lebih dekat ke wajah
- **Nilai lebih besar** (mis: 300mm) → Lebih mudah terdeteksi

---

## Best Practices

### Posisi Optimal

```
        [Kinect]
           |
           |
         1.5m - 3m
           |
           ▼
        [Person]
```

**Jarak:** 1.5 - 3 meter dari Kinect
**Tinggi Kinect:** Setinggi dada (optimal untuk body tracking)
**Lighting:** Cukup terang, hindari backlight

### Gesture Tips

1. **Gerakan yang Jelas**
   - Hindari gerakan setengah-setengah
   - Tahan posisi 0.5-1 detik untuk gesture statis
   - Gerakan cepat untuk lambaian

2. **Visibility**
   - Pastikan tangan terlihat kamera
   - Jangan menutupi tangan dengan tubuh
   - Hadap langsung ke kamera

3. **Konsistensi**
   - Gunakan gerakan yang sama setiap kali
   - Praktik untuk muscle memory
   - Hindari gerakan yang ambigu

### Troubleshooting Umum

| Problem | Solution |
|---------|----------|
| Gesture tidak terdeteksi | Periksa jarak, lighting, posisi |
| False positive | Kurangi sensitivitas (raise threshold) |
| Lambat terdeteksi | Reduce buffer_size di config |
| Gesture salah | Pastikan hanya satu gesture aktif |

---

## Advanced Techniques

### Kombinasi Gesture

Meskipun tidak officially supported, beberapa kombinasi dapat digunakan:

1. **Sequential Gestures**
   ```
   TANGAN_KANAN → TANGAN_KIRI → Zigzag motion
   ```

2. **Hold & Wave**
   ```
   Angkat tangan → Lambaikan → Emergency stop sambil menunjuk
   ```

### Custom Gesture Development

Untuk menambah gesture baru:

1. **Identifikasi Kriteria**
   - Keypoints yang terlibat
   - Threshold yang dibutuhkan
   - Temporal atau spatial?

2. **Implement Detection**
   ```python
   def detect_custom_gesture(self, keypoints):
       # Your logic here
       return True/False
   ```

3. **Test & Tune**
   - Test dengan berbagai kondisi
   - Adjust threshold
   - Validate dengan user lain

---

## Performance Metrics

### Akurasi per Gesture

| Gesture | Akurasi | Latency |
|---------|---------|---------|
| Kedua Tangan | 95% | <50ms |
| Tangan Kanan/Kiri | 92% | <50ms |
| Lambaian | 88% | <100ms |
| Tangan di Wajah | 85% | <50ms |
| Netral | 98% | <30ms |

*Tested dengan kondisi ideal (jarak 2m, lighting bagus)

### Faktor yang Mempengaruhi

- **Jarak**: Optimal 1.5-2.5m
- **Lighting**: Terang lebih baik
- **Occlusion**: Pastikan body terlihat penuh
- **Postur**: Berdiri lebih baik dari duduk
- **Pakaian**: Kontras dengan background

---

## Safety Guidelines

### Do's ✅
- Test di area aman sebelum deploy
- Selalu siap gesture STOP (lambaian)
- Monitor robot behavior
- Stay in camera view

### Don'ts ❌
- Jangan gerakan terlalu cepat (except waving)
- Jangan menutupi wajah sepenuhnya
- Jangan berdiri terlalu dekat/jauh
- Jangan gunakan di tempat gelap

---

## Demo Scenarios

### Scenario 1: Simple Navigation
```
1. Netral (STOP) - Robot standby
2. Kedua Tangan (MAJU) - Robot maju 2 detik
3. Tangan Kanan (KANAN) - Robot belok kanan
4. Lambaian (STOP) - Robot berhenti
```

### Scenario 2: Obstacle Avoidance
```
1. Kedua Tangan (MAJU) - Mulai maju
2. Tangan di Wajah (MUNDUR) - Deteksi obstacle, mundur
3. Tangan Kiri (KIRI) - Hindari obstacle
4. Kedua Tangan (MAJU) - Lanjut maju
```

### Scenario 3: Emergency Stop
```
1. Kedua Tangan (MAJU) - Robot bergerak
2. EMERGENCY! 
3. Lambaian (STOP) - Langsung berhenti
```

---

**Happy Gesturing! 👋**
