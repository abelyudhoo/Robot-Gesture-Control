# API Reference

## Modules

### GestureRecognizer

Class untuk mengenali gerakan dari keypoints tubuh.

#### Initialization

```python
from modules import GestureRecognizer

recognizer = GestureRecognizer(buffer_size=15)
```

**Parameters:**
- `buffer_size` (int, optional): Ukuran buffer untuk analisis temporal. Default: 15

#### Methods

##### `recognize_gesture(body)`

Mengenali gesture dari body object.

**Parameters:**
- `body`: Body object dari Azure Kinect

**Returns:**
- `list`: List gesture yang terdeteksi

**Example:**
```python
gestures = recognizer.recognize_gesture(body)
# Output: ['TANGAN_KANAN']
```

##### `extract_keypoints(body)`

Ekstrak keypoints dari body.

**Returns:**
- `dict`: Dictionary keypoints dengan format:
  ```python
  {
      'joint_name': {
          'x': float,
          'y': float,
          'z': float,
          'confidence': int
      }
  }
  ```

##### `get_gesture_statistics()`

Dapatkan statistik gesture yang terdeteksi.

**Returns:**
- `dict`: Dictionary berisi persentase setiap gesture

---

### RobotController

Class untuk mengontrol robot via serial.

#### Initialization

```python
from modules import RobotController

robot = RobotController(port='COM5', baud_rate=9600)
```

**Parameters:**
- `port` (str, optional): Serial port. Default dari config
- `baud_rate` (int, optional): Baud rate. Default dari config
- `timeout` (int, optional): Timeout koneksi. Default dari config

#### Methods

##### `connect()`

Koneksi ke robot.

**Returns:**
- `bool`: True jika berhasil

**Example:**
```python
if robot.connect():
    print("Robot terhubung!")
```

##### `send_command(command)`

Kirim perintah ke robot.

**Parameters:**
- `command` (str): Perintah (F, B, L, R, S)

**Returns:**
- `bool`: True jika berhasil

##### `gesture_to_command(gestures)`

Konversi gesture ke perintah robot.

**Parameters:**
- `gestures` (list): List gesture

**Returns:**
- `str`: Perintah robot

**Example:**
```python
cmd = robot.gesture_to_command(['KEDUA_TANGAN'])
# Output: 'F'
```

##### `send_gesture_command(gestures)`

Konversi dan kirim perintah dalam satu fungsi.

**Parameters:**
- `gestures` (list): List gesture

**Returns:**
- `tuple`: (command, success)

##### `emergency_stop()`

Kirim perintah STOP darurat.

**Returns:**
- `bool`: True jika berhasil

##### `list_available_ports()` (static)

List semua port serial tersedia.

**Returns:**
- `list`: List dict dengan info port

**Example:**
```python
ports = RobotController.list_available_ports()
for port in ports:
    print(f"{port['device']}: {port['description']}")
```

---

### KinectManager

Class untuk mengelola Azure Kinect device.

#### Initialization

```python
from modules import KinectManager

kinect = KinectManager()
```

#### Methods

##### `initialize()`

Inisialisasi Kinect dan body tracker.

**Returns:**
- `bool`: True jika berhasil

##### `get_frame()`

Ambil frame dari Kinect.

**Returns:**
- `tuple`: (capture, body_frame)

##### `get_depth_image(capture)`

Ambil depth image.

**Parameters:**
- `capture`: Capture object

**Returns:**
- `tuple`: (success, depth_image)

##### `get_body_segmentation(body_frame)`

Ambil body segmentation image.

**Parameters:**
- `body_frame`: Body frame object

**Returns:**
- `tuple`: (success, body_image)

##### `get_num_bodies(body_frame)`

Dapatkan jumlah body terdeteksi.

**Returns:**
- `int`: Jumlah body

##### `get_body(body_frame, body_id=0)`

Dapatkan body object berdasarkan ID.

**Parameters:**
- `body_frame`: Body frame object
- `body_id` (int): ID body (default: 0)

**Returns:**
- Body object atau None

##### `cleanup()`

Bersihkan resources Kinect.

---

### Visualizer

Class untuk visualisasi gesture recognition.

#### Initialization

```python
from modules import Visualizer

viz = Visualizer(window_name='My Window')
```

**Parameters:**
- `window_name` (str, optional): Nama window. Default dari config

