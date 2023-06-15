import pygame
import random
import sys

pygame.init()

sw, sh = 600, 600
screen = pygame.display.set_icon(pygame.image.load('icon.png'))
screen = pygame.display.set_caption('2048')
screen = pygame.display.set_mode((sw, sh))

bg_1 = pygame.image.load("bg_1.png")
bg_2 = pygame.image.load("bg_2.png")
bg_3 = pygame.image.load("bg_3.png")
gameover_alpha = 0
bg_3.set_alpha(0)

register = True
appear = False
gameover = False

colors = {'2':(238, 228, 218), '4':(237, 224, 195), '8':(242, 177, 121), '16':(245, 149, 99), '32':(246, 124, 95), '64':(246, 94, 59),
          '128':(237, 207, 114), '256':(237, 204, 97), '512':(237, 200, 80), '1024':(237, 197, 63), '2048':(237, 194, 46), '4096':(243, 103, 116),
          '8192':(241, 75, 97), '16384':(236, 67, 62), '32768':(113, 182, 224), '65536':(94, 161, 229), '131072':(0, 127, 194)}

font_small = pygame.font.Font('LECO.ttf', 39)
font_big = pygame.font.Font('LECO.ttf', 55)

to_move = []
not_to_move = []
new_box, new_box_alpha = [], 255


def calc(x):
    return 14 * (x + 1) + 132 * x


grid = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]]
for i in range(2):
    x, y = random.randint(0, 3), random.randint(0, 3)
    while i == 1 and grid[y][x] != 1:
        x, y = random.randint(0, 3), random.randint(0, 3)
    if random.randint(0, 10) == 1:
        grid[y][x] = 4
    else:
        grid[y][x] = 2
    not_to_move.append([calc(x), calc(y), grid[y][x]])


def check_full():
    for y in range(4):
        for x in range(4):
            if grid[y][x] == 1:
                return False
    return True


def draw_endscreen():
    global gameover_alpha

    if gameover_alpha < 255:
        gameover_alpha += 15
    bg_3.set_alpha(gameover_alpha)
    screen.blit(bg_3, (0, 0))


def draw_squares():
    global appear, new_box_alpha

    for box in not_to_move:
        color = (119, 110, 101) if (box[2] in (2, 4)) else (255, 255, 255)
        font = font_big if (box[2] in (2, 4, 8, 16, 32, 64, 128, 256, 512)) else font_small
        num = font.render(str(box[2]), True, color)
        num_rect = num.get_rect(center=(box[0] + 66, box[1] + 67))
                
        pygame.draw.rect(screen, colors[str(box[2])], pygame.Rect(box[0], box[1], 135, 135))
        screen.blit(num, num_rect)

    for box, i in zip(to_move, range(len(to_move))):
        if box != 'place holder':
            if box[0] < box[1]:
                if box[1] - box[0] <= box[5]:
                    box[0] = box[1]
                    not_to_move.append([box[2], box[0], box[4] if box[6] == 'constant' else box[4] * 2])
                    for a in not_to_move:
                        for b in not_to_move:
                            if (a[0], a[1]) == (b[0], b[1]) and a != b:
                                if a[2] == box[4]:
                                    not_to_move.remove(a)
                                else:
                                    not_to_move.remove(b)
                    to_move[i] = 'place holder'
                else:
                    box[0] += box[5]
            if box[0] > box[1]:
                if box[0] - box[1] <= box[5]:
                    box[0] = box[1]
                    not_to_move.append([box[2], box[0], box[4] if box[6] == 'constant' else box[4] * 2])
                    for a in not_to_move:
                        for b in not_to_move:
                            if (a[0], a[1]) == (b[0], b[1]) and a != b:
                                if a[2] == box[4]:
                                    not_to_move.remove(a)
                                else:
                                    not_to_move.remove(b)
                    to_move[i] = 'place holder'
                else:
                    box[0] -= box[5]
            if box[2] < box[3]:
                if box[3] - box[2] <= box[5]:
                    box[2] = box[3]
                    not_to_move.append([box[2], box[0], box[4] if box[6] == 'constant' else box[4] * 2])
                    for a in not_to_move:
                        for b in not_to_move:
                            if (a[0], a[1]) == (b[0], b[1]) and a != b:
                                if a[2] == box[4]:
                                    not_to_move.remove(a)
                                else:
                                    not_to_move.remove(b)
                    to_move[i] = 'place holder'
                else:
                    box[2] += box[5]
            if box[2] > box[3]:
                if box[2] - box[3] <= box[5]:
                    box[2] = box[3]
                    not_to_move.append([box[2], box[0], box[4] if box[6] == 'constant' else box[4] * 2])
                    for a in not_to_move:
                        for b in not_to_move:
                            if (a[0], a[1]) == (b[0], b[1]) and a != b:
                                if a[2] == box[4]:
                                    not_to_move.remove(a)
                                else:
                                    not_to_move.remove(b)
                    to_move[i] = 'place holder'
                else:
                    box[2] -= box[5]

            color = (119, 110, 101) if (box[4] in (2, 4)) else (255, 255, 255)
            font = font_big if (box[4] in (2, 4, 8, 16, 32, 64, 128, 256, 512)) else font_small
            num = font.render(str(box[4]), True, color)
            num_rect = num.get_rect(center=(box[2] + 66, box[0] + 67))
                    
            pygame.draw.rect(screen, colors[str(box[4])], pygame.Rect(box[2], box[0], 135, 135))
            screen.blit(num, num_rect)
    
    for i in to_move:
        if i == 'place holder':
            to_move.remove(i)

    if to_move == [] and new_box not in not_to_move + [[]]:
        not_to_move.append(new_box)
        appear = True

    if appear:
        cover = pygame.Surface((135, 135))
        cover.set_alpha(new_box_alpha)
        cover.fill((204, 192, 179))
        screen.blit(cover, (new_box[0], new_box[1]))

        if new_box_alpha > 0:
            if new_box_alpha - 10 < 0:
                new_box_alpha = 0
            else:
                new_box_alpha -= 10
        else:
            appear = False
            new_box_alpha = 255

