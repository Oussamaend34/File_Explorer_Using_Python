import pygame

class SideScreen():
    """Initialize the settings for the side screen."""
    def __init__(self, screen):
        self.screen = screen
        self.bg_color = (60,70,120)
        self.side_rect = pygame.Rect(0, 0, 200, 620)
        self.before_color = (120,60,90)
        self.before_rect = pygame.Rect(0,20,90,50)
        self.after_rect = pygame.Rect(110,20,90,50)
        self.home_rect = pygame.Rect(0,80,200,50)
        self.id1fs_rect = pygame.Rect(0,140,200,50)
        self.id1fs_logout_rect = pygame.Rect(0,140,200,50)
        self.ID1FS = False


    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.side_rect)
        pygame.draw.rect(self.screen, self.before_color, self.before_rect)
        pygame.draw.rect(self.screen, self.before_color, self.home_rect)
        if self.ID1FS:
            pygame.draw.rect(self.screen, self.before_color, self.id1fs_rect)
        else:
            pygame.draw.rect(self.screen, self.before_color, self.id1fs_logout_rect)