"""
Robot Gesture Control System - Main Program
Sistem kontrol robot menggunakan gesture recognition dari Azure Kinect

Author: [Your Name]
Date: November 2025
Version: 1.0
"""

import sys
import time

from modules import (
    GestureRecognizer,
    RobotController,
    KinectManager,
    Visualizer
)
from config.settings import COMMAND_NAMES


def print_header():
    """Cetak header program"""
    print("=" * 70)
    print("🤖 SISTEM KONTROL ROBOT DENGAN GESTURE RECOGNITION")
    print("=" * 70)
    print()
    print("📋 Mapping Gerakan:")
    print("  - Kedua Tangan Terangkat  → MAJU (F)")
    print("  - Tangan Kanan Terangkat  → BELOK KANAN (R)")
    print("  - Tangan Kiri Terangkat   → BELOK KIRI (L)")
    print("  - Lambai Tangan           → STOP (S)")
    print("  - Tangan di Wajah         → MUNDUR (B)")
    print("=" * 70)
    print()


def print_controls():
    """Cetak kontrol keyboard"""
    print("🎮 Kontrol Keyboard:")
    print("  Q - Keluar dari program")
    print("  C - Toggle koneksi robot (connect/disconnect)")
    print("  D - Toggle tampilan gesture info")
    print("  F - Toggle tampilan FPS")
    print("  S - Emergency STOP")
    print()


def main():
    """Fungsi utama program"""
    
    # Print info program
    print_header()
    
    # Inisialisasi semua modul
    print("🔧 Inisialisasi sistem...")
    print()
    
    # 1. Kinect Manager
    kinect = KinectManager()
    if not kinect.initialize():
        print("❌ Gagal inisialisasi Kinect. Program dihentikan.")
        return
    
    print()
    
    # 2. Robot Controller
    robot = RobotController()
    print("🤖 Menghubungkan ke robot...")
    if not robot.connect():
        print("⚠️  Lanjut tanpa koneksi robot (mode simulasi)")
        print("    Edit config/settings.py untuk mengatur port robot yang benar")
    
    print()
    
    # 3. Gesture Recognizer
    gesture_recognizer = GestureRecognizer()
    print("👋 Gesture recognizer siap")
    
    # 4. Visualizer
    visualizer = Visualizer()
    print("📺 Visualizer siap")
    
    print()
    print_controls()
    print("=" * 70)
    print("▶️  Program dimulai. Tekan Q untuk keluar.")
    print("=" * 70)
    print()
    
    # Main loop variables
    frame_number = 0
    running = True
    
    try:
        while running:
            # Update FPS
            visualizer.update_fps()
            
            # Ambil frame dari Kinect
            capture, body_frame = kinect.get_frame()
            
            if capture is None or body_frame is None:
                continue
            
            # Ambil depth dan body segmentation image
            ret_depth, depth_image = kinect.get_depth_image(capture)
            ret_body, body_image = kinect.get_body_segmentation(body_frame)
            
            if not ret_depth or not ret_body:
                continue
            
            # Combine images
            combined_image = visualizer.combine_images(depth_image, body_image)
            
            # Draw skeleton
            try:
                combined_image = body_frame.draw_bodies(combined_image)
            except:
                pass
            
            # Deteksi gesture dan kontrol robot
            num_bodies = kinect.get_num_bodies(body_frame)
            current_command = 'S'  # Default: STOP
            
            if num_bodies > 0:
                # Ambil body pertama
                body = kinect.get_body(body_frame, 0)
                
                if body is not None:
                    # Kenali gesture
                    gestures = gesture_recognizer.recognize_gesture(body)
                    
                    # Konversi ke perintah robot
                    current_command, sent = robot.send_gesture_command(gestures)
                    
                    if sent and robot.is_connected():
                        print(f"📤 Frame {frame_number}: {COMMAND_NAMES[current_command]} ({current_command}) - Gestures: {', '.join(gestures)}")
                    
                    # Visualisasi gesture
                    combined_image = visualizer.draw_gestures(
                        combined_image, 
                        gestures, 
                        body_id=0
                    )
                    
                    # Visualisasi perintah robot
                    combined_image = visualizer.draw_robot_command(
                        combined_image,
                        current_command,
                        robot.is_connected(),
                        gestures
                    )
            
            # Draw status bar
            combined_image = visualizer.draw_status(
                combined_image,
                frame_number,
                robot.is_connected()
            )
            
            # Tampilkan
            visualizer.show(combined_image)
            
            # Handle keyboard input
            key = visualizer.wait_key(1)
            
            if key == ord('q') or key == ord('Q'):
                # Quit
                print("\n⏹️  Keluar dari program...")
                running = False
                
            elif key == ord('c') or key == ord('C'):
                # Toggle koneksi robot
                if robot.is_connected():
                    robot.disconnect()
                else:
                    robot.connect()
                    
            elif key == ord('d') or key == ord('D'):
                # Toggle tampilan gesture
                show = visualizer.toggle_gestures()
                status = "ON" if show else "OFF"
                print(f"👁️  Tampilan gesture: {status}")
                
            elif key == ord('f') or key == ord('F'):
                # Toggle tampilan FPS
                show = visualizer.toggle_fps()
                status = "ON" if show else "OFF"
                print(f"📊 Tampilan FPS: {status}")
                
            elif key == ord('s') or key == ord('S'):
                # Emergency STOP
                robot.emergency_stop()
                print("🛑 EMERGENCY STOP!")
            
            frame_number += 1
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Program dihentikan (Ctrl+C)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        print("\n🧹 Membersihkan resources...")
        
        # Kirim STOP ke robot sebelum keluar
        if robot.is_connected():
            print("🛑 Mengirim perintah STOP ke robot...")
            robot.emergency_stop()
            time.sleep(0.2)
        
        robot.disconnect()
        kinect.cleanup()
        visualizer.cleanup()
        
        print()
        print("=" * 70)
        print("✅ Program selesai")
        print(f"📊 Total frame diproses: {frame_number}")
        
        # Tampilkan statistik gesture
        stats = gesture_recognizer.get_gesture_statistics()
        if stats:
            print("\n📈 Statistik Gesture:")
            for gesture, percentage in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                print(f"  - {gesture}: {percentage:.1f}%")
        
        print("=" * 70)


if __name__ == "__main__":
    main()
