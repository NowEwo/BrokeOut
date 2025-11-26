import pygame

def gaussian_blur(surface, radius):
    width, height = surface.get_size()
    small_size = (max(1, width // radius), max(1, height // radius))
    scaled_surface = pygame.transform.smoothscale(surface, small_size)
    blurred_surface = pygame.transform.smoothscale(scaled_surface, (width, height))
    return blurred_surface