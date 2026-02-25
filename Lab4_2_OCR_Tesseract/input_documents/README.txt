# Sample Invoice Images

This folder should contain your document images for OCR processing.

## Supported Formats
- PNG (.png)
- JPEG (.jpg, .jpeg)  
- BMP (.bmp)
- TIFF (.tiff)

## How to Add Images

1. **Using Sample Images (Recommended for Testing)**
   - Just run the script: `python ocr_pipeline.py`
   - The script will automatically create 5 sample invoice images
   - No manual setup needed!

2. **Using Your Own Invoice Images**
   - Place your document images in this folder
   - Supports PNG, JPG, JPEG, BMP, TIFF formats
   - Minimum recommended: 300x300 pixels
   - Minimum recommended resolution: 150 DPI (300 DPI ideal)

## Tips for Best OCR Results

- **Image Quality**: Clear, sharp images with good contrast
- **Lighting**: Avoid shadows, reflections, and uneven lighting
- **Angle**: Straight on (0-5° skew), not at angles
- **Size**: Characters should be at least 10-15 pixels tall
- **Background**: Plain background, no patterns or watermarks

## What Happens

When you run `python ocr_pipeline.py`:
1. The script checks this folder for images
2. If empty, automatically creates 5 sample invoices for testing
3. Processes all images through the OCR pipeline
4. Outputs:
   - Preprocessed images → `../output_images/`
   - Extracted JSON files → `../output_json/`
   - Accuracy report → `../accuracy_report.txt`
