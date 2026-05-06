import pygame

class Timer(pygame.sprite.Sprite):
    def __init__(self,center_position, text, font_size, text_rgb):
        self.text = text
        self.font_size=font_size
        self.text_rgb=text_rgb
        self.timer = self.create_surface_with_text(text, font_size, text_rgb)

    def draw(self, screen):
        screen.blit()

    def update(self, time):
        self.timer = self.create_surface_with_text(time, self.font_size, self.text_rgb)

    def create_surface_with_text(self, text, font_size, text_rgb):
        font = pygame.freetype.SysFont("Courier", font_size, bold=True)
        surface, _ = font.render(text=text, fgcolor=text_rgb)
        return surface.convert_alpha()