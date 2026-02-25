# Contributing to OCR Pipeline with Tesseract

First off, thank you for considering contributing to this project! 🎉

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots and animated GIFs if possible**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and existing functionality**
- **Explain the expected improvement and its benefit**

### Pull Requests

- Fill in the required template
- Follow the Python PEP 8 style guide
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ocr-pipeline-tesseract.git
cd ocr-pipeline-tesseract

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install pylint pytest pytest-cov black flake8
```

## Style Guide

### Python Code Style

We follow PEP 8 with these guidelines:

```python
# Good
def load_image(image_path):
    """Load an image from file.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        PIL.Image: Loaded image or None
    """
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print(f"Error loading {image_path}: {e}")
        return None

# Bad
def load_image(path):
    img = Image.open(path)
    return img
```

### Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add OCR preprocessing for rotation correction

- Implement image rotation detection
- Add automatic rotation correction
- Improve accuracy for rotated documents

Fixes #123
```

### Documentation

- Add docstrings to all functions
- Keep comments clear and concise
- Update README.md for user-facing changes
- Update SETUP.txt for installation changes

## Testing

Before submitting a pull request:

```bash
# Check code style
pylint ocr_pipeline.py
flake8 ocr_pipeline.py

# Format code
black ocr_pipeline.py

# Run tests (if added)
pytest tests/
```

## Additional Notes

### Issue and Pull Request Labels

- **bug** - Something isn't working
- **enhancement** - New feature or request
- **documentation** - Improvements or additions to documentation
- **good first issue** - Good for newcomers
- **help wanted** - Extra attention is needed
- **in progress** - Currently being worked on
- **question** - Further information is requested

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

## Questions?

Feel free to open an issue with the label `question` or contact us through GitHub discussions.

Thank you for contributing! 🎊