def update_grid(range_1, range_2, range_3, direction):
    global new_box, grid

    grid_changed = False
    merged = []
    for y in range_1:
        for x in range_2:
            if grid[y][x] != 1:
                for i in range_3:
                    if direction == 'vertical':
                        if i == y:
                            break
                        elif grid[i][x] == 1:
                            grid[i][x] = grid[y][x]
                            grid[y][x] = 1
                            to_move.append([calc(y), calc(i), calc(x), calc(x), grid[i][x], abs(y - i) // 0.08, 'constant'])
                            not_to_move.remove([calc(x), calc(y), grid[i][x]])
                            grid_changed = True
                            break
                        elif grid[i][x] == grid[y][x]:
                            allow_multiply = False if (i, x) in merged else True
                            for j in (range(i + 1, y) if y > (i + 1) else range(y + 1, i)):
                                if grid[j][x] != 1:
                                    allow_multiply = False
                            if allow_multiply:
                                to_move.append([calc(y), calc(i), calc(x), calc(x), grid[i][x], abs(y - i) // 0.08, 'double'])
                                not_to_move.remove([calc(x), calc(y), grid[i][x]])
                                grid[i][x] *= 2
                                grid[y][x] = 1
                                merged.append((i, x))
                                grid_changed = True
                                break
                    if direction == 'horizontal':
                        if i == x:
                            break
                        elif grid[y][i] == 1:
                            grid[y][i] = grid[y][x]
                            grid[y][x] = 1
                            to_move.append([calc(y), calc(y), calc(x), calc(i), grid[y][i], abs(x - i) // 0.08, 'constant'])
                            not_to_move.remove([calc(x), calc(y), grid[y][i]])
                            grid_changed = True
                            break
                        elif grid[y][i] == grid[y][x]:
                            allow_multiply = False if (y, i) in merged else True
                            for j in (range(i + 1, x) if x > (i + 1) else range(x + 1, i)):
                                if grid[y][j] != 1:
                                    allow_multiply = False
                            if allow_multiply:
                                to_move.append([calc(y), calc(y), calc(x), calc(i), grid[y][i], abs(x - i) // 0.08, 'double'])
                                not_to_move.remove([calc(x), calc(y), grid[y][i]])
                                grid[y][i] *= 2
                                grid[y][x] = 1
                                merged.append((y, i))
                                grid_changed = True
                                break
               
    if not check_full() and grid_changed:
        add = (random.randint(0, 3), random.randint(0, 3))
        while grid[add[1]][add[0]] != 1:
            add = (random.randint(0, 3), random.randint(0, 3))
        if random.randint(0, 10) == 1:
            grid[add[1]][add[0]] = 4
        else:
            grid[add[1]][add[0]] = 2
        
        new_box = [calc(add[0]), calc(add[1]), grid[add[1]][add[0]]]


def game_over():
    if check_full():
        for y in range(1, 3):
            for x in range(1, 3):
                if grid[y][x] in (grid[y - 1][x], grid[y][x - 1], grid[y + 1][x], grid[y][x + 1]):
                    return False
        if (grid[0][0] in (grid[0][1], grid[1][0]) or grid[0][3] in (grid[0][2], grid[1][3]) 
        or grid[3][0] in (grid[3][1], grid[2][0]) or grid[3][3] in (grid[3][2], grid[2][3]) 
        or grid[0][1] == grid[0][2] or grid[3][1] == grid[3][2] or grid[1][0] == grid[2][0] 
        or grid[1][3] == grid[2][3]):
            return False
    else:
        return False

    return True
        

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and register and not appear and to_move == []:
            if event.key == pygame.K_UP:
                update_grid(range(4), range(4), range(4), 'vertical')
            if event.key == pygame.K_DOWN:
                update_grid(range(3, -1, -1), range(4), range(3, -1, -1), 'vertical')
            if event.key == pygame.K_RIGHT:
                update_grid(range(4), range(3, -1, -1), range(3, -1, -1), 'horizontal')
            if event.key == pygame.K_LEFT:
                update_grid(range(4), range(4), range(4), 'horizontal')
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                register = True
                gameover = game_over()

    screen.blit(bg_2, (0, 0))
    draw_squares()
    screen.blit(bg_1, (0, 0))

    if gameover:
        draw_endscreen()

    pygame.time.Clock().tick(300)
    pygame.display.update()
