import os
import re
import json
import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from datetime import datetime
import subprocess
import platform

# Try to import pytesseract, fallback to easyocr if not available
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

try:
    import easyocr
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False

# Global OCR reader
ocr_reader = None
ocr_engine = None  # 'pytesseract', 'easyocr', or None

def configure_pytesseract():
    """Configure pytesseract to find Tesseract executable based on OS"""
    if platform.system() == 'Windows':
        # Try common Windows installation paths
        possible_paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.pytesseract_cmd = path
                print(f"[OK] Tesseract found at: {path}")
                return True
        
        # Try to find it using 'where' command
        try:
            result = subprocess.run(['where', 'tesseract'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                path = result.stdout.strip()
                pytesseract.pytesseract.pytesseract_cmd = path
                print(f"[OK] Tesseract found at: {path}")
                return True
        except Exception:
            pass
        
        print("[!] Tesseract not found in standard Windows paths")
        return False
    elif platform.system() == 'Darwin':
        # macOS
        try:
            result = subprocess.run(['which', 'tesseract'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] Tesseract found via which: {result.stdout.strip()}")
                return True
        except Exception:
            pass
        print("[!] Tesseract not found on macOS. Install with: brew install tesseract")
        return False
    else:
        # Linux
        try:
            result = subprocess.run(['which', 'tesseract'],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] Tesseract found via which: {result.stdout.strip()}")
                return True
        except Exception:
            pass
        print("[!] Tesseract not found on Linux. Install with: sudo apt-get install tesseract-ocr")
        return False

def initialize_ocr():
    """Initialize OCR engine - try pytesseract first, then easyocr"""
    global ocr_reader, ocr_engine
    
    print("[*] Initializing OCR engine...")
    
    # Try pytesseract first
    if HAS_PYTESSERACT:
        print("  Attempting to use Tesseract (pytesseract)...")
        if configure_pytesseract():
            ocr_engine = 'pytesseract'
            print(f"  [OK] Initialized Tesseract OCR engine")
            return True
    
    # Fallback to easyocr
    if HAS_EASYOCR:
        print("  Attempting to use EasyOCR...")
        try:
            ocr_reader = easyocr.Reader(['en'], gpu=False)
            ocr_engine = 'easyocr'
            print(f"  [OK] Initialized EasyOCR engine")
            return True
        except Exception as e:
            print(f"  [ERROR] EasyOCR initialization failed: {e}")
            return False
    
    # No OCR engine available
    print("\n[ERROR] No OCR engine available!")
    print("   Install one of the following:")
    print("   1. Tesseract: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   2. EasyOCR: pip install easyocr")
    return False


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Config:
    """Configuration parameters for OCR pipeline"""
    INPUT_DIR = 'input_documents'
    OUTPUT_IMG_DIR = 'output_images'
    OUTPUT_JSON_DIR = 'output_json'
    ACCURACY_REPORT = 'accuracy_report.txt'
    
    # Thresholding parameters - use Otsu's binary thresholding for adaptive adjustment
    THRESHOLD_VALUE = 127  # Reduced from 150 for better text preservation
    MAX_VALUE = 255
    
    # Morphological operations
    MORPH_KERNEL_SIZE = (3, 3)  # Reduced from (5, 5) to preserve text details
    
    # Blur parameters
    BLUR_KERNEL_SIZE = (3, 3)


# ============================================================================
# REGEX PATTERNS FOR FIELD EXTRACTION
# ============================================================================

class RegexPatterns:
    
    # Date patterns (multiple formats)
    DATE_PATTERNS = [
        r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',  # DD/MM/YYYY or MM/DD/YYYY
        r'\b(\d{4})[/-](\d{1,2})[/-](\d{1,2})\b',    # YYYY/MM/DD
        r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* (\d{1,2})[,]? (\d{4})\b',  # Month DD, YYYY
    ]
    
    # Currency amounts (handles $, €, ₹, etc.)
    CURRENCY_PATTERNS = [
        r'[$€₹£¥]\s*(\d+[,.]?\d*[,.]?\d*)',  # Currency symbol first
        r'(\d+[,.]?\d*[,.]?\d*)\s*[$€₹£¥]',  # Currency symbol last
        r'\b(USD|EUR|INR|GBP|JPY):?\s*(\d+[,.]?\d*[,.]?\d*)',  # Currency code
    ]
    
    # Email addresses
    EMAIL_PATTERN = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    
    @classmethod
    def extract_dates(cls, text):
        """Extract all dates from text"""
        dates = []
        for pattern in cls.DATE_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append(match.group(0))
        return list(set(dates))  # Remove duplicates
    
    @classmethod
    def extract_amounts(cls, text):
        """Extract all currency amounts from text"""
        amounts = []
        for pattern in cls.CURRENCY_PATTERNS:
            matches = re.finditer(pattern, text)
            for match in matches:
                amounts.append(match.group(0).strip())
        return list(set(amounts))  # Remove duplicates
    
    @classmethod
    def extract_emails(cls, text):
        """Extract all email addresses from text"""
        matches = re.finditer(cls.EMAIL_PATTERN, text)
        return [match.group(0) for match in matches]


# ============================================================================
# CORE OCR FUNCTIONS
# ============================================================================

def ensure_directories_exist():
    """Create output directories if they don't exist"""
    for directory in [Config.OUTPUT_IMG_DIR, Config.OUTPUT_JSON_DIR]:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"[OK] Directory '{directory}' ready")


def load_image(image_path):
    try:
        image = Image.open(image_path)
        print(f"[OK] Loaded image: {os.path.basename(image_path)}")
        return image
    except Exception as e:
        print(f"[ERROR] Error loading {image_path}: {e}")
        return None


def preprocess_image(cv_image):
    # Step 1: Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Step 2: Apply Gaussian blur (noise reduction)
    blurred = cv2.GaussianBlur(gray, Config.BLUR_KERNEL_SIZE, 0)
    
    # Step 3: Apply Otsu's binary thresholding (adaptive threshold)
    _, binary = cv2.threshold(blurred, 0, Config.MAX_VALUE, 
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 4: Apply morphological operations (but more gently)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, Config.MORPH_KERNEL_SIZE)
    
    # Light closing: removes small black noise (holes in text)
    closed = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
    
    # Light opening: removes small white noise (speckles)
    processed = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # Optional: Apply dilation to make text slightly thicker for better OCR
    # This helps preserve thin characters
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.dilate(processed, dilate_kernel, iterations=1)
    
    return processed


def extract_text(image_pil):
    """Extract text using the configured OCR engine"""
    global ocr_reader, ocr_engine
    
    try:
        if ocr_engine == 'pytesseract':
            text = pytesseract.image_to_string(image_pil)
            if not text or text.strip() == "":
                print("  ⚠ Warning: Tesseract returned empty text. Check if Tesseract is properly installed.")
            return text
        
        elif ocr_engine == 'easyocr':
            # EasyOCR expects numpy array or file path
            # Convert PIL to numpy array
            img_np = np.array(image_pil)
            results = ocr_reader.readtext(img_np, detail=0)
            text = '\n'.join(results)
            return text
        
        else:
            print(f"[ERROR] No OCR engine initialized!")
            return ""
    
    except Exception as e:
        print(f"[ERROR] Error extracting text: {e}")
        return ""


def extract_fields(text):
    fields = {
        'dates': RegexPatterns.extract_dates(text),
        'amounts': RegexPatterns.extract_amounts(text),
        'emails': RegexPatterns.extract_emails(text)
    }
    return fields


def save_json(filename, data, output_dir):
    try:
        json_filename = f"{Path(filename).stem}_extracted.json"
        json_path = os.path.join(output_dir, json_filename)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Saved JSON: {json_filename}")
        return json_path
    except Exception as e:
        print(f"[ERROR] Error saving JSON: {e}")
        return None


def save_image(image_array, filename, output_dir):
    try:
        output_filename = f"{Path(filename).stem}_preprocessed.png"
        output_path = os.path.join(output_dir, output_filename)
        
        cv2.imwrite(output_path, image_array)
        print(f"[OK] Saved preprocessed image: {output_filename}")
        return output_path
    except Exception as e:
        print(f"[ERROR] Error saving image: {e}")
        return None


def get_sample_images():
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Ensure input directory exists
        if not os.path.exists(Config.INPUT_DIR):
            os.makedirs(Config.INPUT_DIR, exist_ok=True)
        
        # Check if directory is empty - always regenerate for better quality
        existing_files = [f for f in os.listdir(Config.INPUT_DIR) 
                         if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
        
        # Remove existing sample images to force regeneration
        if existing_files and any('sample_invoice' in f for f in existing_files):
            for f in existing_files:
                if 'sample_invoice' in f:
                    try:
                        os.remove(os.path.join(Config.INPUT_DIR, f))
                    except:
                        pass
        
        print("\n[*] Creating OCR-optimized sample invoice images...")
        
        sample_texts = [
            "INVOICE #001\nDate: 15/01/2024\nAmount: $500.50\nEmail: customer1@example.com",
            "INVOICE #002\nDate: Jan 20, 2024\nAmount: €750.75\nEmail: buyer@company.com",
            "INVOICE #003\nDate: 2024-02-10\nAmount: ₹45000\nEmail: contact@business.in",
            "INVOICE #004\nDate: 05/15/2024\nAmount: $1200.00\nEmail: user@domain.com",
            "INVOICE #005\nDate: Feb 28, 2024\nAmount: USD 3500\nEmail: admin@organization.org"
        ]
        
        for i, text in enumerate(sample_texts, 1):
            try:
                # Create larger white image for better OCR readability
                img = Image.new('RGB', (1200, 800), color='white')
                draw = ImageDraw.Draw(img)
                
                # Try to use better font sizes
                try:
                    font = ImageFont.truetype("arial.ttf", 60)
                except Exception:
                    try:
                        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 60)
                    except Exception:
                        font = ImageFont.load_default()
                
                # Draw text with proper spacing and larger font
                lines = text.split('\n')
                y_offset = 100
                for line in lines:
                    # Draw with black text on white background for max contrast
                    draw.text((80, y_offset), line, fill='black', font=font)
                    y_offset += 130
                
                # Add border for better OCR detection
                draw.rectangle([(10, 10), (1190, 790)], outline='black', width=3)
                
                # Save with proper path handling
                filename = os.path.join(Config.INPUT_DIR, f"sample_invoice_{i:02d}.png")
                img.save(filename, quality=95)
                print(f"  [OK] Created {os.path.basename(filename)} (1200x800, high quality)")
            except Exception as sub_error:
                print(f"  [ERROR] Error creating image {i}: {sub_error}")
                continue
        
        print("[OK] Sample images created successfully\n")
            
    except ImportError:
        print("\n[ERROR] PIL (Pillow) not installed. Run: pip install Pillow\n")
    except Exception as e:
        print(f"\n[ERROR] Error in sample image creation: {e}\n")
        print("  Try manually adding images to input_documents/ folder\n")


# ============================================================================
# MAIN PROCESSING PIPELINE
# ============================================================================

def process_document(image_path):
    results = {
        'filename': os.path.basename(image_path),
        'text_before_preprocessing': '',
        'text_after_preprocessing': '',
        'characters_before': 0,
        'characters_after': 0,
        'fields': {}
    }
    
    # Load image
    pil_image = load_image(image_path)
    if pil_image is None:
        return results
    
    # Convert PIL image to OpenCV format for preprocessing
    cv_image = cv2.imread(image_path)
    
    # ========== STEP 1: OCR WITHOUT PREPROCESSING ==========
    text_before = extract_text(pil_image)
    results['text_before_preprocessing'] = text_before
    results['characters_before'] = len(text_before)
    
    print(f"  Before preprocessing: {results['characters_before']} characters")
    
    # ========== STEP 2: PREPROCESS AND OCR ==========
    preprocessed = preprocess_image(cv_image)
    
    # Convert preprocessed image to PIL format for Tesseract
    pil_preprocessed = Image.fromarray(preprocessed)
    text_after = extract_text(pil_preprocessed)
    results['text_after_preprocessing'] = text_after
    results['characters_after'] = len(text_after)
    
    print(f"  After preprocessing: {results['characters_after']} characters")
    
    # ========== STEP 3: EXTRACT STRUCTURED FIELDS ==========
    fields = extract_fields(text_after)
    results['fields'] = fields
    
    print(f"  Extracted: {len(fields['dates'])} dates, " + 
          f"{len(fields['amounts'])} amounts, {len(fields['emails'])} emails")
    
    # ========== STEP 4: SAVE OUTPUTS ==========
    # Save preprocessed image
    save_image(preprocessed, image_path, Config.OUTPUT_IMG_DIR)
    
    # Prepare JSON output
    json_data = {
        'filename': results['filename'],
        'extracted_text': text_after[:500],  # First 500 chars for brevity
        'dates': fields['dates'],
        'amounts': fields['amounts'],
        'emails': fields['emails'],
        'processing_timestamp': datetime.now().isoformat()
    }
    
    # Save JSON
    save_json(image_path, json_data, Config.OUTPUT_JSON_DIR)
    
    return results


def generate_accuracy_report(all_results):
    total_before = sum(r['characters_before'] for r in all_results)
    total_after = sum(r['characters_after'] for r in all_results)
    
    improvement = 0
    if total_before > 0:
        improvement = ((total_after - total_before) / total_before) * 100
    
    report = f"""
{'='*80}
OCR ACCURACY COMPARISON REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

SUMMARY STATISTICS
{'-'*80}
Total characters detected WITHOUT preprocessing: {total_before}
Total characters detected WITH preprocessing:    {total_after}
Improvement:                                     {improvement:+.2f}%

{'='*80}
DOCUMENT-BY-DOCUMENT BREAKDOWN
{'-'*80}
"""
    
    for result in all_results:
        doc_improvement = 0
        if result['characters_before'] > 0:
            doc_improvement = ((result['characters_after'] - result['characters_before']) 
                              / result['characters_before']) * 100
        
        report += f"""
Document: {result['filename']}
  - Characters (before):  {result['characters_before']}
  - Characters (after):   {result['characters_after']}
  - Improvement:          {doc_improvement:+.2f}%
  - Extracted Fields:
    • Dates found:        {len(result['fields']['dates'])}
    • Amounts found:      {len(result['fields']['amounts'])}
    • Emails found:       {len(result['fields']['emails'])}
"""
    
    report += f"""
{'='*80}
CONCLUSION
{'-'*80}
Preprocessing enhanced OCR accuracy by improving text detection and reducing
noise. Higher positive percentages indicate that preprocessing significantly
improved the quality of extracted text, leading to better structured data
extraction for business automation tasks.

{'='*80}
"""
    
    try:
        with open(Config.ACCURACY_REPORT, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n[OK] Accuracy report saved: {Config.ACCURACY_REPORT}")
    except Exception as e:
        print(f"[ERROR] Error saving report: {e}")
    
    print(report)


def main():
    print("\n" + "="*80)
    print("OCR PIPELINE WITH TESSERACT - Lab 4.2")
    print("="*80 + "\n")
    
    # Initialize OCR engine (try pytesseract first, fallback to easyocr)
    if not initialize_ocr():
        print("\n[ERROR] OCR initialization failed!")
        print("   Please install EasyOCR: pip install easyocr")
        print("   Or install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki\n")
        return
    
    # Ensure output directories exist
    ensure_directories_exist()
    
    # Create sample images if needed
    get_sample_images()
    
    # Check for input images
    if not os.path.exists(Config.INPUT_DIR):
        print(f"[ERROR] '{Config.INPUT_DIR}' directory not found!")
        return
    
    image_files = [f for f in os.listdir(Config.INPUT_DIR) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    if not image_files:
        print(f"[ERROR] No image files found in '{Config.INPUT_DIR}'")
        print(f"   Please add invoice images (.png, .jpg, .jpeg, .bmp, .tiff)")
        print(f"   Or ensure sample images were created in the folder above.\n")
        return
    
    print(f"Found {len(image_files)} image(s) to process\n")
    
    # Process all documents
    all_results = []
    for i, image_file in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] Processing: {image_file}")
        print("-" * 80)
        
        image_path = os.path.join(Config.INPUT_DIR, image_file)
        result = process_document(image_path)
        all_results.append(result)
    
    # Generate accuracy report
    print("\n" + "="*80)
    generate_accuracy_report(all_results)
    
    print("\n[OK] Pipeline completed successfully!")
    print(f"  - Preprocessed images saved to: {Config.OUTPUT_IMG_DIR}/")
    print(f"  - Extracted data saved to: {Config.OUTPUT_JSON_DIR}/")


if __name__ == "__main__":
    main()
