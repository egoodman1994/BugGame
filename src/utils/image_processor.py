import os
import sys
import pygame

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    # Make sure to handle the assets directory correctly
    if relative_path.startswith("assets/"):
        return os.path.join(base_path, relative_path)
    return os.path.join(base_path, "assets", relative_path)

def clean_sprite_edges(surface):
    """Remove any remaining border artifacts from PNG sprites."""
    # Create a new surface with alpha
    cleaned = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    
    # Get pixel array of both surfaces
    pixels = pygame.PixelArray(surface)
    
    # Process each pixel
    width, height = surface.get_size()
    for x in range(width):
        for y in range(height):
            pixel = pixels[x, y]
            alpha = (pixel >> 24) & 0xFF
            # Make semi-transparent pixels either fully transparent or opaque
            if alpha < 200:
                cleaned.set_at((x, y), (0, 0, 0, 0))
            else:
                cleaned.set_at((x, y), surface.get_at((x, y)))
    
    del pixels  # Release the surface lock
    return cleaned

def load_and_clean_sprite(image_path, size):
    try:
        path = get_resource_path(f"images/{image_path}")
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None 