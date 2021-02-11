import pygame


class BoardRect:
    def __init__(self, x, y, gridSize, cellSize):
        self.boardrect: pygame.Rect = pygame.Rect((x, y), (gridSize[0] * cellSize[0], gridSize[1] * cellSize[1]))
        self.cellrects: list = [
            [pygame.Rect((x + i * cellSize[0], y + j * cellSize[1]), cellSize) for j in range(gridSize[1])] for i in
            range(gridSize[0])]

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

    def move_absolute(self, pos):
        _x, _y = pos[0], pos[1]
        _now_x, _now_y = self.boardrect.x, self.boardrect.y

        _dx, _dy = _x - _now_x, -_now_y + _y
        self.boardrect.move_ip(_dx, _dy)
        for row in self.cellrects:
            for cell in row:
                cell.move_ip(_dx, _dy)

    def offset(self, pos):
        return pos[0] - self.boardrect.x, pos[1] - self.boardrect.y


"""
import pygame

class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__() 
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.original_image, color, (25, 25), 25)
        self.click_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(self.click_image, color, (25, 25), 25)
        pygame.draw.circle(self.click_image, (255, 255, 255), (25, 25), 25, 4)
        self.image = self.original_image 
        self.rect = self.image.get_rect(center = (x, y))
        self.clicked = False

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.clicked = not self.clicked

        self.image = self.click_image if self.clicked else self.original_image

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

sprite_object = SpriteObject(*window.get_rect().center, (128, 128, 0))
group = pygame.sprite.Group([
    SpriteObject(window.get_width() // 3, window.get_height() // 3, (128, 0, 0)),
    SpriteObject(window.get_width() * 2 // 3, window.get_height() // 3, (0, 128, 0)),
    SpriteObject(window.get_width() // 3, window.get_height() * 2 // 3, (0, 0, 128)),
    SpriteObject(window.get_width() * 2// 3, window.get_height() * 2 // 3, (128, 128, 0)),
])

run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False 

    group.update(event_list)

    window.fill(0)
    group.draw(window)
    pygame.display.flip()

pygame.quit()
exit()"""
"https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection"
