from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import json

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

def analyze_pdf(pdf_path):
    """Extract pages from a PDF and analyze CMYK color distribution."""
    pages = convert_from_path(pdf_path)
    results = {}
    
    for i, page in enumerate(pages, start=1):
        cmyk_distribution = rgb_to_cmyk(page)
        results[f"Page {i}"] = cmyk_distribution
    
    return results

# Example usage:
pdf_file = "/Users/rahi/Code/printer_kun/Lab 01.pdf"  # Replace with your PDF file path
cmyk_results = analyze_pdf(pdf_file)
# Save results to a JSON file
with open("cmyk_results.json", "w") as f:
    json.dump(cmyk_results, f, indent=4)
# print(cmyk_results)
