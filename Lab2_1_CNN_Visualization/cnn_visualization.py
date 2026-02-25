import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.gridspec as gridspec

# Import Keras models and preprocessing
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model

# ============================================================================
# CONFIGURATION AND CONSTANTS
# ============================================================================

IMAGE_WIDTH = 224
IMAGE_HEIGHT = 224
INPUT_IMAGE_PATH = "input_images/chest_image.jpg"
OUTPUT_DIR = "output_images"
LAYERS_TO_VISUALIZE = ["block1_conv1", "block3_conv3", "block5_conv3"]
NUM_FILTERS_DISPLAY = 16  

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_output_directory():
    """
    Create output_images directory if it doesn't exist.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✓ Created output directory: {OUTPUT_DIR}")
    else:
        print(f"✓ Output directory already exists: {OUTPUT_DIR}")


def load_and_preprocess_image(image_path):
    try:
        # Load image
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        img = image.load_img(image_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH))
        print(f"✓ Image loaded successfully: {image_path}")
        print(f"  Image shape: {img.size}")
        
        # Convert to array
        img_array = image.img_to_array(img)
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        # Preprocess for VGG16 (ImageNet normalization)
        preprocessed_img = preprocess_input(img_array.copy())
        
        print(f"✓ Image preprocessed successfully")
        print(f"  Preprocessed shape: {preprocessed_img.shape}")
        
        return preprocessed_img, img_array
        
    except Exception as e:
        print(f"✗ Error loading/preprocessing image: {e}")
        raise


def build_vgg16_model(include_top=False):
    try:
        model = VGG16(
            weights='imagenet',
            include_top=include_top,
            input_shape=(IMAGE_HEIGHT, IMAGE_WIDTH, 3)
        )
        print("✓ VGG16 model loaded with ImageNet weights")
        print(f"  include_top={include_top}")
        return model
        
    except Exception as e:
        print(f"✗ Error loading VGG16 model: {e}")
        raise


def print_model_summary(model):
    print("\n" + "="*80)
    print("VGG16 FULL MODEL SUMMARY")
    print("="*80)
    model.summary()
    print("="*80 + "\n")


def create_activation_models(base_model, layer_names):
    activation_models = {}
    
    try:
        for layer_name in layer_names:
            # Get the layer
            target_layer = base_model.get_layer(layer_name)
            
            # Create sub-model
            activation_model = Model(
                inputs=base_model.input,
                outputs=target_layer.output
            )
            
            activation_models[layer_name] = activation_model
            print(f"✓ Created activation model for: {layer_name}")
            
    except Exception as e:
        print(f"✗ Error creating activation models: {e}")
        raise
    
    return activation_models


def extract_feature_maps(image, activation_models):
    feature_maps = {}
    
    try:
        for layer_name, model in activation_models.items():
            # Get activations
            activations = model.predict(image, verbose=0)
            feature_maps[layer_name] = activations
            
            print(f"✓ Extracted feature maps from {layer_name}")
            print(f"  Shape: {activations.shape} (batch, height, width, channels)")
            
    except Exception as e:
        print(f"✗ Error extracting feature maps: {e}")
        raise
    
    return feature_maps


def normalize_image_for_display(img_array):
    # Handle different input shapes
    if len(img_array.shape) == 4:
        img_array = img_array[0]  # Remove batch dimension
    
    # Normalize to 0-1 range
    min_val = img_array.min()
    max_val = img_array.max()
    
    if max_val - min_val > 0:
        normalized = (img_array - min_val) / (max_val - min_val)
    else:
        normalized = img_array
    
    return normalized


def visualize_layer_filters(feature_maps, layer_name, num_filters=16):
    # Extract single sample and limit to first num_filters
    activations = feature_maps[0, :, :, :num_filters]  # (height, width, num_filters)
    
    # Calculate grid dimensions
    grid_size = 4  # 4x4 grid
    
    # Create figure with proper layout
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(grid_size, grid_size, hspace=0.4, wspace=0.3)
    
    filter_idx = 0
    for i in range(grid_size):
        for j in range(grid_size):
            ax = fig.add_subplot(gs[i, j])
            
            # Get single filter activation
            filter_activation = activations[:, :, filter_idx]
            
            # Normalize for display
            normalized = normalize_image_for_display(filter_activation)
            
            # Display
            im = ax.imshow(normalized, cmap='viridis', interpolation='bilinear')
            ax.set_title(f'Filter {filter_idx + 1}', fontsize=10, fontweight='bold')
            ax.axis('off')
            
            filter_idx += 1
    
    # Overall title
    title = f'{layer_name} - First 16 Filters (4x4 Grid)'
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    return fig


def save_visualization(fig, layer_name):
    try:
        filename = f"{layer_name}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        fig.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualization: {filepath}")
        
    except Exception as e:
        print(f"✗ Error saving visualization: {e}")
        raise


def display_layer_statistics(feature_maps, layer_name):
    print(f"\n--- Statistics for {layer_name} ---")
    print(f"Shape: {feature_maps.shape}")
    print(f"Min value: {feature_maps.min():.4f}")
    print(f"Max value: {feature_maps.max():.4f}")
    print(f"Mean: {feature_maps.mean():.4f}")
    print(f"Std Dev: {feature_maps.std():.4f}")
    print(f"Number of filters: {feature_maps.shape[-1]}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*80)
    print("LAB 2.1: CNN FEATURE VISUALIZATION WITH VGG16")
    print("="*80 + "\n")
    
    try:
        # Step 1: Create output directory
        print("STEP 1: Setting up directories...")
        create_output_directory()
        
        # Step 2: Load and configure VGG16 model
        print("\nSTEP 2: Loading VGG16 model...")
        vgg16_model = build_vgg16_model(include_top=False)
        
        # Step 3: Print model summary
        print("\nSTEP 3: Model Summary...")
        print_model_summary(vgg16_model)
        
        # Step 4: Create activation models for selected layers
        print("STEP 4: Creating activation models...")
        activation_models = create_activation_models(vgg16_model, LAYERS_TO_VISUALIZE)
        
        # Step 5: Load and preprocess image
        print("\nSTEP 5: Loading and preprocessing image...")
        preprocessed_img, original_img = load_and_preprocess_image(INPUT_IMAGE_PATH)
        
        # Step 6: Extract feature maps
        print("\nSTEP 6: Extracting feature maps...")
        feature_maps_dict = extract_feature_maps(preprocessed_img, activation_models)
        
        # Step 7: Display layer statistics
        print("\nSTEP 7: Layer Statistics...")
        for layer_name, feature_maps in feature_maps_dict.items():
            display_layer_statistics(feature_maps, layer_name)
        
        # Step 8: Visualize and save filters
        print("\nSTEP 8: Visualizing and saving filters...")
        for layer_name, feature_maps in feature_maps_dict.items():
            print(f"\nProcessing {layer_name}...")
            fig = visualize_layer_filters(feature_maps, layer_name, NUM_FILTERS_DISPLAY)
            save_visualization(fig, layer_name)
            plt.close(fig)  # Close figure to free memory
        
        # Success message
        print("\n" + "="*80)
        print("✓ EXECUTION COMPLETED SUCCESSFULLY!")
        print(f"✓ All visualizations saved to: {OUTPUT_DIR}/")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ EXECUTION FAILED: {e}")
        print("="*80 + "\n")
        raise


# ============================================================================
# SCRIPT ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
