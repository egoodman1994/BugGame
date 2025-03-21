import pygame

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

def load_and_clean_sprite(path, size=None):
    """Load a sprite, clean its edges, and optionally resize it."""
    try:
        # Load image with alpha channel
        image = pygame.image.load(path).convert_alpha()
        
        # Clean edges
        image = clean_sprite_edges(image)
        
        # Resize if size is specified
        if size:
            image = pygame.transform.scale(image, size)
            
        return image
    except:
        print(f"Could not load image: {path}")
        return None 