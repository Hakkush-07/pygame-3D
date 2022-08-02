import pygame
from pygame.locals import *
import sys
from display.colors import *
from display.player import Player
from core.camera import Camera

class App:
    FPS = 120

    def __init__(self, objects=None):
        pygame.init()
        info = pygame.display.Info()
        self.w = info.current_w
        self.h = info.current_h
        self.window = pygame.display.set_mode((self.w, self.h), FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        self.player = Player()
        self.objects = objects if objects else []
        self.timer = 0
    
    def to_window_tuple(self, window_point):
        """
        converts WindowPoint to pygame window pixel coordinates
        """
        return window_point.x * self.w + 0.5 * self.w, -window_point.y * self.w + 0.5 * self.h
    
    def handle_quit(self):
        """
        handles quit events, esc key and exit button
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def draw_things(self):
        """
        draws objects on the window
        """
        self.window.fill(LIGHT_BLUE)
        for obj in self.objects:
            # draw faces
            for polygon in obj.faces:
                f = self.camera.render_polygon(polygon)
                if f:
                    clipped_f = f.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_f:
                        pygame.draw.polygon(self.window, YELLOW, [self.to_window_tuple(p) for p in clipped_f.vertices])
            # draw edges
            for line in obj.edges:
                l = self.camera.render_line(line)
                if l:
                    clipped_l = l.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_l:
                        clipped_p1, clipped_p2 = clipped_l
                        pygame.draw.line(self.window, BLACK, self.to_window_tuple(clipped_p1), self.to_window_tuple(clipped_p2))
            # draw corners
            for point in obj.corners:
                p = self.camera.render_point(point)
                if p:
                    clipped_p = p.clipped(-1, -self.h / self.w, 1, self.h / self.w)
                    if clipped_p:
                        pygame.draw.circle(self.window, BLACK, self.to_window_tuple(clipped_p), 3)
        self.window.blit(pygame.font.Font(None, 32).render(str(int(App.FPS)), True, BLACK), (10, 10))
        pygame.display.update()

    def handle_movement(self, dt):
        """
        handles movement based on WASD key presses
        """
        keys = pygame.key.get_pressed()
        a = keys[K_a] - keys[K_d]
        b = keys[K_w] - keys[K_s]
        self.camera.position += self.player.move(a, b, dt, self.camera.rotation.a)
    
    def handle_rotation(self, dt):
        """
        handles rotation based on mouse movements
        """
        a, b = pygame.mouse.get_rel()
        self.camera.rotation += self.player.rotate(a, b, dt)
    
    def handle_jump(self, dt):
        """
        handles jumping and space key presses
        """
        space = pygame.key.get_pressed()[K_SPACE]
        self.camera.position += self.player.jump(space, dt)
        if self.camera.position.z < 0:
            self.player.end_jump()
            self.camera.position.z = 0
    
    def time_calculations(self):
        fps = self.clock.get_fps()
        dt = self.clock.tick() * 0.001
        self.timer += dt
        # update fps every second
        if self.timer > 1:
            self.timer = 0
            App.FPS = fps if fps else 120
        return dt

    def run(self):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        while True:
            dt = self.time_calculations()
            self.handle_quit()
            self.draw_things()
            self.handle_movement(dt)
            self.handle_rotation(dt)
            self.handle_jump(dt)
            