#### Methods

##### `combine_images(depth_image, body_image, alpha=0.6, beta=0.4)`

Gabungkan depth dan body image.

**Parameters:**
- `depth_image`: Depth color image
- `body_image`: Body segmentation image
- `alpha` (float): Weight depth image
- `beta` (float): Weight body image

**Returns:**
- Combined image

##### `draw_gestures(image, gestures, body_id=0)`

Gambar info gesture di image.

**Parameters:**
- `image`: Image untuk digambar
- `gestures` (list): List gesture
- `body_id` (int): ID body

**Returns:**
- Image dengan gesture info

##### `draw_robot_command(image, command, connected, gestures=None)`

Gambar info perintah robot.

**Parameters:**
- `image`: Image
- `command` (str): Perintah robot
- `connected` (bool): Status koneksi
- `gestures` (list, optional): List gesture

**Returns:**
- Image dengan command info

##### `draw_status(image, frame_number, connected)`

Gambar status bar.

**Parameters:**
- `image`: Image
- `frame_number` (int): Nomor frame
- `connected` (bool): Status koneksi

**Returns:**
- Image dengan status bar

##### `show(image)`

Tampilkan image.

##### `wait_key(delay=1)`

Tunggu input keyboard.

**Parameters:**
- `delay` (int): Delay dalam ms

**Returns:**
- `int`: Key code

##### `toggle_gestures()`

Toggle tampilan gesture.

**Returns:**
- `bool`: Status baru

##### `update_fps()`

Update perhitungan FPS.

---

## Configuration

### Mengakses Config

```python
from config.settings import (
    KINECT_CONFIG,
    GESTURE_CONFIG,
    ROBOT_CONFIG,
    GESTURE_COMMANDS,
    GESTURE_COLORS,
    COMMAND_NAMES,
    JOINT_MAP
)
```

### Config Structure

#### KINECT_CONFIG
```python
{
    'color_resolution': str,
    'depth_mode': str
}
```

#### GESTURE_CONFIG
```python
{
    'buffer_size': int,
    'raise_threshold': int,
    'wave_threshold': int,
    'face_distance_threshold': int,
    'confidence_threshold': int
}
```

#### ROBOT_CONFIG
```python
{
    'port': str,
    'baud_rate': int,
    'timeout': int,
    'command_delay': float
}
```

---

## Examples

### Basic Usage

```python
from modules import (
    GestureRecognizer,
    RobotController,
    KinectManager,
    Visualizer
)

# Initialize
kinect = KinectManager()
kinect.initialize()

robot = RobotController()
robot.connect()

recognizer = GestureRecognizer()
viz = Visualizer()

# Main loop
while True:
    # Get frame
    capture, body_frame = kinect.get_frame()
    
    # Get images
    _, depth_img = kinect.get_depth_image(capture)
    _, body_img = kinect.get_body_segmentation(body_frame)
    
    # Combine
    img = viz.combine_images(depth_img, body_img)
    
    # Recognize gesture
    body = kinect.get_body(body_frame, 0)
    if body:
        gestures = recognizer.recognize_gesture(body)
        cmd, _ = robot.send_gesture_command(gestures)
        
        # Visualize
        img = viz.draw_gestures(img, gestures)
        img = viz.draw_robot_command(img, cmd, robot.is_connected())
    
    # Show
    viz.show(img)
    
    if viz.wait_key(1) == ord('q'):
        break

# Cleanup
robot.disconnect()
kinect.cleanup()
viz.cleanup()
```

### Custom Gesture Detection

```python
class CustomGestureRecognizer(GestureRecognizer):
    def detect_jump(self, keypoints):
        """Deteksi lompat"""
        if keypoints['pelvis'] and keypoints['pelvis']['y'] < -200:
            return True
        return False
    
    def recognize_gesture(self, body):
        gestures = super().recognize_gesture(body)
        keypoints = self.extract_keypoints(body)
        
        if self.detect_jump(keypoints):
            gestures.append('JUMP')
        
        return gestures
```

### Port Detection

```python
from modules import RobotController

# List available ports
ports = RobotController.list_available_ports()

print("Available ports:")
for port in ports:
    print(f"  {port['device']}: {port['description']}")

# Use first available
if ports:
    robot = RobotController(port=ports[0]['device'])
```
