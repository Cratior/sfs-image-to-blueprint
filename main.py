import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import json

# Open file explorer to select black and white image
root = tk.Tk()
root.withdraw()
image_path = filedialog.askopenfilename(title="Select Black and White Image")

# Load the image and convert it to black and white
image = Image.open(image_path).convert("1")

# Create a blank blueprint
blueprint = {
    "center": 10.0,
    "parts": [],
    "stages": [],
    "rotation": 0.0,
    "offset": {"x": 0.0, "y": 0.0},
    "interiorView": True
}

# Define the scaling factor for the output
scaling_factor = 0.5  # Adjust this value as desired

# Extract the black outlines from the image
draw = ImageDraw.Draw(image)
width, height = image.size
pixels = image.load()

for y in range(height):
    for x in range(width):
        if pixels[x, y] == 0:  # black pixel
            # Add fuel tank at the position of the black pixel with scaling
            scaled_x = x * scaling_factor
            scaled_y = (height - y - 1) * scaling_factor
            fuel_tank = {
                "n": "Fuel Tank",
                "p": {"x": float(scaled_x), "y": float(scaled_y)},
                "o": {"x": 1.0, "y": 1.0, "z": 0.0},
                "t": "-Infinity",
                "N": {
                    "width_original": 2.0,
                    "width_a": 2.0,
                    "width_b": 2.0,
                    "height": 1.0,
                    "fuel_percent": 1.0
                },
                "T": {"color_tex": "_", "shape_tex": "_"}
            }
            blueprint["parts"].append(fuel_tank)

# Save the modified blueprint to a file
output_file = "blueprint.txt"
with open(output_file, "w") as f:
    json.dump(blueprint, f, indent=4)

print(f"Modified blueprint saved to {output_file}")
