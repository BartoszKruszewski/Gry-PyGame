import pygame,math

def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf

def rotCenter(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def getAngle(x,y):
    if y <= 0 or x <= 0:
        return 0
    return int(math.degrees(math.atan(x/y)))

def split_lines(text,max_l):
    words = text.split(" ")
    lines = []
    line = ""
    next_line_word = ""
    for word in words:
        line += next_line_word
        next_line_word = ""
        if len(word) > 3:
            line += word + " "
            if len(line) >= max_l - 1 or word == words[-1]:
                lines.append(line[:-1])
                line = ""
        else:
            if len(line) >= max_l - 4:
                next_line_word = word + " "
                lines.append(line[:-1])
                line = ""
            else:
                line += word + " "



    return lines

def getRect(surf,pos):
    rect = surf.get_rect(center = pos)
    return rect

def liveBar(actual_state,size,color,graduation = 0):
    surf = pygame.Surface(size)
    surf.fill((0,0,0))
    surf.fill((255,255,255),(1,1,size[0]-2,size[1]-2))
    surf.fill(color, (1, 1, min(int((size[0] - 2) * actual_state),size[0]-2), size[1] - 2))
    surf.set_colorkey((255,255,255))

    GRAD_DIST = 100
    if graduation != 0:
        dist = GRAD_DIST / graduation * (size[0]-2)
        for i in range(1,int((size[0] - 2) * actual_state / dist) + 1):
            if int(i * dist) < size[0]-2:
                surf.fill((0,0,0),(int(i * dist),1,1,size[1] - 2))

    return surf

def change_pallete(surf,color1,color2):
    new_surf = surf.copy()
    w = surf.get_width()
    h = surf.get_height()
    for y in range(h):
        for x in range(w):
            if surf.get_at((x,y)) == color1:
                new_surf.set_at((x,y),color2)
    return new_surf



