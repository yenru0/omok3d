import pygame
import numpy as np

from function.pane import BoardRect, HorizontalBoardSliderRect


class OmokPan:
    def __init__(self, size):
        self.size = size
        self.pan = np.zeros(size, dtype=np.uint8)
        self.turn_now = 1
        self.horizontal_slide = HorizontalBoardSliderRect(self.size, (0, 20), 1600, 340, slide_range=(0, RESOLUTION[0]))

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
        self.horizontal_slide.on_event(event)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse = pygame.mouse.get_pos()
            for z, b in enumerate(self.horizontal_slide.board_rects):
                t = b.collide(mouse)
                if t:
                    x, y = b.collide_cell(mouse)
                    if self.launch_at(z, x, y):
                        self.pass_turn()
                    return True
            else:
                return False

    def draw_all(self, surface):
        self.horizontal_slide.draw_boards_grid(surface)
        self.horizontal_slide.draw_axis(surface)
        self.draw_cell(surface)

    def draw_cell(self, surface):
        for z in range(pan.size[0]):
            for x in range(pan.size[1]):
                for y in range(pan.size[2]):
                    t = pan.get_at(z, x, y)
                    if t == 0:
                        pass
                    elif t == 1:
                        pygame.draw.circle(surface, (0, 0, 0), self.horizontal_slide.get_rect(z, x, y).center, 7)
                    elif t == 2:
                        pygame.draw.circle(surface, (255, 255, 255), self.horizontal_slide.get_rect(z, x, y).center, 7)
                    else:
                        pass

    def draw_debug(self, surface):
        pygame.draw.line(surface, (0, 0, 255),
                         self.horizontal_slide.slider_rect.midtop, self.horizontal_slide.slider_rect.midbottom)

        pygame.draw.line(surface, (0, 0, 255),
                         (self.horizontal_slide.slider_rect.topleft[0],
                          self.horizontal_slide.slider_rect.topleft[1] + self.horizontal_slide.padding[1]),
                         (self.horizontal_slide.slider_rect.topright[0],
                          self.horizontal_slide.slider_rect.topright[1] + self.horizontal_slide.padding[1])
                         )
        for i in range(self.size[0]):
            pygame.draw.rect(surface, (0, 255, 0), self.horizontal_slide.font_axis_z_rects[i], 1)


if __name__ == '__main__':
    pygame.init()

    RESOLUTION = (1000, 560)

    screen = pygame.display.set_mode((1000, 560), pygame.DOUBLEBUF)
    clock = pygame.time.Clock()

    SIZE = (5, 13, 13)

    pan = OmokPan(SIZE)

    DONE = False
    DEBUG = not True
    while not DONE:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                DONE = True
            if pan.on_event(event):
                pass

        screen.fill((180, 100, 60))

        pan.draw_all(screen)
        if DEBUG:
            pygame.draw.line(screen, (255, 0, 0), (RESOLUTION[0] // 2, 0), (RESOLUTION[0] // 2, RESOLUTION[1]), 1)
            pan.draw_debug(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
