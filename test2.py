from pdf2image import convert_from_path
from PIL import Image
import numpy as np


def rgb_to_cmyk_visual(image):
    """Convert an RGB image to CMYK and return both CMYK percentages and channel images."""
    image = image.convert("RGB")  # Ensure RGB mode
    r, g, b = np.array(image).astype(float).transpose((2, 0, 1)) / 255.0
    
    # Convert to CMYK
    c = 1 - r
    m = 1 - g
    y = 1 - b
    k = np.minimum(c, np.minimum(m, y))
    
    c = (c - k) / (1 - k + 1e-10)
    m = (m - k) / (1 - k + 1e-10)
    y = (y - k) / (1 - k + 1e-10)

    # Convert back to 0-255 range for visualization
    c_img = Image.fromarray((c * 255).astype(np.uint8))
    m_img = Image.fromarray((m * 255).astype(np.uint8))
    y_img = Image.fromarray((y * 255).astype(np.uint8))
    k_img = Image.fromarray((k * 255).astype(np.uint8))

    return {
        "cyan": c_img,
        "magenta": m_img,
        "yellow": y_img,
        "black": k_img
    }

# Example usage:
pdf_file = "/Users/rahi/Code/printer_kun/Lab 01.pdf"  # Replace with your file
pages = convert_from_path(pdf_file)

# Convert first page for visualization
cmyk_images = rgb_to_cmyk_visual(pages[0])

# Display the CMYK channel images
for color, img in cmyk_images.items():
    img.show(title=color)  # Opens each image separately
