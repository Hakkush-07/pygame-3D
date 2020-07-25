import pygame, sys, random
from pygame.locals import *
from math import sin, cos, tan, sqrt, pi
from DisplayCalc import *

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

# Setting Screen
info = pygame.display.Info()
WINDOW_SIZE = (info.current_w, info.current_h)
WINDOW = pygame.display.set_mode(WINDOW_SIZE, FULLSCREEN)
pygame.display.set_caption('3D Shooter')
FPS = pygame.time.Clock()

w, h = int(WINDOW_SIZE[0] / 2), int(WINDOW_SIZE[1] / 2)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
LIGHTBLUE = (100, 100, 255)
WHITEBLUE = (200, 200, 255)
DARKBLUE = (0, 0, 100)
DARKGRAY = (40, 40, 40)
GRAY = (150, 150, 150)
MING = (15, 108, 118)

# Loading images and sounds
bg_image = pygame.image.load("files/bg.png")
cursor = pygame.image.load("files/cursor.png")
sens = pygame.image.load("files/sensitivity.png")
music_on = pygame.image.load("files/music-on.png")
music_off = pygame.image.load("files/music-off.png")
hit_sound = pygame.mixer.Sound("files/explosion.wav")
self_hit = pygame.mixer.Sound("files/self_hit.wav")
shoot_sound = pygame.mixer.Sound("files/shoot.wav")
death_sound = pygame.mixer.Sound("files/death.wav")

# Setting fonts
title_font = pygame.font.Font("files/Roboto-Thin.ttf", 100)
button_font = pygame.font.Font("files/IndieFlower.ttf", 40)
by_font = pygame.font.Font("files/DancingScript-Regular.ttf", 30)
credit_font = pygame.font.Font("files/Walkway.ttf", 40)
write_font = pygame.font.Font("files/CutiveMono-Regular.ttf", 80)
instructions_font = pygame.font.Font("files/CutiveMono-Regular.ttf", 30)

# ground grid
grid = 4
segments = [(i, j, 0, i, j + 1, 0) for i in range(-grid, grid + 1) for j in range(-grid, grid)] + \
           [(j, i, 0, j + 1, i, 0) for i in range(-grid, grid + 1) for j in range(-grid, grid)]

instruction = ["WASD --> move",
               "Mouse or arrows --> direction",
               "Left click or SPACE --> shoot",
               "CTRL --> sprint",
               "C --> focus",
               "T and Y --> FOV",
               "M --> music",
               "N --> hit animation",
               "ESC --> pause or exit"
               ]


class Text:
    def __init__(self, text, color, font, centerx, centery):
        """
        Parameters
        ----------
        text : text string
        color : color of the text
        font : font of the text
        centerx : x of text center
        centery : y of text center
        """
        self.text = text
        self.color = color
        self.font = font
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.x, self.y = centerx, centery

    def draw(self):
        """Draws the text on screen."""
        self.rect.center = (self.x, self.y)
        WINDOW.blit(self.surface, self.rect)


class Button:
    """
    A class used to represent buttons

    Attributes
    ----------
    text : text of the button
    text_color : color of the text
    color : color of the button
    text_font : font of the text
    width : width of the button
    height : height of the button
    centerx : x of button center
    centery : y of button center

    Methods
    -------
    draw()
        Draws the button on screen
    over()
        Shows if mouse is over the button
    """
    def __init__(self, text, text_color, color, text_font, width, height, centerx, centery):
        """
        Parameters
        ----------
        text : text of the button
        text_color : color of the text
        color : color of the button
        text_font : font of the text
        width : width of the button
        height : height of the button
        centerx : x of button center
        centery : y of button center
        """
        self.text = text
        self.text_color = text_color
        self.color = color
        self.width, self.height = width, height
        self.bg = pygame.Rect(0, 0, self.width, self.height)
        self.shadow = pygame.Rect(0, 0, self.width, self.height)
        self.frame = pygame.Rect(0, 0, self.width, self.height)
        self.font = text_font
        self.surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.surface.get_rect()
        self.x, self.y = centerx, centery
        self.dark_color = tuple(map(lambda x: max(0, x - 40), self.color))

    def over(self):
        """Shows if mouse is over the button."""
        mx, my = pygame.mouse.get_pos()
        if self.x - int(self.width / 2) < mx < self.x + int(self.width / 2) and self.y - int(self.height / 2) < my < self.y + int(self.height / 2):
            return True
        else:
            return False

    def draw(self):
        """Draws the button on screen."""
        self.rect.center = (self.x, self.y)
        self.bg.center = (self.x, self.y)
        self.shadow.center = (self.x - 10, self.y + 10)
        self.frame.center = (self.x, self.y)
        pygame.draw.rect(WINDOW, BLACK, self.shadow)
        if self.over():
            pygame.draw.rect(WINDOW, self.dark_color, self.bg)
        else:
            pygame.draw.rect(WINDOW, self.color, self.bg)
        pygame.draw.rect(WINDOW, BLACK, self.frame, 2)
        WINDOW.blit(self.surface, self.rect)


