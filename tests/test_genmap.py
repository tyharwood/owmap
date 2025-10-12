import pytest
from PIL import Image
import tempfile
import os
from owmap.genmap import (
    interpret_rgb_as_terrain,
    interpret_rgb_as_height,
    interpret_rgb_as_vegetation,
    generate_donut_map,
    generate_palette
)

class TestRGBInterpretation:
    """Test class for RGB interpretation functions. """
    
    def test_terrain_interpretation_known_colors(self):
        # Test some basic terrain mappings
        assert interpret_rgb_as_terrain((0, 128, 0)) == "TERRAIN_LUSH"
        assert interpret_rgb_as_terrain((255, 200, 0)) == "TERRAIN_ARID"
        assert interpret_rgb_as_terrain((0, 0, 128)) == "TERRAIN_WATER"
        assert interpret_rgb_as_terrain((0, 255, 0)) == "TERRAIN_TEMPERATE"
    
    def test_terrain_interpretation_unknown_color(self):
        # Test with a color that's not in the terrain map
        assert interpret_rgb_as_terrain((123, 45, 67)) == "Unknown"
        assert interpret_rgb_as_terrain((255, 255, 255)) == "Unknown"
    
    def test_height_interpretation_known_colors(self):
        assert interpret_rgb_as_height((222, 222, 222)) == "HEIGHT_MOUNTAIN"
        assert interpret_rgb_as_height((144, 144, 144)) == "HEIGHT_HILL"
        assert interpret_rgb_as_height((0, 0, 255)) == "HEIGHT_OCEAN"
        assert interpret_rgb_as_height((255, 0, 0)) == "HEIGHT_VOLCANO"
    
    def test_height_interpretation_unknown_color(self):
        assert interpret_rgb_as_height((100, 200, 50)) == "None"
    
    def test_vegetation_interpretation(self):
        assert interpret_rgb_as_vegetation((0, 90, 0)) == "VEGETATION_TREES"
        assert interpret_rgb_as_vegetation((200, 128, 0)) == "VEGETATION_SCRUB"
        assert interpret_rgb_as_vegetation((255, 255, 255)) == "None"
        assert interpret_rgb_as_vegetation((50, 75, 100)) == "None"


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
