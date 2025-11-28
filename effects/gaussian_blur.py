from pygame.transform import smoothscale
from pygame import Surface

def gaussian_blur(surface, radius) -> Surface:
    width, height = surface.get_size()
    small_size = (max(1, width // radius), max(1, height // radius))
    scaled_surface = smoothscale(surface, small_size)
    blurred_surface = smoothscale(scaled_surface, (width, height))
    return blurred_surface