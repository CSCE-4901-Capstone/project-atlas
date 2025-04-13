import os
import requests
from PIL import Image
from io import BytesIO

API_KEY = "317c3f3999ad90c494695b155a43932d"
ZOOM = 2  # zoom level (2^2 = 4x4 tiles)
TILE_SIZE = 256
LAYER = 'temp_new'
PALETTE = '-98:4200ff;0:0061ff;15:00d5ff;21:a0ddff;23:ffffff;25:ffffcc;30:ffff00;40:ff8000;60:ff0000'
OUTPUT_PATH = os.path.join("client", "public", "images", "stitched_weather.png")


def stitch_weather_map():
    width = TILE_SIZE * 2**ZOOM
    height = TILE_SIZE * 2**ZOOM
    stitched = Image.new('RGBA', (width, height))

    for x in range(2**ZOOM):
        for y in range(2**ZOOM):
            url = (
                f"https://tile.openweathermap.org/map/{LAYER}/{ZOOM}/{x}/{y}.png"
                f"?appid={API_KEY}&palette={PALETTE}"
            )
            print(f"Fetching tile {x},{y} -> {url}")
            try:
                response = requests.get(url)
                response.raise_for_status()
                tile = Image.open(BytesIO(response.content)).convert("RGBA")
                stitched.paste(tile, (x * TILE_SIZE, y * TILE_SIZE))
            except Exception as e:
                print(f"Error fetching tile {x},{y}: {e}")

    stitched.save(OUTPUT_PATH)
    print(f"Saved stitched weather map to: {OUTPUT_PATH}")


if __name__ == "__main__":
    stitch_weather_map()
