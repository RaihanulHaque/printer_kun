from pdf2image import convert_from_path
from PIL import Image
import numpy as np

def rgb_to_cmyk(image):
    """Convert an RGB image to CMYK and return CMYK percentages."""
    image = image.convert("RGB")  # Ensure RGB mode
    r, g, b = np.array(image).astype(float).transpose((2, 0, 1)) / 255.0
    
    c = 1 - r
    m = 1 - g
    y = 1 - b
    k = np.minimum(c, np.minimum(m, y))
    
    c = (c - k) / (1 - k + 1e-10)  # Avoid division by zero
    m = (m - k) / (1 - k + 1e-10)
    y = (y - k) / (1 - k + 1e-10)
    
    # Compute percentage of each component in the image
    total_pixels = image.size[0] * image.size[1]
    
    c_percent = np.sum(c) / total_pixels * 100
    m_percent = np.sum(m) / total_pixels * 100
    y_percent = np.sum(y) / total_pixels * 100
    k_percent = np.sum(k) / total_pixels * 100
    
    return {
        "cyan": round(c_percent, 2),
        "magenta": round(m_percent, 2),
        "yellow": round(y_percent, 2),
        "black": round(k_percent, 2),
    }


image_path = "/Users/rahi/Code/printer_kun/ng.png"
# pdf_path = "/Users/rahi/Code/printer_kun/Lab 01.pdf"
image = Image.open(image_path)
cmyk_distribution = rgb_to_cmyk(image)

# pages = convert_from_path(pdf_path)

# Show the CMYK distribution
print(cmyk_distribution)