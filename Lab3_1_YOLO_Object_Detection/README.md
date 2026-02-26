# Lab 3.1: Pre-trained Object Detection with YOLO

## 📋 Lab Overview

This laboratory exercise focuses on **using pre-trained YOLO (You Only Look Once) models for real-time multi-object detection**. Students will implement an object detection system using YOLOv8n that processes video frames, detects all objects in the COCO dataset, displays detection statistics, and saves annotated output with real-time performance monitoring.

### Learning Objectives

1. **Understand pre-trained model usage** - Load and use production-ready deep learning models
2. **Implement real-time object detection** - Process video frames with minimal latency
3. **Handle multiple object classes** - Detect and visualize all COCO dataset classes
4. **Calculate and monitor FPS** - Measure real-time performance metrics
5. **Handle video I/O** - Read input video streams and write annotated output with proper codecs
6. **Develop production code** - Error handling, structured functions, clean architecture
7. **Understand one-stage detectors** - How YOLO differs from two-stage detectors (R-CNN family)

---

## 🏗️ Project Structure

```
Lab3_1_YOLO_Object_Detection/
├── yolo_detection.py       # Main object detection script (well-documented)
├── requirements.txt        # Project dependencies
├── README.md              # This file - project documentation
├── answers.txt            # Answers to all lab questions
├── input_video/           # Input video folder
│   └── test.mp4           # Sample video file for processing
├── output_video/          # Output folder (auto-created)
│   └── detection_output.mp4  # Annotated video with detections
└── output_frames/         # Sample frames folder (auto-created)
    ├── frame_0030.png     # Sample frame 1
    ├── frame_0060.png     # Sample frame 2
    └── ...                # Up to 5 sample frames
```

---

## 🔧 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Libraries:**
- **ultralytics** - YOLOv8 implementation and model loading
- **opencv-python** - Video reading/writing and image processing
- **numpy** - Numerical computing and array operations

### Step 2: Prepare Input Video

Place your test video in the `input_video/` folder:
- **Filename**: `test.mp4`
- **Format**: MP4, AVI, MOV (any OpenCV-compatible format)
- **Resolution**: Any size (will be processed at original resolution)
- **Minimum duration**: 5 seconds recommended

**Or use Webcam:**
To use your webcam instead, edit line ~60 in `yolo_detection.py`:
```python
USE_WEBCAM = True  # Change from False to True
```

### Step 3: Run the Script

```bash
python yolo_detection.py
```

**The script will:**
- ✓ Load YOLOv8n model (automatic download on first run)
- ✓ Open input video or webcam stream
- ✓ Process each frame with YOLO inference
- ✓ Detect all COCO dataset objects (people, cars, animals, etc.)
- ✓ Draw bounding boxes with class labels and confidence scores
- ✓ Display real-time object count and FPS on video
- ✓ Save annotated video to `output_video/detection_output.mp4`
- ✓ Save 5 sample frames to `output_frames/` for verification
- ✓ Print summary statistics and performance metrics

**To stop processing:** Press `ESC` key

---

## 📊 What the Code Does

### 1. **Model Loading**
- Downloads and loads **YOLOv8n** (nano version)
- Optimized for CPU inference (~5-10 FPS depending on resolution)
- ~3.2M parameters (smallest YOLO variant)

### 2. **Video Input**
- Reads frames from `input_video/test.mp4` or webcam
- Extracts video properties: resolution, FPS, frame count
- Maintains frame order and timing

### 3. **YOLO Inference**
- Runs deep learning model on each frame
- Detects objects with class labels and confidence scores
- NMS (Non-Maximum Suppression) removes duplicate detections

### 4. **Object Detection**
- Runs deep learning model on each frame with NMS (Non-Maximum Suppression)
- Detects all COCO dataset classes: people, vehicles, animals, furniture, etc.
- Returns bounding box coordinates, class labels, and confidence scores
- Applies confidence threshold filtering (default: 0.5)

### 5. **Visualization**
- Draws green bounding boxes around all detected objects
- Displays class label and confidence score for each detection
- Shows live object count by class (top-left corner)
- Shows real-time FPS counter (top-right corner)
- Uses OpenCV text rendering for performance

### 6. **FPS Calculation**
- Uses sliding window (last 30 frames) for smooth FPS estimation
- Calculated from actual processing time, not video FPS
- Indicates real-time performance capability

### 7. **Output Generation**
- Saves **annotated video** with all detections visible
- Uses MJPEG codec for broad compatibility
- Saves **5 sample frames** at regular intervals
- Computes **summary statistics**: average people, FPS, etc.

---

## 💡 Understanding the Results

### Output Video (`detection_output.mp4`)
- Same resolution and duration as input video
- Green boxes show all detected objects with class labels
- Confidence score displayed above each box
- Object counts updated per frame
- FPS counter shows real-time inference performance
- Uses MJPEG codec for broad compatibility and quick playback

### Sample Frames (`frame_XXXX.png`)
- Snapshot frames saved at regular intervals (every 30 frames by default)
- Useful for verification and review without playing full video
- Can be embedded in presentations or reports

### Console Output
```
STEP 1: Setting up directories...
✓ Created directory: output_video
✓ Created directory: output_frames

STEP 2: Loading YOLO model...
Loading yolov8n model...
✓ yolov8n model loaded successfully
  Model device: cpu

STEP 3: Opening video source...
✓ Video file opened: input_video/test.mp4
  Video info: 1280x720 @ 30.0 FPS
  Total frames: 900

STEP 4: Setting up video writer...
✓ Video writer created: output_video/detection_output.mp4

STEP 5: Processing frames...
Press ESC to stop

  Frame   30 | People:  2 | FPS: 12.5
  Frame   60 | People:  3 | FPS: 13.2
  ...
  Frame  900 | People:  1 | FPS: 12.8

✓ End of video reached

SUMMARY STATISTICS
Average people per frame: 2.45
Max people in single frame: 5
Average FPS: 12.8
Output video saved: output_video/detection_output.mp4
Sample frames saved: output_frames/
```

