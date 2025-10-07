import os
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

def generate_donut_map(path='donut.png', size=128):
    """Generate a donut-shaped map with concentric circles of different terrain types."""
    img = Image.new('RGB', (size, size), (255, 255, 255))  # ocean
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    outer_radius = int(size * 0.4)
    middle_radius = int(size * 0.3)
    inner_radius = int(size * 0.1)
    
    # Draw circles from largest to smallest
    draw.ellipse([(center-outer_radius, center-outer_radius), 
                  (center+outer_radius, center+outer_radius)], 
                 fill=(255, 255, 255)) 
    
    draw.ellipse([(center-middle_radius, center-middle_radius), 
                  (center+middle_radius, center+middle_radius)], 
                 fill=(0, 255, 0))
    
    draw.ellipse([(center-inner_radius, center-inner_radius), 
                  (center+inner_radius, center+inner_radius)], 
                 fill=(255, 255, 255))
    
    img.save(path)

def generate_palette(palette, filename):
    """Generate a PNG image with one pixel for each color in the palette."""
    # Create an image with the size of the palette
    width = len(palette)
    height = 1  # One row of pixels
    img = Image.new('RGB', (width, height))

    # Set pixels
    for x, color in enumerate(palette.keys()):
        # TODO: Add a label for each color in the palette
        img.putpixel((x, 0), color)

    # Save image
    # TODO: Save palette as svg instead of png
    img.save(filename)

#TODO: Rewrite interpret_generic or impl. process_layer
# Not amenable to current pipeline, rewrite or impl. process_layer
def interpret_generic(rgb, tilemap, tolerance=15):
    """
    More generic function, not sure if this is the best way to do it.
    """
    tiletype = tilemap.get(rgb, "Unknown")
    
    if tiletype != "Unknown" and tiletype != "None": 
        return tiletype

    for center_rgb, tiletype in tilemap.items():
        # Manhattan distance (faster than Euclidean)
        distance = sum(abs(a - b) for a, b in zip(rgb, center_rgb))
        if distance <= tolerance * 3:  # tolerance per channel * 3 channels
            return tiletype
    
    return "Unknown"

# Define mappings for terrain, height, vegetation, and rivers
def interpret_rgb_as_terrain(rgb):
    """Map RGB values to terrain types."""
    terrain_map = {
        (0, 128, 0): "TERRAIN_LUSH",
        (255, 200, 0): "TERRAIN_ARID",
        (255, 255, 0): "TERRAIN_SAND",
        (0, 255, 0): "TERRAIN_TEMPERATE",
        (222, 222, 222): "TERRAIN_TUNDRA",
        (0, 0, 0): "TERRAIN_URBAN",
        (0, 0, 128): "TERRAIN_WATER"
    }
    return terrain_map.get(rgb, "Unknown")

def interpret_rgb_as_height(rgb):
    """Map RGB values to height levels."""
    height_map = {
        (222, 222, 222): "HEIGHT_MOUNTAIN",  
        (144, 144, 144): "HEIGHT_HILL",      
        (111, 111, 111): "HEIGHT_FLAT",      
        (0, 222, 255): "HEIGHT_LAKE",     
        (0, 111, 255): "HEIGHT_COAST",       
        (0, 0, 255): "HEIGHT_OCEAN",    
        (255, 0, 0): "HEIGHT_VOLCANO" 
    }
    return height_map.get(rgb, "None") 

def interpret_rgb_as_vegetation(rgb):
    """Map RGB values to vegetation types."""
    vegetation_map = {
        (0, 255, 0): "VEGETATION_TREES",
        (0, 128, 0): "VEGETATION_SCRUB",
        (255,255,255): "None"
    }
    return vegetation_map.get(rgb, "None")

#TODO: Implement process_layer to make it modular
def process_layer():
    """Generic version of loop code in process_map_images"""
    ...    

def process_map_images(terrain_file, height_file, vegetation_file, output_file):
    """Generate an XML map file from input PNG maps."""
    # Open images
    terrain_img = Image.open(terrain_file)
    height_img = Image.open(height_file)
    vegetation_img = Image.open(vegetation_file)

    # Ensure all images have the same dimensions
    w, h = terrain_img.size
    if any(img.size != (w, h) for img in [height_img, vegetation_img]):
        raise ValueError("All input images must have the same dimensions.")

    # Prepare XML structure
    root = ET.Element("Root", MapWidth=str(w), MapHeight=str(h), MapEdgesSafe="False")

    id = 0
    for y in reversed(range(h)):
        for x in range(w):
            # Get pixel data
            terrain_rgb = terrain_img.getpixel((x, y))[:3]  # RGB tuple
            height_rgb = height_img.getpixel((x, y))[:3]
            vegetation_rgb = vegetation_img.getpixel((x, y))[:3]

            # Interpret pixel data
            terrain = interpret_rgb_as_terrain(terrain_rgb)
            height = interpret_rgb_as_height(height_rgb)
            vegetation = interpret_rgb_as_vegetation(vegetation_rgb)

            # Create tile element
            tile = ET.SubElement(root, "Tile", ID=str(id))
            ET.SubElement(tile, "Terrain").text = terrain
            ET.SubElement(tile, "Height").text = height
            if vegetation:
                ET.SubElement(tile, "Vegetation").text = vegetation
            id+=1
    # Write to output file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

# Example usage
if __name__ == "__main__":
    terrain_file = "docs/terrainmap.png"
    height_file = "docs/heightmap.png"
    vegetation_file = "docs/vegmap.png"
    output_file = "docs/map.xml"

    process_map_images(terrain_file, height_file, vegetation_file, output_file)
    #generate_donut_map('docs/donut.png')