"""
Face Emotion Detection
Uses OpenCV for basic face detection and emotion estimation
"""

import cv2
import numpy as np
from PIL import Image


class FaceEmotionDetector:
    """Detect emotion from facial expressions"""
    
    def __init__(self):
        # Load face cascade
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.smile_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_smile.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )
            self.available = True
        except Exception as e:
            self.available = False
            print(f"Face cascade error: {e}")
    
    def detect_faces(self, image):
        """Detect faces in image"""
        if not self.available:
            return []
        
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces
    
    def analyze(self, image):
        """Analyze emotion from face image"""
        if not self.available or image is None:
            return {
                'emotion': 'unknown',
                'confidence': 0.0,
                'face_detected': False,
                'details': 'Face detection not available'
            }
        
        try:
            img_array = np.array(image)
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) == 0:
                return {
                    'emotion': 'no_face',
                    'confidence': 0.0,
                    'face_detected': False,
                    'details': 'No face detected'
                }
            
            # Take first face
            (x, y, w, h) = faces[0]
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img_array[y:y+h, x:x+w]
            
            # Detect smile
            smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
            eyes = self.eye_cascade.detectMultiScale(roi_gray)
            
            # Simple emotion detection logic
            if len(smiles) > 0:
                emotion = 'happy'
                confidence = 0.7
            elif len(eyes) < 2:
                emotion = 'surprised'
                confidence = 0.5
            else:
                emotion = 'neutral'
                confidence = 0.5
            
            return {
                'emotion': emotion,
                'confidence': confidence,
                'face_detected': True,
                'details': f'Smiles: {len(smiles)}, Eyes: {len(eyes)}',
                'faces_count': len(faces)
            }
        
        except Exception as e:
            return {
                'emotion': 'error',
                'confidence': 0.0,
                'face_detected': False,
                'details': str(e)
            }
    
    def draw_faces(self, image):
        """Draw rectangles around detected faces"""
        if not self.available:
            return image
        
        img_array = np.array(image).copy()
        faces = self.detect_faces(image)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        return Image.fromarray(img_array)