import pygame


class BoardRect:
    def __init__(self, x, y, gridSize, cellSize):
        self.x = gridSize[0]
        self.y = gridSize[1]

        self.boardrect: pygame.Rect = pygame.Rect((x, y), (gridSize[0] * cellSize[0], gridSize[1] * cellSize[1]))
        self.cellrects: list = [
            [pygame.Rect((x + i * cellSize[0], y + j * cellSize[1]), cellSize) for j in range(gridSize[1])] for i in
            range(gridSize[0])]
        self.font_axis_xy = pygame.font.Font(None, 24)

        self.font_axis_x_surfaces = [self.font_axis_xy.render(str(x + 1), True, (0, 0, 0)) for x in range(self.x)]
        self.font_axis_y_surfaces = [self.font_axis_xy.render(str(y + 1), True, (0, 0, 0)) for y in range(self.y)]
        self.font_axis_x_rects = [x.get_rect() for x in self.font_axis_x_surfaces]
        self.font_axis_y_rects = [y.get_rect() for y in self.font_axis_y_surfaces]

        for x in range(self.x):
            self.font_axis_x_rects[x].midbottom = self.cellrects[x][0].midtop

        for y in range(self.y):
            self.font_axis_y_rects[y].midright = self.cellrects[0][y].midleft

    def collide(self, point):
        return self.boardrect.collidepoint(*point)

    def collide_cell(self, point):
        for i, row in enumerate(self.cellrects):
            for j, cell in enumerate(row):
                if cell.collidepoint(*point):
                    return i, j

    def get_rect(self, x, y):
        return self.cellrects[x][y]

    def draw(self, surface):
        for row in self.cellrects:
            for cell in row:
                pygame.draw.rect(surface, (0, 0, 0), cell, 1)
        for x in range(self.x):
            surface.blit(self.font_axis_x_surfaces[x], self.font_axis_x_rects[x])
        for y in range(self.y):
            surface.blit(self.font_axis_y_surfaces[y], self.font_axis_y_rects[y])

    def move_absolute_center(self, pos):
        _x, _y = pos[0], pos[1]
        _now_x, _now_y = self.boardrect.center

        _dx, _dy = _x - _now_x, -_now_y + _y
        self.boardrect.center = _dx + _now_x, _dy + _now_y
        for row in self.cellrects:
            for cell in row:
                cc = cell.center
                cell.center = cc[0] + _dx, cc[1] + _dy

        for r in self.font_axis_x_rects:
            rc = r.center
            r.center = rc[0] + _dx, rc[1] + _dy
        for r in self.font_axis_y_rects:
            rc = r.center
            r.center = rc[0] + _dx, rc[1] + _dy

    def slide(self, x):
        self.boardrect.move_ip(x, 0)
        for row in self.cellrects:
            for cell in row:
                cell.move_ip(x, 0)

        for r in self.font_axis_x_rects:
            r.move_ip(x, 0)
        for r in self.font_axis_y_rects:
            r.move_ip(x, 0)


class HorizontalBoardSliderRect:
    def __init__(self, size, pos, width, height, padding=(50, 50), slide_range=(0, 1000)):

        self.z = size[0]
        self.slider_rect = pygame.Rect(pos, (width, height))
        self.slide_range = slide_range

        self.board_rects = [BoardRect(0, 0, size[1:], (20, 20)) for _ in range(self.z)]
        self.font_axis_z = pygame.font.Font(None, 48)
        self.font_axis_z_surfaces = [self.font_axis_z.render(str(z), True, (0, 0, 0)) for z in range(self.z)]
        self.font_axis_z_rects = [z.get_rect() for z in self.font_axis_z_surfaces]

        self.padding = padding

        for i, b in enumerate(self.board_rects):
            b.move_absolute_center(
                (int(padding[0] + ((width - 2 * padding[0]) / (2 * self.z)) * (2 * i + 1)),
                 int(pos[1] + (height + padding[1]) / 2))
            )
            self.font_axis_z_rects[i].center = (
                int(padding[0] + ((width - 2 * padding[0]) / (2 * self.z)) * (2 * i + 1)), int(padding[1] / 2 + pos[1])
            )

        self.slide(x=int(-width / 2 + sum(slide_range) / 2))

        self.slide_before_pos = (0, 0)

    def on_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.slide_before_pos = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[2]:
                mouse = pygame.mouse.get_pos()
                if self.slider_rect.collidepoint(mouse):
                    self.slide(mouse[0] - self.slide_before_pos[0])
                    self.slide_before_pos = mouse

    def slide(self, x: int):
        if self.slider_rect.topright[0] + x < self.slide_range[1] or \
                self.slider_rect.topleft[0] + x > self.slide_range[0]:
            return
        self.slider_rect.move_ip(x, 0)
        for r in self.font_axis_z_rects:
            r.move_ip(x, 0)
        for b in self.board_rects:
            b.slide(x)

    def draw_boards_grid(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.slider_rect, 1)
        [b.draw(surface) for b in self.board_rects]

    def draw_axis(self, surface):
        for i in range(self.z):
            surface.blit(self.font_axis_z_surfaces[i], self.font_axis_z_rects[i])

    def get_board(self, z):
        return self.board_rects[z]

    def get_rect(self, z, x, y):
        return self.get_board(z).get_rect(x, y)


"https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection"