---

## 🧠 How YOLO Works

**YOLO (You Only Look Once)** performs object detection in a **single forward pass** through the network, unlike two-stage detectors (Faster R-CNN) that first propose regions then classify them.

**Architecture:**
1. **Backbone**: Extracts features from input image (in YOLOv8: CNNs with residual blocks)
2. **Neck**: Aggregates multi-scale features for different object sizes
3. **Head**: Predicts bounding boxes, confidence scores, and class probabilities at multiple scales

**Detection Process:**
- Input image is divided into a **grid**
- Each grid cell predicts multiple bounding boxes and confidence scores
- Anchor-free approach: directly predicts box coordinates
- Non-Maximum Suppression (NMS) removes overlapping detections
- Output: filtered bounding boxes with class labels and confidences

**Why single-stage is fast:**
- One forward pass (vs. two for region-based methods)
- Parallelizable grid-based detection
- Trades some accuracy for speed (99% accuracy for 100% speed improvement isn't always available)

---

## 📈 Key Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `MODEL_NAME` | yolov8n | Nano model - fastest, least parameters |
| `CONFIDENCE_THRESHOLD` | 0.5 | Only accept detections with >50% confidence |
| `TARGET_CLASS_ID` | 0 | COCO class ID for "person" |
| `FPS_WINDOW` | 30 | Frames used for FPS averaging |
| `FONT_THICKNESS` | 2 | Bounding box line thickness (pixels) |
| `BOX_COLOR` | (0, 255, 0) | Green color in BGR format |

---

## ⚙️ Customization Guide

### Change Detection Threshold
```python
CONFIDENCE_THRESHOLD = 0.7  # 70% confidence (more strict)
```

### Detect Multiple Classes
```python
# Change in filter_detections_by_class():
TARGET_CLASSES = [0, 1, 2]  # person, bicycle, car
if cls_id in TARGET_CLASSES:
    boxes.append(...)
```

### Use Different YOLO Version
```python
MODEL_NAME = "yolov8s"  # Small (faster than m/l, more accurate than n)
# or "yolov8m", "yolov8l", "yolov8x" for larger models
```

### Use GPU (if available)
```python
device = 0  # Automatically uses CUDA GPU if available
# Change: device=0 in run_yolo_inference() and model.to(device)
```

### Adjust Output Resolution
```python
# Resize frame before writing:
resized = cv2.resize(annotated_frame, (640, 360))
writer.write(resized)
```

---

## 🚀 Running Options

### Option 1: Command Line
```bash
cd Lab3_1_YOLO_Object_Detection
python yolo_detection.py
```

### Option 2: VS Code
1. Open folder in VS Code
2. Install Python extension
3. Open `yolo_detection.py`
4. Click "Run" button or press `Ctrl+F5`
5. Press `ESC` to stop when done

### Option 3: With Webcam
```python
# Edit yolo_detection.py, line 57:
USE_WEBCAM = True
# Then run: python yolo_detection.py
```

---

## 📊 Performance Benchmarks

### CPU Performance (Intel i5/Ryzen 5 equivalent):
- **YOLOv8n**: ~10-15 FPS @ 1280×720
- **YOLOv8s**: ~5-8 FPS @ 1280×720
- **YOLOv8m**: ~2-4 FPS @ 1280×720

### GPU Performance (NVIDIA RTX 3060):
- **YOLOv8n**: ~100+ FPS @ 1280×720
- **YOLOv8s**: ~80+ FPS @ 1280×720
- **YOLOv8m**: ~50+ FPS @ 1280×720

**Note**: YOLOv8n is optimized for real-time inference on edge devices and CPUs.

---

## 🔗 References

1. **YOLOv8 Paper**: Ultralytics YOLOv8 (2023)
2. **YOLO Series Evolution**: 
   - YOLOv1: https://arxiv.org/abs/1506.02640
   - YOLOv5: https://github.com/ultralytics/yolov5
3. **OpenCV Documentation**: https://docs.opencv.org/
4. **COCO Dataset**: https://cocodataset.org/ (class labels reference)
5. **Ultralytics Docs**: https://docs.ultralytics.com/

---

## 📋 Submission Checklist

Before submitting, verify:

- [ ] `yolo_detection.py` runs without errors
- [ ] `input_video/test.mp4` exists (any video with people)
- [ ] `detection_output.mp4` is generated in `output_video/`
- [ ] At least 5 sample frames saved in `output_frames/`
- [ ] `answers.txt` contains complete answers to all 6 questions
- [ ] `README.md` is comprehensive (this file)
- [ ] `requirements.txt` lists all dependencies
- [ ] Console output shows summary statistics
- [ ] Code runs with `python yolo_detection.py` (no errors)

---

## 🎓 Advanced Topics

### Object Tracking
Use YOLO + tracking algorithms (ByteTrack, DeepSORT) to track people across frames and count unique individuals.

### Pose Estimation
Use YOLOv8-Pose instead of YOLOv8-Detect to estimate human pose keypoints.

### Segmentation
Use YOLOv8-Segment for pixel-level masks instead of bounding boxes.

### Model Optimization
- Quantization: reduce model size for mobile devices
- Pruning: remove less important connections
- Knowledge Distillation: train smaller model to mimic larger one

---

## ✍️ Author Information

**Lab Course**: B.Tech AI - Module 3  
**Lab Title**: Pre-trained Object Detection with YOLO  
**Date**: February 2026  
**Submission Format**: Professional Lab Assignment  

---

**Last Updated**: February 25, 2026

