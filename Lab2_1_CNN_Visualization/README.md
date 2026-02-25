# Lab 2.1: Understanding CNN Layers with VGG16

## 📋 Lab Overview

This laboratory exercise focuses on **understanding how Convolutional Neural Networks (CNNs) learn hierarchical representations** through feature visualization. Using the pre-trained **VGG16 model**, students will extract and visualize feature maps from different layers to understand what patterns are detected at various depths of the network.

### Learning Objectives

1. **Load and understand pre-trained deep CNN models** (VGG16 with ImageNet weights)
2. **Extract intermediate feature representations** from specific convolutional layers
3. **Visualize learned filters** at different network depths to understand hierarchical learning
4. **Analyze how CNN complexity increases** with depth (simple → complex features)
5. **Understand feature visualization's importance** in medical AI and safety-critical systems
6. **Develop skills in model interpretability** for explainable AI

---

## 🏗️ Project Structure

```
Lab2_1_CNN_Visualization/
├── cnn_visualization.py   # Main Python script (fully documented)
├── requirements.txt       # Project dependencies
├── README.md             # This file - project documentation
├── answers.txt           # Answers to lab questions
├── input_images/         # Input test images
│   └── test.jpg          # Sample image for visualization
└── output_images/        # Output folder (auto-created)
    ├── block1_conv1.png  # Early layer visualization
    ├── block3_conv3.png  # Middle layer visualization
    └── block5_conv3.png  # Deep layer visualization
```

---

## 🔧 Installation & Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Libraries:**
- **tensorflow/keras** - Deep learning framework for VGG16
- **numpy** - Numerical computing
- **matplotlib** - Data visualization
- **pillow** - Image processing
- **opencv-python** - Computer vision utilities

### Step 2: Prepare Input Image

Place your test image in the `input_images/` folder:
- **Filename**: `test.jpg`
- **Size**: Any size (will be resized to 224×224 for VGG16)
- **Format**: JPG, PNG, or BMP

### Step 3: Run the Code

```bash
python code.py
```

The script will:
✓ Load VGG16 with ImageNet weights  
✓ Create activation models for selected layers  
✓ Load and preprocess your image  
✓ Extract feature maps  
✓ Generate 4×4 grid visualizations  
✓ Save outputs to `output_images/`  

---

## 📊 What the Code Does

### 1. **Model Loading**
- Loads **VGG16** pre-trained on **ImageNet**
- Uses `include_top=False` to access convolutional layers only
- Prints complete model architecture summary

### 2. **Layer Selection**
Three representative layers are visualized:

| Layer | Kernel | Filters | Purpose |
|-------|--------|---------|---------|
| **block1_conv1** | 3×3 | 64 | Early: Edge/texture detection |
| **block3_conv3** | 3×3 | 256 | Middle: Shape/pattern detection |
| **block5_conv3** | 3×3 | 512 | Deep: Object part detection |

### 3. **Feature Extraction**
- Creates **sub-models** for each selected layer
- Uses model prediction to extract activation maps
- Handles batch dimension and tensor operations

### 4. **Visualization**
- Displays **first 16 filters** from each layer
- Organized as **4×4 grid** for clear comparison
- Normalized for proper display (0-1 range)
- Uses `viridis` colormap for interpretability

### 5. **Image Preprocessing**
- Resizes image to **224×224** (VGG16 standard)
- Applies **ImageNet normalization** (RGB mean/variance subtraction)
- Handles batch dimensions correctly

---

## 💡 Understanding the Results

### Early Layers (block1_conv1)
- Detect **low-level features**: edges, gradients, textures
- Show **simple, repetitive patterns**
- High spatial resolution (feature maps are large)
- Easy to interpret visually

**Example detections:** Horizontal lines, vertical edges, color boundaries

### Middle Layers (block3_conv3)
- Detect **mid-level features**: corners, shapes, local patterns
- Combine early layer outputs
- Moderate spatial resolution
- Intermediate complexity

**Example detections:** Corners, simple shapes, texture combinations

### Deep Layers (block5_conv3)
- Detect **high-level features**: object parts, semantic concepts
- Highly abstract representations
- Low spatial resolution (feature maps are small)
- Difficult to interpret visually

**Example detections:** Eyes, wheels, faces (abstract patterns)

---

## 🧠 CNN Hierarchical Learning

CNNs learn hierarchical features through **stacked convolutional layers**:

1. **Layer 1 (Early)**: Learns **basic visual primitives**
   - Edges in different orientations
   - Color contrasts
   - Simple gradients

2. **Layer 2-3 (Middle)**: Learns **combinations of primitives**
   - Corners and junctions
   - Simple textures
   - Local shapes

