import pygame
import os

class File():
    """A class that contains the settings of a folder."""
    def __init__(self, path):
        """Initialize a folder."""
        self.path = path
        self.name = os.path.basename(path)
        self.reduced_name = self.name[:10]
        self.image = pygame.image.load(self.get_file_image())
        self.rect = self.image.get_rect()
        self.pos = None
        self.text_color = (30, 30, 30)
        self.bg_color = (230, 230, 230)
        self.font_path = "font.ttf"
        self.font = pygame.font.Font(self.font_path, 9)
        self.get_name_rect()


    def __str__(self):
        return "File"

    def get_name_rect(self):
        self.name_image = self.font.render(self.reduced_name, True, self.text_color, self.bg_color)
        self.name_rect = self.name_image.get_rect()

    def get_name_pos(self):
        self.name_rect.centerx = self.rect.centerx
        self.name_rect.top = self.rect.bottom

    def get_command(self):
        extension = self.name.split(".")[-1]
        extension = self.name.split(".")[-1]
        if "." in self.name:
            if extension == "py":
                return "code " + self.path
            if extension == "rar":
                return "start winrar " + self.path
            if extension in ["mp4","mkv","avi", "mov", "wmv", "flv", "webm", "3gp", "ogg", "ogv", "m4v", "mpg", "mpeg", "mov", "rm", "rmvb", "asf"]:
                return "start vlc " + self.path
            
    
    def get_file_image(self):
        extension = self.name.split(".")[-1]
        if "." in self.name:
            if extension == "py":
                return "images/py.png"
            if extension == "rar":
                return "images/rar.png"
            if extension == "docx":
                return "images/doc.png"
            if extension == "pdf":
                return "images/pdf.png"
            if extension == "xlsx":
                return "images/xlsx.png"
            if extension in ["mp4","mkv","avi", "mov", "wmv", "flv", "webm", "3gp", "ogg", "ogv", "m4v", "mpg", "mpeg", "mov", "rm", "rmvb", "asf"]:
                return "images/video.png"
            if extension in ["jpg", "jpeg","png", "bmp", "tiff", "tif", "raw","svg", "webp", "heif","ico","pnm","pgm","ppm","pbm","hdr","exr","jfif"]:
                return "images/photo.png"
            if extension == "txt":
                return "images/txt.png"
            else:
                return "images/file.png"
        else:
            return "images/file.png"