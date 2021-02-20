try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def read_image(image):
    text = pytesseract.image_to_string(Image.open(image))
    return text