class Ball:
    """
    A class used to represent bullet balls

    Attributes
    ----------
    sx : starting point x
    sy : starting point y
    sz : starting point z
    fx : finishing point x
    fy : finishing point y
    fz : finishing point z
    ball_type : shows who shoots the ball

    Methods
    -------
    draw()
        Draws the ball on screen with current position
    distance()
        Returns squared distance of the ball to player
    """
    def __init__(self, sx, sy, sz, fx, fy, fz, ball_type):
        """
        Parameters
        ----------
        sx : starting point x
        sy : starting point y
        sz : starting point z
        fx : finishing point x
        fy : finishing point y
        fz : finishing point z
        ball_type : shows who shoots the ball
        """
        self.sx, self.sy, self.sz, self.fx, self.fy, self.fz = sx, sy, sz, fx, fy, fz
        self.a = 0
        self.cx, self.cy, self.cz = self.sx, self.sy, self.sz
        self.ball_type = ball_type

    def increase(self):
        self.a += 0.01

    def draw(self):
        """Draws the ball on screen with current position."""
        self.cx, self.cy, self.cz = self.sx + self.a * (self.fx - self.sx), self.sy + self.a * (self.fy - self.sy), self.sz + self.a * (self.fz - self.sz)
        control = get_point_coordinate(dxy, dz, posx, posy, posz, self.cx, self.cy, self.cz, fovd, w, h)
        distance = sqrt((posx - self.cx)**2 + (posy - self.cy)**2 + (posz - self.cz)**2)
        r = min(15/(distance + 0.001) + 5, 20)
        if control:
            pygame.draw.circle(WINDOW, BLACK, control, int(r))

    def distance(self):
        """Returns squared distance of the ball to player."""
        return (posx - self.cx) ** 2 + (posy - self.cy) ** 2 + (posz - self.cz) ** 2


