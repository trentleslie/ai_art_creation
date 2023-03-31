from collections import Counter
from PIL import Image
import sys

def rank_colors(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")
    
    # Reduce the number of colors in the image to 256 using the `quantize` method
    #img = img.quantize(colors=256, method=2)
    
    pixels = img.getdata()
    
    color_counts = Counter(pixels)
    ranked_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
    
    return [color for color, count in ranked_colors]

def set_color_transparent(image_path, rank, output_path):
    ranked_colors = rank_colors(image_path)
    
    if rank > len(ranked_colors):
        print(f"Rank {rank} not found in the image, the highest rank is {len(ranked_colors)}")
        sys.exit(1)
    
    img = Image.open(image_path)
    img = img.convert("RGBA")
    
    # Reduce the number of colors in the image to 256 using the `quantize` method
    #img = img.quantize(colors=256, method=2)
    
    target_color = ranked_colors[:rank]
    new_pixels = [(255, 255, 255, 0) if pixel in target_color else pixel for pixel in img.getdata()]
    
    img.putdata(new_pixels)
    img.save(output_path)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <image_path> <rank> <output_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    rank = int(sys.argv[2])
    output_path = sys.argv[3]
    
    set_color_transparent(image_path, rank, output_path)
    print(f"New image saved as {output_path}")
