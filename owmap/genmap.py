import os
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

# TODO: Have palette be imported from yaml files instead of hard-coded
TERRAIN = {
    (0, 128, 0): "TERRAIN_LUSH",
    (255, 200, 0): "TERRAIN_ARID",
    (255, 255, 0): "TERRAIN_SAND",
    (0, 255, 0): "TERRAIN_TEMPERATE",
    (222, 222, 222): "TERRAIN_TUNDRA",
    (0, 222, 111): "TERRAIN_MARSH",
    (222, 0, 111): "TERRAIN_URBAN",
    (0, 0, 128): "TERRAIN_WATER",
    (0,0,0) : "Unknown"
}
HEIGHT = {
    (222, 222, 222): "HEIGHT_MOUNTAIN",  
    (144, 144, 144): "HEIGHT_HILL",      
    (111, 111, 111): "HEIGHT_FLAT",      
    (0, 255, 255): "HEIGHT_LAKE",     
    (0, 111, 255): "HEIGHT_COAST",       
    (0, 0, 255): "HEIGHT_OCEAN",    
    (255, 0, 0): "HEIGHT_VOLCANO" 
}
VEGET = {
    (0, 90, 0): "VEGETATION_TREES",
    (200, 128, 0): "VEGETATION_SCRUB",
}

def generate_donut_map(path='.', size=128):
    """Generate a donut-shaped map with concentric circles of different terrain types."""
    # --------------------------- TERRAIN ---------------------------
    terrain = Image.new('RGB', (size, size), (0, 0, 128))  # ocean
    draw = ImageDraw.Draw(terrain)
    
    center = size // 2
    outer_radius = int(size * 0.4)
    middle_radius = int(size * 0.3)
    inner_radius = int(size * 0.1)
    
    draw.ellipse([(center-outer_radius, center-outer_radius), 
                  (center+outer_radius, center+outer_radius)], 
                 fill=(255, 200, 0)) 
    
    draw.ellipse([(center-middle_radius, center-middle_radius), 
                  (center+middle_radius, center+middle_radius)], 
                 fill=(0, 128, 0))
    
    draw.ellipse([(center-inner_radius, center-inner_radius), 
                  (center+inner_radius, center+inner_radius)], 
                 fill=(0, 0, 128))
    
    terrain.save(f"{path}/terrain_ex.png")

    #----------------------VEG------------------------------------
    veg = Image.new('RGB', (size, size), (0, 0, 0))  # ocean
    draw = ImageDraw.Draw(veg)
    
    center = size // 2
    outer_radius = int(size * 0.25)
    inner_radius = int(size * 0.12)
    
    draw.ellipse([(center-outer_radius, center-outer_radius), 
                  (center+outer_radius, center+outer_radius)], 
                 fill=(0, 90, 0)) 
    
    draw.ellipse([(center-inner_radius, center-inner_radius), 
                  (center+inner_radius, center+inner_radius)], 
                 fill=(0, 0, 0))
    
    veg.save(f"{path}/veg_ex.png")
    # -----------------HEIGHT--------------------------------------
    height = Image.new('RGB', (size, size), (0, 111, 255))  # ocean
    draw = ImageDraw.Draw(height)
    
    center = size // 2
    outer_radius = int(size * 0.4)
    middle_radius = int(size * 0.3)
    inner_radius = int(size * 0.1)
    
    draw.ellipse([(center-outer_radius, center-outer_radius), 
                  (center+outer_radius, center+outer_radius)], 
                 fill=(144, 144, 144)) 
    
    draw.ellipse([(center-middle_radius, center-middle_radius), 
                  (center+middle_radius, center+middle_radius)], 
                 fill=(111, 111, 111))
    
    draw.ellipse([(center-inner_radius, center-inner_radius), 
                  (center+inner_radius, center+inner_radius)], 
                 fill=(0, 255, 255))
    
    height.save(f"{path}/height_ex.png")