3. **Layer 4-5 (Deep)**: Learns **complex semantic features**
   - Object parts
   - Compositional patterns
   - High-level concepts

**Key Insight**: Each layer receives features from previous layers and learns **more complex, object-relevant patterns** through combination and composition.

---

## 🏥 Medical AI Applications

Feature visualization is critical in **medical AI systems** for:

### 1. **Diagnostic Confidence**
- Understand what patterns the model uses to diagnose
- Identify if model relies on relevant medical features
- Detect bias in learned representations

### 2. **Clinical Validation**
- Doctors can verify if detected features are medically meaningful
- Builds trust in AI system predictions
- Enables collaborative human-AI diagnosis

### 3. **Regulatory Compliance**
- FDA requires **explainability** for medical devices
- Feature visualization proves model learns meaningful patterns
- Documents decision-making process

### 4. **Safety & Error Detection**
- Identify if model learns spurious correlations
- Detect dataset bias (e.g., scanner artifacts)
- Prevent harmful misclassifications

**Example**: In cancer detection, doctors want to see **which regions are flagged** and **what patterns triggered the alert** before accepting the diagnosis.

---

## 🔍 Code Quality Features

✓ **Comprehensive error handling** - Try-except blocks prevent crashes  
✓ **Clear function structure** - Modular, single responsibility functions  
✓ **Professional documentation** - Docstrings for all functions  
✓ **Progress indicators** - Clear ✓/✗ symbols show execution status  
✓ **Organized constants** - Configuration at top of file  
✓ **Proper tensor handling** - Correct batch dimension management  
✓ **Memory efficiency** - Closes figures after saving  

---

## 📈 Key Parameters

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `IMAGE_WIDTH/HEIGHT` | 224 | VGG16 input size |
| `NUM_FILTERS_DISPLAY` | 16 | 4×4 grid size |
| `DPI` | 150 | Output image resolution |
| `COLORMAP` | viridis | Color scheme for visualization |

---

## 📝 Sample Output

```
================================================================================
LAB 2.1: CNN FEATURE VISUALIZATION WITH VGG16
================================================================================

STEP 1: Setting up directories...
✓ Created output directory: output_images

STEP 2: Loading VGG16 model...
✓ VGG16 model loaded with ImageNet weights

STEP 3: Model Summary...
Model: "vgg16"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         [(None, 224, 224, 3)]    0
block1_conv1 (Conv2D)        (None, 224, 224, 64)     1792
...
[Model summary continues]
...
STEP 5: Loading and preprocessing image...
✓ Image loaded successfully: input_images/test.jpg
✓ Image preprocessed successfully

STEP 6: Extracting feature maps...
✓ Extracted feature maps from block1_conv1
  Shape: (1, 224, 224, 64)

STEP 8: Visualizing and saving filters...
✓ Saved visualization: output_images/block1_conv1.png
✓ Saved visualization: output_images/block3_conv3.png
✓ Saved visualization: output_images/block5_conv3.png

✓ EXECUTION COMPLETED SUCCESSFULLY!
✓ All visualizations saved to: output_images/
================================================================================
```

---

## 🚀 Running the Lab

### Option 1: Command Line
```bash
cd Lab2_1_CNN_Visualization
python cnn_visualization.py
```

### Option 2: VS Code
1. Open folder in VS Code
2. Install Python extension
3. Open `cnn_visualization.py`
4. Click "Run" button or press `Ctrl+F5`

### Option 3: Jupyter Notebook
```python
%cd Lab2_1_CNN_Visualization
exec(open('code.py').read())
```

---

## 📋 Submission Checklist

Before submitting, verify:

- [ ] `cnn_visualization.py` runs without errors
- [ ] `input_images/test.jpg` exists and is a valid image
- [ ] All three PNG files are generated in `output_images/`
- [ ] `answers.txt` contains complete answers to all questions
- [ ] `README.md` is comprehensive and well-formatted
- [ ] `requirements.txt` lists all dependencies

---

## 🔗 References

1. **VGG16 Paper**: Simonyan, K., & Zisserman, A. (2014). *Very Deep Convolutional Networks for Large-Scale Image Recognition*
2. **Keras VGG16 Docs**: https://keras.io/api/applications/vgg/
3. **CNN Visualization Survey**: Erhan et al. (2009), Visualizing and Understanding CNNs
4. **Medical AI**: Ronneberger et al. (2015), U-Net for medical image segmentation

---

## ✍️ Author Information

**Lab Course**: B.Tech AI - Module 3  
**Lab Title**: Understanding CNN Layers with VGG16  
**Date**: February 2026  
**Submission Format**: Professional Lab Assignment  

---

**Last Updated**: February 25, 2026

