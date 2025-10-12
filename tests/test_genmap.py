import pytest
from PIL import Image
import tempfile
import os
from owmap.genmap import (
    interpret_generic,
    generate_donut_map,
    generate_palette,
    HEIGHT,
    TERRAIN,
    VEGET,
)

class TestRGBInterpretation:
    """Test class for RGB interpretation functions. """
    
    def test_terrain_interpretation_known_colors(self):
        # Test some basic terrain mappings
        assert interpret_generic((0, 128, 0), TERRAIN) == "TERRAIN_LUSH"
        assert interpret_generic((255, 200, 0), TERRAIN) == "TERRAIN_ARID"
        assert interpret_generic((0, 0, 128), TERRAIN) == "TERRAIN_WATER"
        assert interpret_generic((0, 255, 0), TERRAIN) == "TERRAIN_TEMPERATE"
    
    def test_terrain_interpretation_unknown_color(self):
        # Test with a color that's not in the terrain map
        assert interpret_generic((123, 45, 67), TERRAIN) == "Unknown"
        assert interpret_generic((255, 255, 255), TERRAIN) == "Unknown"
    
    def test_height_interpretation_known_colors(self):
        assert interpret_generic((222, 222, 222), HEIGHT) == "HEIGHT_MOUNTAIN"
        assert interpret_generic((144, 144, 144), HEIGHT) == "HEIGHT_HILL"
        assert interpret_generic((0, 0, 255), HEIGHT) == "HEIGHT_OCEAN"
        assert interpret_generic((255, 0, 0), HEIGHT) == "HEIGHT_VOLCANO"
    
    def test_height_interpretation_unknown_color(self):
        assert interpret_generic((100, 200, 50), HEIGHT) == "Unknown"
    
    def test_vegetation_interpretation(self):
        assert interpret_generic((0, 90, 0), VEGET) == "VEGETATION_TREES"
        assert interpret_generic((200, 128, 0), VEGET) == "VEGETATION_SCRUB"
        assert interpret_generic((255, 255, 255), VEGET) == "Unknown"
        assert interpret_generic((50, 75, 100), VEGET) == "Unknown"


class TestImageGeneration:
    """Test class for image generation functions."""
    # TODO: Rewrite donutgen unit test
    def test_generate_donut_map_creates_file(self):
        """Test that generate_donut_map creates a PNG file."""
        ...
    
    def test_generate_palette_creates_correct_image(self):
        """Test that generate_palette creates the correct palette image."""
        # Create a small test palette
        test_palette = {
            (255, 0, 0): "Red",    # Red
            (0, 255, 0): "Green",  # Green  
            (0, 0, 255): "Blue"    # Blue
        }
        
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            temp_path = tmp.name
        
        try:
            generate_palette(test_palette, temp_path)
            
            # Verify the generated image
            assert os.path.exists(temp_path)
            img = Image.open(temp_path)
            
            # Should be 3 pixels wide (one for each color), 1 pixel tall
            assert img.size == (3, 1)
            assert img.mode == 'RGB'
            
            # Check that the colors are correct
            assert img.getpixel((0, 0)) == (255, 0, 0)  # Red
            assert img.getpixel((1, 0)) == (0, 255, 0)  # Green
            assert img.getpixel((2, 0)) == (0, 0, 255)  # Blue
            
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