def generate_palette(palette:dict, filename:str):
    """Generate a PNG image with one pixel for each color in the palette."""
    # Create an image with the size of the palette
    fontsize = 8
    height = len(palette) * 8
    width = max(map(lambda s: len(s), palette.values())) * fontsize - fontsize // 2
    img = Image.new('RGB', (width, height), color=(255,255,255))
    draw = ImageDraw.Draw(img)
    fnt = ImageFont.load_default(fontsize)


    # Set pixels
    for y, color, mapping in zip(
        range(0, height, 8), 
        palette.keys(), 
        palette.values()
    ):
        # Rectangle with text beside it    
        draw.rectangle([0, y, 8, y+10], fill=color)
        draw.text((16, y-2), mapping,  font=fnt, fill=(0,0,0))
        print(f"Made {color}:{mapping} at {y}")

    # Save image
    # TODO: Save palette as svg instead of png?
    img.save(filename)

#TODO: IO Operations should be moved to the CLI
def generate_height_palette():
    generate_palette(HEIGHT, './height_palette.png')

def generate_terrain_palette():
    generate_palette(TERRAIN, './terrain_palette.png')

def generate_veg_palette():
    generate_palette(VEGET, './vegetation_palette.png')

def interpret_generic(rgb, tilemap, tolerance=15):
    """
    More generic function, not sure if this is the best way to do it.
    """
    tiletype = tilemap.get(rgb, None)
    if tiletype:
        return tiletype
    
    best_fit = 255, "Unknown"
    for center_rgb, tiletype in tilemap.items():
        # Manhattan distance
        distance = sum(abs(a - b) for a, b in zip(rgb, center_rgb))
        if distance <= tolerance * 3 or distance < best_fit[0]:  # tolerance per channel * 3 channels
            best_fit = distance, tiletype

    return best_fit[1]

# TODO: Implement process_layer to make it modular
def process_layer(imagefile, tilemap) -> ET.ElementTree:
    """Generic version of loop code in process_map_images"""
    ...    

# TODO: Add default value when no layer given so all layers are optional
def process_map_images(height_file, terrain_file, vegetation_file, output_file):
    """Generate an XML map file from input PNG maps."""
    # Open images
    height_img = Image.open(height_file) if height_file else None
    terrain_img = Image.open(terrain_file) if terrain_file else None
    vegetation_img = Image.open(vegetation_file) if vegetation_file else None

    imgs = [height_img, terrain_img, vegetation_img]

    # Check if there are any images to render
    # TODO: Error message / raise for no images given
    if all([not isinstance(img, Image.Image) for img in imgs]): return

    # Ensure all images have the same dimensions
    w,h = imgs[0].size
    if any(img.size != (w, h) for img in imgs if isinstance(img, Image.Image)):
        raise ValueError("All input images must have the same dimensions.")

    # Prepare XML
    root = ET.Element("Root", MapWidth=str(w), MapHeight=str(h), MapEdgesSafe="False")

    id = 0
    for y in reversed(range(h)):
        for x in range(w):
            # Create tile element
            tile = ET.SubElement(root, "Tile", ID=str(id))

            # Terrain
            if terrain_img:
                terrain_rgb = terrain_img.getpixel((x, y))[:3]  # RGB tuple
                terrain = interpret_generic(terrain_rgb, TERRAIN)
                ET.SubElement(tile, "Terrain").text = terrain
            
            # Height
            if height_img:
                height_rgb = height_img.getpixel((x, y))[:3]
                height = interpret_generic(height_rgb, HEIGHT)
                if height != "Unknown":
                    ET.SubElement(tile, "Height").text = height


            # Vegetation
            if vegetation_img:
                vegetation_rgb = vegetation_img.getpixel((x, y))[:3]
                vegetation = interpret_generic(vegetation_rgb, VEGET)

                if vegetation != 'Unknown':
                    ET.SubElement(tile, "Vegetation").text = vegetation
            
            
            id+=1

    # Write out to XML doc
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    # Example usage
    generate_donut_map('.', 50)
    generate_height_palette()
    generate_terrain_palette()
    generate_veg_palette()
    process_map_images('height_ex.png', 'terrain_ex.png', 'veg_ex.png', 'newmap.xml')