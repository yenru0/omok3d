import pygame
import numpy as np

from function.pane import BoardRect


class OmokPan:
    def __init__(self, size):
        self.size = size
        self.pan = np.zeros(size, dtype=np.uint8)
        self.turn_now = 1
        pad = 6
        spacing = 10
        self.board_rects = [BoardRect(pad + z * (20 * 14 + spacing), pad * 4, self.size[1:], (20, 20))
                            for z in range(self.size[0])]

        # using in to be functional
        self.moving: int = None

    def pass_turn(self):
        if self.turn_now == 1:
            self.turn_now = 2
        else:
            self.turn_now = 1

    def check(self):
        """
        :return: 0 None, 1: if player 1 win, 2: if player 2 win
        """

        for z in range(self.size[0]):
            # x axis(1) length check
            for x in range(self.size[1] - 4):
                for y in range(self.size[2]):
                    t = self.pan[z, x:x + 5, y]
                    if np.all(t == 1):
                        return 1
                    elif np.all(t == 2):
                        return 2
            # y axis(2) length check
            for x in range(self.size[1]):
                for y in range(self.size[2] - 4):
                    t = self.pan[z, x, y: y + 5]
                    if np.all(t == 1):
                        return 1
                    elif np.all(t == 2):
                        return 2
        for z in range(self.size[0] - 4):
            for x in range(self.size[1]):
                for y in range(self.size[2]):
                    t = self.pan[z: z + 5, x, y]
                    if np.all(t == 1):
                        return 1
                    elif np.all(t == 2):
                        return 2
        # x-y diagonal (with)
        for z in range(self.size[0]):
            for i in range(-(self.size[2] - 4 - 1), self.size[1] - 4):
                t = self.pan[z].diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2
                t = np.fliplr(self.pan[z]).diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2

        # x-z diagonal (with)
        for y in range(self.size[2]):
            for i in range(-(self.size[0] - 4 - 1), self.size[1] - 4):
                t = self.pan[:, :, y].diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2
                t = np.fliplr(self.pan[:, :, y]).diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2

        # y-z diagonal (with)
        for x in range(self.size[1]):
            for i in range(-(self.size[0] - 4 - 1), self.size[2] - 4):
                t = self.pan[:, x, :].diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2
                t = np.fliplr(self.pan[:, x, :]).diagonal(i)
                for j in range(len(t) - 4):
                    if np.all(t[j:j + 5] == 1):
                        return 1
                    elif np.all(t[j:j + 5] == 2):
                        return 2

    def launch_at(self, z, x, y):
        if self.get_at(z, x, y) == 0:
            self.pan[z, x, y] = self.turn_now
            self.update()
            return True
        else:
            return False

    def get_at(self, z, x, y):
        return self.pan[z, x, y]

    def update(self):
        t = self.check()
        if t:
            if t == 1:
                print("1 is win")
            elif t == 2:
                print("2 is win")
            self.init()

    def init(self):
        pass

        # self.pan = np.zeros(self.size, dtype=np.uint8)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse = pygame.mouse.get_pos()
            for z, b in enumerate(self.board_rects):
                t = b.collide(mouse)
                if t:
                    x, y = b.collide_cell(mouse)
                    if self.launch_at(z, x, y):
                        self.pass_turn()
                    return True
            else:
                return False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.moving is None:
                mouse = pygame.mouse.get_pos()
                for z, b in enumerate(self.board_rects):
                    t = b.collide(mouse)
                    if t:
                        self.moving = z
                        break
                else:
                    return False

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            if not (self.moving is None):
                self.moving = None


        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[2]:
                if not (self.moving is None):
                    self.board_rects[self.moving].move_absolute(pygame.mouse.get_pos())

    def draw_all(self, surface):
        self.draw_grid(surface)
        self.draw_cell(surface)

    def draw_grid(self, surface):
        [b.draw(surface) for b in self.board_rects]

    def draw_cell(self, surface):
        for z in range(pan.size[0]):
            for x in range(pan.size[1]):
                for y in range(pan.size[2]):
                    t = pan.get_at(z, x, y)
                    if t == 0:
                        pass
                    elif t == 1:
                        pygame.draw.rect(surface, (0, 0, 0), self.board_rects[z].get_rect(x, y), 0)
                    elif t == 2:
                        pygame.draw.rect(surface, (255, 255, 255), self.board_rects[z].get_rect(x, y), 0)
                    else:
                        pass


pygame.init()

screen = pygame.display.set_mode((1000, 560), pygame.DOUBLEBUF)
clock = pygame.time.Clock()

SIZE = (5, 13, 13)

pan = OmokPan(SIZE)

DONE = False

while not DONE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            DONE = True
        if pan.on_event(event):
            pass

    screen.fill((180, 100, 60))

    pan.draw_all(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
