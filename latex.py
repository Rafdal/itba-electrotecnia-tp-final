import tex2pix
from PIL import Image
import io

# Define the LaTeX expression
expr = r"\frac{1}{2}\int_0^\infty x^2 e^{-x} dx"

# Render LaTeX expression as image data buffer
data = tex2pix.Renderer(expr).mkpng()

# Create PIL image from image data buffer
img = Image.open(io.BytesIO(data))

# Display the image
img.show()