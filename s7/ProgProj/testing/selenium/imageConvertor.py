import base64
from PIL import Image
from io import BytesIO

# Sample Base64 encoded image data
base64_image_data = "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"

# Decode Base64 and save the image
image_data = base64.b64decode(base64_image_data)
image = Image.open(BytesIO(image_data))

# Save the image as a file
image_path = "image.png"
image.save(image_path)

print("Image saved as", image_path)