class Enemy:
    """
    A class used to represent enemy cubes

    Attributes
    ----------
    color : color of the enemy in RGB
    shoot_rate : shot frequency of the enemy

    Methods
    -------
    draw()
        Draws the enemy on screen
    shoot()
        Creates a Ball object from enemy towards player
    collision_check(bx, by, bz, ball_type)
        Checks if the enemy is hit by the player
    distance()
        Returns squared distance of the enemy to player
    """
    def __init__(self, color, shoot_rate):
        """
        Parameters
        ----------
        color : color of the enemy in RGB
        shoot_rate : shot frequency of the enemy
        """
        self.x, self.y, self.z = random.uniform(-3, 3), random.uniform(-3, 3), 0.25
        self.color = color
        self.shoot_rate = shoot_rate
        self.sr = 0

    def draw(self):
        """Draws the enemy on screen."""
        if get_point_coordinate(dxy, dz, posx, posy, posz, self.x, self.y, self.z, fovd, w, h, 0.2):
            enemy_corners = [(self.x + i, self.y + j, self.z + k) for i in (-0.25, 0.25) for j in (-0.25, 0.25) for k in (-0.25, 0.25)]
            enemy_segments = [(x1, y1, z1, x2, y2, z2) for x1, y1, z1 in enemy_corners for x2, y2, z2 in enemy_corners if [x1-x2, y1-y2, z1-z2].count(0) == 2]
            a1, a2, a3, a4, a5, a6 = self.x-0.25, self.x+0.25, self.y-0.25, self.y+0.25, 0, 0.5
            enemy_surfaces = [(a1, a3, a5, a1, a4, a5, a1, a4, a6, a1, a3, a6),
                              (a2, a3, a5, a2, a4, a5, a2, a4, a6, a2, a3, a6),
                              (a1, a3, a5, a2, a3, a5, a2, a3, a6, a1, a3, a6),
                              (a1, a4, a5, a2, a4, a5, a2, a4, a6, a1, a4, a6),
                              (a1, a3, a5, a2, a3, a5, a2, a4, a5, a1, a4, a5),
                              (a1, a3, a6, a2, a3, a6, a2, a4, a6, a1, a4, a6)
                              ]
            for ix, iy, iz, jx, jy, jz, kx, ky, kz, lx, ly, lz in enemy_surfaces:
                control1 = get_point_coordinate(dxy, dz, posx, posy, posz, ix, iy, iz, fovd, w, h)
                control2 = get_point_coordinate(dxy, dz, posx, posy, posz, jx, jy, jz, fovd, w, h)
                control3 = get_point_coordinate(dxy, dz, posx, posy, posz, kx, ky, kz, fovd, w, h)
                control4 = get_point_coordinate(dxy, dz, posx, posy, posz, lx, ly, lz, fovd, w, h)
                if control1 and control2 and control3 and control4:
                    pygame.draw.polygon(WINDOW, self.color, (control1, control2, control3, control4))
            for ix, iy, iz, jx, jy, jz in enemy_segments:
                control = get_segment_coordinate(dxy, dz, posx, posy, posz, ix, iy, iz, jx, jy, jz, fovd, w, h)
                if control:
                    x1, y1, x2, y2 = control[0], control[1], control[2], control[3]
                    pygame.draw.line(WINDOW, BLACK, (x1, y1), (x2, y2), 1)

    def shoot(self):
        """Creates a Ball from the enemy towards player."""
        if music:
            shoot_sound.play()
        return Ball(self.x, self.y, self.z, posx, posy, posz, "enemy")

    def collision_check(self, bx, by, bz, ball_type):
        """Checks if the enemy is hit by player."""
        if ball_type == "player" and self.x - 0.25 < bx < self.x + 0.25 and self.y - 0.25 < by < self.y + 0.25 and self.z - 0.25 < bz < self.z + 0.25:
            return True
        else:
            return False

    def distance(self):
        """Returns squared distance of the enemy to player."""
        return (posx - self.x) ** 2 + (posy - self.y) ** 2 + (posz - self.z) ** 2


def draw_instructions():
    """Draws instruction card."""
    s = pygame.Surface((560, 360))
    s.set_alpha(128)
    s.fill(BLACK)
    WINDOW.blit(s, (10, 180))
    if 10 < pygame.mouse.get_pos()[0] < 570 and 180 < pygame.mouse.get_pos()[1] < 540:
        for i in range(len(instruction)):
            j = instruction[i]
            j_text = Text(j, YELLOW, instructions_font, 280, 200 + i * 40)
            j_text.draw()
    else:
        j_text = Text("Instructions", YELLOW, write_font, 290, 360)
        j_text.draw()


def draw_mouse_sensitivity():
    """Draws mouse sensitivity setting."""
    mouse_sensitivity = Text("Mouse Sensitivity: " + str(sensitivity), WHITE, button_font, w + 360, h - 80)
    mouse_sensitivity.draw()
    pygame.draw.line(WINDOW, WHITE, (w + 198, h - 20), (w + 522, h - 20), 3)
    for i in range(7):
        j = 54
        pygame.draw.line(WINDOW, WHITE, (w + 200 + j * i, h - 30), (w + 200 + j * i, h - 10), 2)
    WINDOW.blit(sens, (w + 198 + round((sensitivity - 0.8) * 54 / 0.4) - 15, h - 20 - 25))


