import pygame
from pygame import Vector3, Vector2

WHITE = (255, 255, 255)
RED = (137, 18, 20)
BLUE = (13, 72, 172)
ORANGE = (255, 85, 37)
GREEN = (25, 155, 76)
YELLOW = (254, 213, 47)
GRAY = (128, 128, 128)

pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Rotating Cube')
clock = pygame.time.Clock()

# Corner-points of a cube
p1 = Vector3(+1, +1, +1)
p2 = Vector3(-1, +1, +1)
p3 = Vector3(-1, -1, +1)
p4 = Vector3(+1, -1, +1)
p5 = Vector3(+1, +1, -1)
p6 = Vector3(-1, +1, -1)
p7 = Vector3(-1, -1, -1)
p8 = Vector3(+1, -1, -1)
points = [p1, p2, p3, p4, p5, p6, p7, p8]

# Surfaces/Faces of the cube defined in terms of points
# Normal to the surface is sequence of the points and
# direction is obtained by right-hand thumb rule.
s1 = (p1, p2, p3, p4)
s2 = (p8, p7, p6, p5)
s3 = (p5, p6, p2, p1)
s4 = (p4, p3, p7, p8)
s5 = (p1, p4, p8, p5)
s6 = (p3, p2, p6, p7)
surfaces = [s1, s2, s3, s4, s5, s6]

# Colors corresponding to the surfaces.
colors = [WHITE, YELLOW, BLUE, GREEN, RED, ORANGE]

# Center and Scale of the Cube.
OFFSET = (250, 250)
SCALE = (100, 100)


def surface2poly(surf):
    """
        This function takes a surface/face and maps it to the 2d surface. In this case projects 3D surface
        onto plane defined by z=0, (x-y plane).
        This function also scales and offsets the points according to globally defined constants.
    """
    return [Vector2(p.x * SCALE[0] , p.y * SCALE[1]) + OFFSET for p in surf]


def if_draw_surface(surf):
    """
        This function determines whether a surface must be mapped to the 2D plane or not
        depending on the orientation of the surface.
        This function works hand-in hand with surface2poly and is dependent on how it is implemented.
    """
    return (surf[1] - surf[0]).cross(surf[2] - surf[1]).z > 0


# Main simulation loop of pygame
run = True
# Indicates is mouse is being dragged (moved with a mouse key pressed)
dragging = False

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Rotating the cube using mouse movements
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Obtains values relative to the previous call
            # Initial call is ignored to setup reference
            pygame.mouse.get_rel()
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        if event.type == pygame.MOUSEMOTION:
            if dragging:
                # Rotate points based on how much mouse has moved.
                # TODO: Later if possible move based on where mouse is.
                x, y = pygame.mouse.get_rel()
                for p in points:
                    p.rotate_x_ip(-y)
                    p.rotate_y_ip(x)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x] or keys[pygame.K_c] or keys[pygame.K_ESCAPE]:
        # Quit the simulation of Pressing K or C
        run = False

    # Rotate the Cube based on inputs from the Keyboard
    # by rotating the corner points of the cube accordingly
    if keys[pygame.K_w] or keys[pygame.K_UP]:
       for p in points:
           p.rotate_x_ip(1)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        for p in points:
            p.rotate_x_ip(-1)

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        for p in points:
            p.rotate_y_ip(-1)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        for p in points:
            p.rotate_y_ip(1)

    if keys[pygame.K_q] or keys[pygame.K_LEFTBRACKET]:
        for p in points:
            p.rotate_z_ip(-1)
    if keys[pygame.K_e] or keys[pygame.K_RIGHTBRACKET]:
        for p in points:
            p.rotate_z_ip(1)

    # Set the background color to GRAY.
    win.fill(GRAY)

    # Draw the surfaces to the screen
    for s, c in zip(surfaces, colors):
        if if_draw_surface(s):
            pygame.draw.polygon(win, c, surface2poly(s))


    pygame.display.update()
pygame.quit()