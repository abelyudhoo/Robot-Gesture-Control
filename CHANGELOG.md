# Changelog

All notable changes to Robot Gesture Control System will be documented in this file.

## [1.0.0] - 2025-11-25

### Added
- ✨ Initial release
- 🎯 Gesture recognition dengan 5 gesture utama
- 🤖 Robot control via serial/Bluetooth
- 📺 Real-time visualization dengan OpenCV
- 🏗️ Modular architecture (4 modul utama)
- ⚙️ Configuration system yang fleksibel
- 📊 FPS monitoring
- 🔧 Emergency stop feature
- 📝 Comprehensive documentation
  - README.md
  - API.md
  - ARCHITECTURE.md
  - GESTURES.md
  - CHANGELOG.md

### Features
- Gesture Detection:
  - Kedua tangan terangkat (Forward)
  - Tangan kanan terangkat (Right)
  - Tangan kiri terangkat (Left)
  - Lambaian tangan (Stop)
  - Tangan di wajah (Backward)

- Robot Control:
  - Serial communication support
  - Command throttling
  - Priority-based gesture mapping
  - Emergency stop

- Visualization:
  - Skeleton overlay
  - Gesture info display
  - Robot command display
  - Status bar with FPS

- Configuration:
  - Kinect settings
  - Gesture thresholds
  - Robot connection
  - Display preferences

### Modules
- `gesture_recognizer.py` - Deteksi gesture dari keypoints
- `robot_controller.py` - Kontrol robot via serial
- `kinect_manager.py` - Manajemen Azure Kinect
- `visualizer.py` - Visualisasi real-time

### Documentation
- Complete API reference
- Architecture overview
- Gesture usage guide
- Installation instructions
- Troubleshooting guide

---

## Future Plans

### [1.1.0] - Planned
- [ ] Machine learning-based gesture recognition
- [ ] Multi-person support
- [ ] Gesture recording & playback
- [ ] Web interface for monitoring
- [ ] Data logging to CSV/JSON
- [ ] Configuration GUI
- [ ] Unit tests
- [ ] CI/CD pipeline

### [1.2.0] - Planned
- [ ] WiFi/Network robot control
- [ ] Custom gesture builder
- [ ] Voice command integration
- [ ] Mobile app controller
- [ ] Gesture analytics dashboard
- [ ] Performance profiling tools

---

## Version History

- **1.0.0** (2025-11-25) - Initial modular release