def draw_menu(buttons):
    """Draws menu page."""
    name = Text("3D Shooter", WHITE, title_font, w, 100)
    name.draw()
    by = Text("by", WHITE, by_font, w, 2 * h - 100)
    by.draw()
    credit = Text("Hakan Karakus", WHITE, credit_font, w, 2 * h - 50)
    credit.draw()
    draw_mouse_sensitivity()
    draw_instructions()
    for button in buttons:
        button.draw()


def draw_win(buttons):
    """Draws win page."""
    score_text = Text("Score: " + str(score), BLACK, pygame.font.Font(None, 100), w, h - 40)
    score_text.draw()
    thanks_text = Text("Thanks for playing", BLACK, write_font, w, 120)
    thanks_text.draw()
    diff_text = Text("Difficulty: " + difficulty, BLACK, pygame.font.Font(None, 100), w, 250)
    diff_text.draw()
    for button in buttons:
        button.draw()


def draw_ground():
    """Draws ground grid"""
    for ix, iy, iz, jx, jy, jz in segments:
        control = get_segment_coordinate(dxy, dz, posx, posy, posz, ix, iy, iz, jx, jy, jz, fovd, w, h)
        if control:
            x1, y1, x2, y2 = control[0], control[1], control[2], control[3]
            pygame.draw.line(WINDOW, BLACK, (x1, y1), (x2, y2), 1)


def draw_game_things():
    """Draws cursor, score, health, music icon."""
    WINDOW.blit(cursor, (w - 12, h - 12))
    score_text = Text("Score: " + str(score), BLACK, pygame.font.Font(None, 40), 2 * w - 100, 40)
    score_text.draw()
    health_text = Text("Health: " + str(max(health, 0)), RED, pygame.font.Font(None, 40), 100, 40)
    health_text.draw()
    if music:
        music_pic = music_on
    else:
        music_pic = music_off
    if anim:
        pass
    else:
        pass
    WINDOW.blit(music_pic, (20, 2 * h - 70))


def diff_settings(difficulty):
    """Returns the decreasing speed of enemy_spawn_rate and a constant for the ending point of enemy_spawn_rate."""
    if difficulty == "Easy":
        dff = 0.03
        esr = 0
    elif difficulty == "Medium":
        dff = 0.05
        esr = 1
    elif difficulty == "Hard":
        dff = 0.08
        esr = 2
    return dff, esr


def set_speed():
    """Sets speed"""
    if sprinting:
        speed = sprs
    elif health > 0:
        speed = ms
    else:
        speed = ms / 4
    return speed


def focus_mode():
    """Magnifies the screen or takes it back."""
    global fov_decrease, fov_increase, fovd
    if fov_decrease:
        fov_decrease = False
        fovd -= 200
    if fov_increase:
        fov_increase = False
        fovd += 200


def player_shoot():
    """Shoots a ball from player."""
    global cooldown
    if music:
        shoot_sound.play()
    ball_list.append(
        Ball(posx, posy, posz, posx + cos(dxy) * 5, posy + sin(dxy) * 5, posz + tan(dz) * 5,
             "player"))
    cooldown = cooldown_time


def mouse_movement():
    """Changes direction according to mouse movements."""
    global old_mouse_pos, fix_dxy, fix_dz, dxy, dz
    if pygame.mouse.get_pos() == old_mouse_pos:
        fix_dxy, fix_dz = dxy, dz
        pygame.mouse.set_pos(w, h)
    else:
        mx, my = pygame.mouse.get_pos()
        a, b = angles_to_mouse(mx, my, fovd, w, h)
        dxy, dz = fix_dxy + a * sensitivity, fix_dz + b * sensitivity
    old_mouse_pos = pygame.mouse.get_pos()
    if dz < -pi / 2 + 0.01:
        dz = -pi / 2 + 0.01
    elif dz > pi / 2 - 0.01:
        dz = pi / 2 - 0.01


