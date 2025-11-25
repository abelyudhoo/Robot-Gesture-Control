# Arsitektur Sistem

## Overview

Robot Gesture Control System menggunakan arsitektur modular dengan pemisahan concerns yang jelas antara gesture detection, robot control, dan visualization.

```
┌─────────────────────────────────────────────────────────────┐
│                         MAIN.PY                             │
│                    (Orchestrator)                           │
└────────┬─────────────┬─────────────┬────────────┬──────────┘
         │             │             │            │
         ▼             ▼             ▼            ▼
┌────────────┐ ┌──────────────┐ ┌─────────┐ ┌──────────┐
│  Kinect    │ │   Gesture    │ │  Robot  │ │Visualizer│
│  Manager   │ │ Recognizer   │ │Controller│ │          │
└────────────┘ └──────────────┘ └─────────┘ └──────────┘
         │             │             │            │
         ▼             ▼             ▼            ▼
    Azure Kinect   Keypoints    Serial/BT    OpenCV
    Body Tracking  Analysis     Protocol     Display
```

## Komponen Utama

### 1. KinectManager
**Tanggung Jawab:**
- Inisialisasi Azure Kinect SDK
- Manajemen device lifecycle
- Capture frame (depth + body)
- Extract body data

**Dependencies:**
- pykinect_azure
- Azure Kinect SDK
- Body Tracking SDK

**Flow:**
```
Initialize() → Connect Device → Start Body Tracker
     ↓
Get Frame() → Update Capture → Update Body Frame
     ↓
Extract Body() → Return Body Object
```

### 2. GestureRecognizer
**Tanggung Jawab:**
- Extract keypoints dari body
- Deteksi gesture berbasis aturan
- Buffer temporal untuk analisis gerakan
- Statistik gesture

**Algoritma:**
```python
# Spatial Analysis (single frame)
is_hand_raised() → Compare wrist_y with shoulder_y

# Temporal Analysis (multi frame)
detect_waving() → Analyze position variance over time
                → Count direction changes
```

**Gesture Detection Pipeline:**
```
Body Object
    ↓
Extract Keypoints (32 joints)
    ↓
Spatial Analysis (position, distance)
    ↓
Temporal Analysis (movement, variance)
    ↓
Rule-Based Classification
    ↓
Gesture List
```

### 3. RobotController
**Tanggung Jawab:**
- Manajemen koneksi serial/Bluetooth
- Konversi gesture → command
- Command throttling (prevent spam)
- Emergency stop

**Communication Protocol:**
```
Gesture → Command Mapper → Serial Write
                              ↓
                         Robot Receives
                              ↓
                         Execute Action
```

**Command Priority:**
```
LAMBAI (S)           Priority 1 (Emergency Stop)
TANGAN_DI_WAJAH (B)  Priority 2 (Safety - Backward)
KEDUA_TANGAN (F)     Priority 3 (Forward)
TANGAN_KANAN (R)     Priority 4 (Turn)
TANGAN_KIRI (L)      Priority 5 (Turn)
NETRAL (S)           Priority 6 (Default Stop)
```

### 4. Visualizer
**Tanggung Jawab:**
- Combine depth + segmentation image
- Draw skeleton overlay
- Display gesture info
- Show robot command
- FPS monitoring

**Rendering Pipeline:**
```
Depth Image + Body Segmentation
    ↓
Alpha Blending (60% depth, 40% body)
    ↓
Draw Skeleton (from body_frame)
    ↓
Overlay Gesture Info (text boxes)
    ↓
Overlay Command Info (colored text)
    ↓
Status Bar (frame, FPS, connection)
    ↓
Display to Window
```

## Data Flow

### Frame Processing Flow
```
1. Kinect Capture
   ├─ Depth Camera → Depth Image (512x512 or 640x576)
   └─ Body Tracking → Body Frame (up to 10 bodies)

2. Data Extraction
   ├─ Depth Image → Colored Depth Image
   ├─ Body Frame → Body Segmentation Image
   └─ Body Object → 32 Joint Keypoints

3. Gesture Analysis
   ├─ Keypoints → Spatial Features
   ├─ Buffer → Temporal Features
   └─ Rules → Gesture Classification

4. Robot Control
   ├─ Gestures → Command Mapping
   ├─ Priority Check → Final Command
   └─ Throttling → Send to Robot

5. Visualization
   ├─ Images → Combined Display
   ├─ Gestures → Text Overlay
   └─ Status → Info Bar
```

### Timing Diagram
```
Frame N:
├─ t=0ms   : Kinect capture
├─ t=5ms   : Get depth + body images
├─ t=10ms  : Extract keypoints
├─ t=15ms  : Gesture recognition
├─ t=20ms  : Command generation
├─ t=22ms  : Send to robot (if not throttled)
├─ t=25ms  : Render visualization
└─ t=30ms  : Display frame (30 FPS)

Frame N+1 starts at t=33ms
```

