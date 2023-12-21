import pygame
import sys
import os
import shutil
import subprocess
import json
import hashlib
import id1fs_functions as id1fs


def hash_string(input_string):
    """Hash a string using SHA-256."""
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode('utf-8'))
    return sha256_hash.hexdigest()

def check_events(desktop, settings, side_screen, login_screen):
    """Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_DOWN:
                for icon in desktop.icon_places:
                    icon.y = icon.y - desktop.icon_size
                desktop.icons_get_pos()
            elif event.key == pygame.K_UP:
                for icon in desktop.icon_places:
                    icon.y = icon.y + desktop.icon_size
                desktop.icons_get_pos()
            if event.key == pygame.K_n:
                if settings.ctrl and settings.shift :
                    count = 0
                    while True:
                        try:
                            if count == 0:
                                os.mkdir(os.path.join(desktop.path,"New_Folder"))
                            else:
                                os.mkdir(os.path.join(desktop.path,f"New_Folder({count})"))
                            break
                        except FileExistsError:
                            count = count + 1
                    desktop.Initialize_desktop()
                if settings.ctrl and not settings.shift:
                    count = 0
                    while True:
                        try:
                            if count == 0:
                                with open(os.path.join(desktop.path,"New file.txt"),"x"):
                                    pass
                                if settings.ID1FS:
                                    id1fs.create_file_backup(os.path.join(desktop.path,f"New_File.txt"))
                            else:
                                with open(os.path.join(desktop.path,f"New_File({count}).txt"),"x"):
                                   pass
                                if settings.ID1FS:
                                    id1fs.create_file_backup(os.path.join(desktop.path,f"New_File({count}).txt"))
                                    
                            break
                        except FileExistsError:
                            count = count + 1
                    desktop.Initialize_desktop()
            if event.key == pygame.K_DELETE:
                if settings.selected_file != None:
                    os.remove(settings.selected_file.path)
                    settings.selected_file = None
                    desktop.Initialize_desktop()
                if settings.hover_icon != None and str(settings.hover_icon) == "File":
                    os.remove(settings.hover_icon.path)
                    settings.hover_icon = None
                    desktop.Initialize_desktop()
                if settings.hover_icon != None and str(settings.hover_icon) == "Folder" and settings.shift:
                    shutil.rmtree(settings.hover_icon.path)
                    settings.hover_icon = None
                    desktop.Initialize_desktop()
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                settings.ctrl = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                settings.shift = True
            if settings.changing_name == True:
                if event.key == pygame.K_RETURN:
                    try:
                        os.rename(settings.changing_name_icon.path, os.path.join(desktop.path,settings.name))
                    except OSError:
                        pass
                    settings.changing_name = False
                    settings.changing_name_icon = None
                    desktop.Initialize_desktop()
                elif event.key == pygame.K_BACKSPACE:
                    settings.name = settings.name[:-1]
                else:
                    settings.name += event.unicode
            if login_screen.login == True or login_screen.register:
                if login_screen.entering_username == True:
                    if event.key == pygame.K_RETURN:
                        login_screen.entering_username = False
                        login_screen.entering_password = True
                    elif event.key == pygame.K_BACKSPACE:
                        login_screen.username = login_screen.username[:-1]
                        settings.username = settings.username[:-1]
                    else:
                        login_screen.username += event.unicode
                        settings.username += event.unicode
                    login_screen.render_username()
                elif login_screen.entering_password == True:
                    if event.key == pygame.K_RETURN:
                        login_screen.entering_password = False
                        login_screen.password = ""
                        login_screen.username = ""
                        login_screen.render_username()
                        if login_screen.login:
                            check_login(desktop,settings,side_screen, login_screen)
                        elif login_screen.register:
                            add_user(settings ,login_screen)
                    elif event.key == pygame.K_BACKSPACE:
                        login_screen.password = login_screen.password[:-1]
                        settings.password = settings.password[:-1]
                    else:
                        login_screen.password += "*"
                        settings.password += event.unicode
                    login_screen.render_password()
                        
            if event.key == pygame.K_r and settings.ctrl and settings.shift and settings.hover_icon != None:
                settings.changing_name = True
                settings.changing_name_icon = settings.hover_icon
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                settings.ctrl = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                settings.shift = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for folder in desktop.folders:
                if folder.rect.collidepoint(mouse_x,mouse_y):
                    if folder == settings.hover_icon:
                        settings.hover_icon.text_color = settings.text_color
                        settings.hover_icon.bg_color = settings.bg_color
                        settings.hover_icon.get_name_rect()
                        settings.hover_count = 0
                        settings.hover_icon = None
                    settings.selected_folder = folder
            for file in desktop.files:
                if file.rect.collidepoint(mouse_x,mouse_y):
                    settings.selected_file = file
            
        if event.type == pygame.MOUSEBUTTONUP:
            if not settings.clicked:
                settings.clicked = True
            elif settings.clicked_count < 300:
                try:
                    if str(settings.selected_folder) == "Folder": 
                        os.listdir(settings.selected_folder.path)
                        desktop.path = settings.selected_folder.path
                        settings.selected_folder = None
                        desktop.Initialize_desktop()
                    if str(settings.selected_file) == "File": 
                        command = "start notepad " + settings.selected_file.path
                        subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                except PermissionError:
                            print("Permission denied.")
                settings.clicked = False
                settings.clicked_count = 0
            if settings.selected_folder != None:
                collisions_folder(desktop, settings)
                if settings.selected_folder != None:
                    settings.selected_folder.rect.center = desktop.icon_places[settings.selected_folder.x].center
                    settings.selected_folder = None
            if settings.selected_file != None:
                collisions_file(desktop,settings)
                if settings.selected_file !=None:
                    settings.selected_file.rect.center = desktop.icon_places[settings.selected_file.x].center
                    settings.selected_file = None
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if side_screen.before_rect.collidepoint(mouse_x,mouse_y):
                path = desktop.path
                if not settings.ID1FS:
                    desktop.path = os.path.dirname(path)
                    desktop.Initialize_desktop()
                elif "C:\\Users\\Oussama\\Documents\\Deskrop_env\\ID1FS" in os.path.dirname(path):
                    desktop.path = os.path.dirname(path)
                    desktop.Initialize_desktop()
            if side_screen.home_rect.collidepoint(mouse_x,mouse_y):
                desktop.path = "C:\\Users\\Oussama"
                desktop.Initialize_desktop()
            elif  side_screen.ID1FS == False and side_screen.id1fs_rect.collidepoint(mouse_x,mouse_y):
                settings.login = True
                settings.password = ""
                settings.username = ""
            elif login_screen.login == False and login_screen.login_button_image_rect.collidepoint(mouse_x,mouse_y):
                login_screen.login = True
                login_screen.entering_username = True
            elif side_screen.ID1FS and side_screen.id1fs_logout_rect.collidepoint(mouse_x,mouse_y):
                settings.ID1FS = False
                side_screen.ID1FS = False
                desktop.path = "C:\\Users\\Oussama\\Documents\\Deskrop_env"
                desktop.Initialize_desktop()
            elif login_screen.login == False and login_screen.register_button_image_rect.collidepoint(mouse_x,mouse_y):
                login_screen.register = True
                login_screen.entering_username = True


def check_login(desktop,settings,side_screen, login_screen):  
    login_screen.login = False
    with open("system/login.json","r") as f:
        users = json.load(f)
    if settings.username in users.keys():
        if users[settings.username] == hash_string(settings.password):
            print("Logged in")
            settings.login = False
            settings.ID1FS = True
            side_screen.ID1FS = True
            desktop.path = "C:\\Users\\Oussama\\Documents\\Deskrop_env\\ID1FS\\home"
            desktop.Initialize_desktop()
        else:
            print("Wrong password")
            settings.login = False
    else:
        print("Wrong username")
            
def add_user(settings ,login_screen):
    login_screen.register = False
    with open("system/login.json","r") as f:
        users = json.load(f)
    if settings.username in users.keys():
        pass
    else:
        users[settings.username] = hash_string(settings.password)
        with open("system/login.json","w") as f:
            json.dump(users,f,indent=4)
    settings.login = False



def hover_icon(desktop, settings):
    if not settings.login:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if settings.hover_icon == None:
            for folder in desktop.folders:
                if folder.rect.collidepoint(mouse_x,mouse_y) and folder != settings.selected_folder:
                    folder.text_color = (222,222,222)
                    folder.bg_color = settings.hover_color
                    folder.get_name_rect()
                    settings.hover_icon = folder
                    settings.name = folder.name
                    break
        if settings.hover_icon == None:
            for file in desktop.files:
                if file.rect.collidepoint(mouse_x,mouse_y) and file != settings.selected_file:
                    file.text_color = (0,0,0)
                    file.bg_color = settings.hover_color
                    file.get_name_rect()
                    settings.hover_icon = file
                    settings.name = file.name
                    break

def inhover_icon(desktop, settings):
    if not settings.login:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if settings.hover_icon != None:
            if settings.hover_icon.rect.collidepoint(mouse_x,mouse_y):
                settings.hover_count= settings.hover_count +1
            else:
                settings.hover_icon.text_color = settings.text_color
                settings.hover_icon.bg_color = settings.bg_color
                settings.hover_icon.get_name_rect()
                settings.hover_count = 0
                settings.hover_icon = None

def check_double_click(settings):
    if settings.clicked:
        settings.clicked_count = settings.clicked_count + 1
        if settings.clicked_count > 300:
            settings.clicked = False
            settings.clicked_count = 0

def collisions_file(desktop,settings):
    if settings.selected_file != None:
        for file in desktop.files :
            if file != settings.selected_file:
                if file.rect.colliderect(settings.selected_file.rect):
                    temp = settings.selected_file.x
                    settings.selected_file.x = file.x 
                    file.x = temp
                    desktop.icons_get_pos()
                    break
        for folder in desktop.folders:
            if folder.rect.colliderect(settings.selected_file.rect):
                shutil.move(settings.selected_file.path,folder.path)
                desktop.Initialize_desktop()
                settings.selected_file = None
                break

def collisions_folder(desktop, settings):
    if settings.selected_folder != None:
        for folder in desktop.folders:
            if folder != settings.selected_folder:
                if folder.rect.colliderect(settings.selected_folder.rect):
                    try:
                        shutil.move(settings.selected_folder.path,folder.path)
                        desktop.Initialize_desktop()
                    except shutil.Error:
                        pass
                    break



def moving_icons(settings):
    if settings.selected_folder != None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        settings.selected_folder.rect.center = mouse_x, mouse_y
    if settings.selected_file != None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        settings.selected_file.rect.center = mouse_x, mouse_y
  
    

def draw_screen(screen, settings, desktop, side_screen, login_screen):
    """Draw the screen."""
    screen.fill(settings.bg_color)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if not settings.login:
        for place in desktop.icon_places:
            if place.collidepoint(mouse_x,mouse_y):
                pygame.draw.rect(screen, settings.hover_color, place)
                break
    desktop.blitme()
    if settings.hover_count > 400 and settings.changing_name == False:
        font_path = "font.ttf"
        font = pygame.font.Font(font_path, 10)
        name_image = font.render(settings.name, True, settings.name_color, settings.name_bg)
        name_rect = name_image.get_rect()
        name_rect.bottom = screen.get_rect().bottom
        name_rect.left = side_screen.side_rect.right
        screen.blit(name_image, name_rect)
    if settings.changing_name:
        font_path = "font.ttf"
        font = pygame.font.Font(font_path, 10)
        name_image = font.render(settings.name, True, settings.name_color, settings.name_bg)
        name_rect = name_image.get_rect()
        name_rect.bottomleft = screen.get_rect().bottomleft
        screen.blit(name_image, name_rect)
    side_screen.draw()
    if settings.login == True:
        login_screen.draw()
    pygame.display.flip()