def movement(speed):
    """Changes position of player."""
    global posx, posy
    if moving_forward:
        posx += speed * cos(dxy)
        posy += speed * sin(dxy)
    if moving_left:
        posx -= speed * sin(dxy)
        posy += speed * cos(dxy)
    if moving_back:
        posx -= speed * cos(dxy)
        posy -= speed * sin(dxy)
    if moving_right:
        posx += speed * sin(dxy)
        posy -= speed * cos(dxy)
    if posx < -grid:
        posx = -grid
    if posx > grid:
        posx = grid
    if posy < -grid:
        posy = -grid
    if posy > grid:
        posy = grid


def direction():
    """Changes direction of player."""
    global dxy_increasing, dxy_decreasing, dz_increasing, dz_decreasing, dxy, dz
    if dxy_increasing:
        dxy += ds
    if dxy_decreasing:
        dxy -= ds
    if dz_increasing:
        dz += ds
    if dz_decreasing:
        dz -= ds


def f():
    """Returns objects to draw on screen and balls to remove."""
    global score, health, player_hit
    objects_to_draw = []
    balls_to_remove = []
    for enemy in enemies:
        objects_to_draw.append(enemy)
        enemy.sr += 1
        if enemy.sr == enemy.shoot_rate:
            ball_list.append(enemy.shoot())
            enemy.sr = 0

    for i in range(len(ball_list)):
        ball = ball_list[i]
        objects_to_draw.append(ball)
        ball.increase()
        if ball.a > 2:
            balls_to_remove.append(i)
        for enemy in enemies:
            if enemy.collision_check(ball.cx, ball.cy, ball.cz, ball.ball_type):
                if music:
                    hit_sound.play()
                enemies.remove(enemy)
                balls_to_remove.append(i)
                score += 1
        if ball.ball_type == "enemy" and posx - 0.35 < ball.cx < posx + 0.35 and posy - 0.35 < ball.cy < posy + 0.35 and posz - 0.35 < ball.cz < posz + 0.35:
            balls_to_remove.append(i)
            player_hit = True
            health -= random.randint(15, 25)
            if health > 0 and music:
                self_hit.play()
            elif health <= 0 and music:
                death_sound.play()
    return objects_to_draw, balls_to_remove


def enemy_spawn_control(esr, dff):
    """Creates an enemy in every enemy_spawn_rate frame and decreases enemy_spawn_rate gradually."""
    global enemy_spawn_count, enemy_spawn_rate
    enemy_spawn_count += 1
    if enemy_spawn_count > enemy_spawn_rate:
        enemies.append(Enemy(get_random_color(), int(enemy_spawn_rate / 3)))
        enemy_spawn_count = 0
    if enemy_spawn_rate > 120 - 30 * esr:
        enemy_spawn_rate -= dff


def play_menu_music():
    """Plays menu music."""
    pygame.mixer.music.load("files/menu_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)


def play_game_music():
    """Plays game music."""
    pygame.mixer.music.load("files/game_music.wav")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.7)


def get_random_color():
    """Returns a random color for enemies."""
    return random.choice([RED, GREEN, BLUE, YELLOW])


def terminate():
    """Terminates the game."""
    pygame.quit()
    sys.exit()