## Configuration System

### Settings Hierarchy
```
config/settings.py
├─ KINECT_CONFIG       (Camera settings)
├─ GESTURE_CONFIG      (Detection thresholds)
├─ ROBOT_CONFIG        (Serial settings)
├─ DISPLAY_CONFIG      (UI settings)
├─ GESTURE_COMMANDS    (Gesture→Command mapping)
├─ GESTURE_COLORS      (Visualization colors)
├─ COMMAND_NAMES       (Display names)
└─ JOINT_MAP           (Kinect joint IDs)
```

### Configuration Loading
```python
# All modules import from config.settings
from config.settings import ROBOT_CONFIG, GESTURE_CONFIG

# Easy to modify without changing code
ROBOT_CONFIG['port'] = 'COM7'  # Change robot port
GESTURE_CONFIG['raise_threshold'] = 150  # More sensitive
```

## Error Handling

### Hierarchical Error Handling
```
Level 1: Module Level
├─ Try-catch in each method
├─ Return None/False on error
└─ Log error message

Level 2: Manager Level (main.py)
├─ Check return values
├─ Graceful degradation
└─ User notification

Level 3: Application Level
├─ Cleanup on exception
├─ Resource deallocation
└─ Safe shutdown
```

### Graceful Degradation
```
Kinect Error → Exit (cannot continue)
Robot Error → Continue in simulation mode
Gesture Error → Skip frame, continue
Visual Error → Continue without visualization
```

## Performance Optimization

### Bottlenecks & Solutions

1. **Body Tracking (GPU)**
   - Problem: CPU-only is slow (5-10 FPS)
   - Solution: Use CUDA + GPU (25-30 FPS)

2. **Serial Communication**
   - Problem: Blocking I/O
   - Solution: Timeout + throttling

3. **Frame Buffer**
   - Problem: Memory for temporal analysis
   - Solution: Circular buffer (deque) with max size

4. **Image Rendering**
   - Problem: Multiple image operations
   - Solution: In-place operations, minimal copies

### Memory Management
```
Circular Buffers:
├─ keypoints_buffer: maxlen=15 (current config)
├─ gesture_history: maxlen=30
└─ Automatic old data removal

Resources:
├─ Kinect: Explicit cleanup in __del__
├─ Serial: Close on disconnect
└─ OpenCV: destroyAllWindows()
```

## Extensibility

### Adding New Gestures

1. **Create Detection Method**
```python
# In gesture_recognizer.py
def detect_thumbs_up(self, keypoints):
    # Your detection logic
    return True/False
```

2. **Add to Recognition Pipeline**
```python
def recognize_gesture(self, body):
    # ... existing code ...
    if self.detect_thumbs_up(keypoints):
        gestures.append("THUMBS_UP")
```

3. **Add Configuration**
```python
# In config/settings.py
GESTURE_COMMANDS['THUMBS_UP'] = 'X'
GESTURE_COLORS['THUMBS_UP'] = (0, 255, 128)
```

### Custom Robot Protocol

1. **Extend RobotController**
```python
class CustomRobotController(RobotController):
    def send_command(self, command):
        # Custom protocol
        packet = f"<{command}>\n"
        self.ser.write(packet.encode())
```

2. **Use in main.py**
```python
robot = CustomRobotController()
```

## Testing Strategy

### Unit Testing
```python
# Test gesture detection
def test_hand_raised():
    recognizer = GestureRecognizer()
    mock_keypoints = {...}
    assert recognizer.is_right_hand_raised(mock_keypoints)
```

### Integration Testing
```python
# Test full pipeline
def test_gesture_to_command():
    robot = RobotController()
    gestures = ['KEDUA_TANGAN']
    cmd = robot.gesture_to_command(gestures)
    assert cmd == 'F'
```

### Hardware Testing
- Kinect availability check
- Robot connection validation
- Port detection

## Security Considerations

1. **Serial Communication**
   - Validate commands before sending
   - Timeout protection
   - Emergency stop available

2. **Input Validation**
   - Check keypoints confidence
   - Validate frame data
   - Boundary checks

3. **Resource Protection**
   - Proper cleanup on exit
   - Exception handling
   - Memory limits (circular buffers)

## Future Improvements

### Potential Enhancements
1. **Machine Learning**
   - Replace rule-based with ML classifier
   - Training data collection
   - Better accuracy

2. **Multi-Person Support**
   - Track multiple people
   - Gesture fusion
   - Person identification

3. **Network Communication**
   - WiFi/Ethernet robot control
   - Web interface
   - Remote monitoring

4. **Data Logging**
   - Save gesture sequences
   - Performance metrics
   - Debugging info

5. **Real-time Tuning**
   - GUI for threshold adjustment
   - Live configuration
   - A/B testing gestures
