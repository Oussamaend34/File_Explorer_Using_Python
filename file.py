import pygame
import os
import json

class File():
    """A class that contains the settings of a folder."""
    def __init__(self, path):
        """Initialize a folder."""
        self.path = path
        self.name = os.path.basename(path)
        self.reduced_name = self.name[:10]
        self.image = self.get_file_image()
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
            
    
    def get_file_type(self):
        extension = self.name.split(".")[-1]
        if "." in self.name:
            if extension == "py":
                return "python"
            if extension == "rar":
                return "winrar"
            if extension == "docx":
                return "word"
            if extension == "pdf":
                return "pdf"
            if extension == "xlsx":
                return "excel"
            if extension in ["mp4","mkv","avi", "mov", "wmv", "flv", "webm", "3gp", "ogg", "ogv", "m4v", "mpg", "mpeg", "mov", "rm", "rmvb", "asf"]:
                return "video"
            if extension in ["jpg", "jpeg","png", "bmp", "tiff", "tif", "raw","svg", "webp", "heif","ico","pnm","pgm","ppm","pbm","hdr","exr","jfif"]:
                return "photo"
            if extension == "txt":
                return "txt"
            if extension == "c":
                return "c"
            if extension == "cpp":
                return "c"
            if extension == "json":
                return "json"
            if extension == "exe":
                return "exe"
            if extension == "ppt":
                return "ppt"
            else:
                return "file"
        else:
            return "file"
    def get_file_image(self):
        type = self.get_file_type()
        if type == "photo":
            original_image = pygame.image.load(self.path)
            resized_image = pygame.transform.scale(original_image, (64, 64))
            return resized_image
        else:
            with open("system/files.json") as f:
                files = json.load(f)
            return pygame.image.load(os.path.join("images",files[type]))