def main():
    global main_page, game_page, win_page, pause_page, dxy, dz, posx, posy, posz, fovd, ds, ms, sprs, \
        moving_forward, moving_left, moving_back, moving_right, dxy_increasing, dxy_decreasing, dz_increasing, dz_decreasing, \
        sprinting, fov_increase, fov_decrease, ball_list, player_hit_animation, player_hit, anim, health, death_screen, \
        score, enemy_spawn_rate, enemy_spawn_count, enemies, difficulty, cooldown, cooldown_time, music, pause_first, \
        old_mouse_pos, fix_dxy, fix_dz, sensitivity, objects_to_draw
    main_page, game_page, win_page, pause_page = True, False, False, False
    dxy, dz, posx, posy, posz, fovd = 0, 0, 0, 0, 1, 350
    ds, ms, sprs = 0.01, 0.02, 0.04
    moving_forward, moving_left, moving_back, moving_right = False, False, False, False
    dxy_increasing, dxy_decreasing, dz_increasing, dz_decreasing = False, False, False, False
    sprinting, fov_increase, fov_decrease = False, False, False
    ball_list = []
    player_hit_animation, player_hit, anim = 90, False, True
    health, death_screen = 100, 0
    score = 0
    enemy_spawn_rate = 600
    enemy_spawn_count = 0
    enemies = []
    difficulty = "Easy"
    cooldown, cooldown_time = 0, 60
    music = True
    pause_first = True
    old_mouse_pos, fix_dxy, fix_dz = (w, h), dxy, dz
    sensitivity = 2.0

    play_menu_music()
    while True:
        if main_page:
            start_button = Button("Start", WHITE, MING, button_font, 150, 100, w, 300)
            difficulty_button = Button(difficulty, WHITE, MING, button_font, 150, 100, w, 450)
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and start_button.over():
                        game_page, main_page, win_page = True, False, False
                        pygame.mouse.set_pos(w, h)
                        play_game_music()
                    elif event.button == 1 and difficulty_button.over():
                        if difficulty == "Hard":
                            difficulty = "Easy"
                        elif difficulty == "Easy":
                            difficulty = "Medium"
                        elif difficulty == "Medium":
                            difficulty = "Hard"
                    elif h - 40 < event.pos[1] < h and w + 171 < event.pos[0] < w + 549:
                        t = event.pos[0] - w - 171
                        t = int(t / 54)
                        sensitivity = round(0.8 + t * 0.4, 1)
                    else:
                        print(event.pos)
            WINDOW.blit(bg_image, (0, 0))
            draw_menu([start_button, difficulty_button])
            dff, esr = diff_settings(difficulty)
            pygame.display.update()
        if game_page:
            pygame.mouse.set_visible(False)
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause_page, game_page = True, False
                    elif event.key == K_UP:
                        dz_increasing = True
                    elif event.key == K_DOWN:
                        dz_decreasing = True
                    elif event.key == K_LEFT:
                        dxy_increasing = True
                    elif event.key == K_RIGHT:
                        dxy_decreasing = True
                    elif event.key == K_w:
                        moving_forward = True
                    elif event.key == K_a:
                        moving_left = True
                    elif event.key == K_s:
                        moving_back = True
                    elif event.key == K_d:
                        moving_right = True
                    elif event.key == K_t:
                        fovd -= 10
                    elif event.key == K_y:
                        fovd += 10
                    elif event.key == K_LCTRL:
                        sprinting = True
                    elif event.key == K_c:
                        fov_increase = True
                    elif event.key == K_SPACE and cooldown <= 0:
                        player_shoot()
                    elif event.key == K_m:
                        if music:
                            music = False
                            pygame.mixer.music.pause()
                        else:
                            music = True
                            pygame.mixer.music.unpause()
                    elif event.key == K_n:
                        if anim:
                            anim = False
                        else:
                            anim = True
                elif event.type == KEYUP:
                    if event.key == K_UP:
                        dz_increasing = False
                    elif event.key == K_DOWN:
                        dz_decreasing = False
                    elif event.key == K_LEFT:
                        dxy_increasing = False
                    elif event.key == K_RIGHT:
                        dxy_decreasing = False
                    elif event.key == K_w:
                        moving_forward = False
                    elif event.key == K_a:
                        moving_left = False
                    elif event.key == K_s:
                        moving_back = False
                    elif event.key == K_d:
                        moving_right = False
                    elif event.key == K_LCTRL:
                        sprinting = False
                    elif event.key == K_c:
                        fov_decrease = True
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and cooldown <= 0:
                        player_shoot()
            mouse_movement()
            speed = set_speed()
            focus_mode()
            movement(speed)
            direction()
            WINDOW.fill(WHITEBLUE)
            draw_ground()
            objects_to_draw, balls_to_remove = f()
            for i in balls_to_remove:
                ball_list.pop(i)
            objects_to_draw.sort(key=lambda x: -x.distance())
            if health > 0:
                for object in objects_to_draw:
                    object.draw()
            else:
                death_screen += 10
                s = pygame.Surface((2 * w, 2 * h))
                s.set_alpha(death_screen)
                s.fill(RED)
                WINDOW.blit(s, (0, 0))
                if death_screen == 250:
                    game_page, win_page = False, True
            if player_hit:
                if anim:
                    player_hit_animation -= 1
                    s = pygame.Surface((2 * w, 2 * h))
                    s.set_alpha(player_hit_animation)
                    s.fill(RED)
                    WINDOW.blit(s, (0, 0))
                    if player_hit_animation == 1:
                        player_hit_animation, player_hit = 90, False
                else:
                    player_hit = False
            draw_game_things()
            enemy_spawn_control(esr, dff)
            if cooldown > 0:
                cooldown -= 1
            pygame.display.update()
        if win_page:
            pygame.mouse.set_visible(True)
            menu_button = Button("Main Menu", WHITE, MING, button_font, 200, 100, w, 500)
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        terminate()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and menu_button.over():
                        play_menu_music()
                        main_page, game_page, win_page, pause_page = True, False, False, False
                        dxy, dz, posx, posy, posz, fovd = 0, 0, 0, 0, 1, 350
                        ds, ms, sprs = 0.01, 0.02, 0.04
                        moving_forward, moving_left, moving_back, moving_right = False, False, False, False
                        dxy_increasing, dxy_decreasing, dz_increasing, dz_decreasing = False, False, False, False
                        sprinting, fov_increase, fov_decrease = False, False, False
                        ball_list = []
                        player_hit_animation, player_hit, anim = 90, False, True
                        health, death_screen = 100, 0
                        score = 0
                        enemy_spawn_rate = 600
                        enemy_spawn_count = 0
                        enemies = []
                        difficulty = "Easy"
                        cooldown, cooldown_time = 0, 60
                        music = True
                        pause_first = True
                        old_mouse_pos, fix_dxy, fix_dz = (w, h), dxy, dz
                        objects_to_draw = []
            WINDOW.fill(RED)
            draw_win([menu_button])
            pygame.display.update()
        if pause_page:
            pygame.mouse.set_visible(True)
            if pause_first:
                s = pygame.Surface((2 * w, 2 * h))
                s.set_alpha(128)
                s.fill(BLUE)
                WINDOW.blit(s, (0, 0))
                pause_first = False
            resume_button = Button("Resume", WHITE, MING, button_font, 200, 100, w, 200)
            menu_button = Button("Menu", WHITE, MING, button_font, 200, 100, w, 350)
            exit_button = Button("Exit", WHITE, MING, button_font, 200, 100, w, 500)
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause_page, game_page = False, True
                        pause_first = True
                        pygame.mouse.set_pos(w, h)
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if resume_button.over():
                            pause_page, game_page = False, True
                            pause_first = True
                            pygame.mouse.set_pos(w, h)
                        elif menu_button.over():
                            play_menu_music()
                            main_page, game_page, win_page, pause_page = True, False, False, False
                            dxy, dz, posx, posy, posz, fovd = 0, 0, 0, 0, 1, 350
                            ds, ms, sprs = 0.01, 0.02, 0.04
                            moving_forward, moving_left, moving_back, moving_right = False, False, False, False
                            dxy_increasing, dxy_decreasing, dz_increasing, dz_decreasing = False, False, False, False
                            sprinting, fov_increase, fov_decrease = False, False, False
                            ball_list = []
                            player_hit_animation, player_hit, anim = 90, False, True
                            health, death_screen = 100, 0
                            score = 0
                            enemy_spawn_rate = 600
                            enemy_spawn_count = 0
                            enemies = []
                            difficulty = "Easy"
                            cooldown, cooldown_time = 0, 60
                            music = True
                            pause_first = True
                            old_mouse_pos, fix_dxy, fix_dz = (w, h), dxy, dz
                            objects_to_draw = []
                        elif exit_button.over():
                            terminate()
            resume_button.draw()
            menu_button.draw()
            exit_button.draw()
            pygame.display.update()
        FPS.tick(60)


if __name__ == '__main__':
    main()

