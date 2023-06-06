from flask import Flask, request, send_file
from PIL import Image, ImageDraw
import json
import io

app = Flask(__name__)

@app.route('/generate_blueprint', methods=['POST'])
def generate_blueprint():
    image = Image.open(request.files['image']).convert("1")
    scaling_factor = float(request.form['scale'])

    blueprint = {
        "center": 10.0,
        "parts": [],
        "stages": [],
        "rotation": 0.0,
        "offset": {"x": 0.0, "y": 0.0},
        "interiorView": True
    }

    draw = ImageDraw.Draw(image)
    width, height = image.size
    pixels = image.load()

    for y in range(height):
        for x in range(width):
            if pixels[x, y] == 0:  # black pixel
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

    output_file = io.BytesIO()
    with open(output_file, "w") as f:
        json.dump(blueprint, f, indent=4)

    output_file.seek(0)
    return send_file(output_file, as_attachment=True, attachment_filename="blueprint.txt")

if __name__ == '__main__':
    app.run()
