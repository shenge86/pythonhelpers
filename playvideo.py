# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 22:21:53 2026

@author: sheng
"""
import sys
import cv2
from pathlib import Path

class VideoPlayer:
    """Video player that pauses on last frame"""
    
    def __init__(self, video_path):
        self.video_path = Path(video_path)
        self.video = cv2.VideoCapture(str(self.video_path))
        self.playing = False
        self.current_frame = 0
        
        if not self.video.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.delay = int(1000 / self.fps)
        
    def play(self):
        """Play video"""
        print("Controls: SPACE=pause/play, Q=quit, R=restart")
        self.playing = True
        
        last_frame = None
        
        while True:
            if self.playing:
                ret, frame = self.video.read()
                
                if not ret:
                    # Video ended - pause and show last frame
                    print("\nVideo ended!")
                    print("Press R to restart or Q to quit")
                    self.playing = False
                    
                    # Continue to show last frame
                    if last_frame is not None:
                        while True:
                            # Add "ENDED" text to last frame
                            display = last_frame.copy()
                            cv2.putText(display, "VIDEO ENDED",
                                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                                       1, (0, 0, 255), 3)
                            cv2.putText(display, "Press R to restart or Q to quit",
                                       (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.6, (255, 255, 255), 2)
                            
                            cv2.imshow('Video Player', display)
                            
                            key = cv2.waitKey(100) & 0xFF
                            
                            if key == ord('q'):
                                self.close()
                                return
                            elif key == ord('r'):
                                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                                self.current_frame = 0
                                self.playing = True
                                print("Restarting...")
                                break
                    continue
                
                last_frame = frame.copy()
                self.current_frame += 1
                
                # Show frame info
                cv2.putText(frame, f"Frame: {self.current_frame}/{self.total_frames}",
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Video Player', frame)
                wait_time = self.delay
            else:
                wait_time = 100
            
            key = cv2.waitKey(wait_time) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord(' '):
                if self.current_frame < self.total_frames:
                    self.playing = not self.playing
                    print("Paused" if not self.playing else "Playing")
            elif key == ord('r'):
                self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
                self.current_frame = 0
                self.playing = True
                print("Restarted")
        
        self.close()
    
    def close(self):
        """Release resources"""
        self.video.release()
        cv2.destroyAllWindows()

# Usage
try:
    video = sys.argv[1]
except:
    video = 'data_vid/rosetta.mp4'
    
player = VideoPlayer(video)
player.play()