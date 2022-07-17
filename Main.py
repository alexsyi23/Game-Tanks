import math
import pygame
pygame.init()
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255,255,255))
    surf.blit(text_surface, (x, y))
def length(obj,direction,size_px):
    X, Y = obj[0], obj[1]
    if (direction[0] * direction[1]) == 0:
        X += direction[0] * size_px
        Y += direction[1] * size_px
    else:
        X += direction[0] * size_px / math.sqrt(2)
        Y += direction[1] * size_px / math.sqrt(2)
    return [X, Y]
class Tank:
    speed = 2
    def __init__(self,color,direction,start_xy,KeyControl):
        self.patrons = 15
        self.xy = start_xy
        self.color = color
        self.image = ImgTanks[color][0][(direction[0],direction[1])]
        self.rect = self.image.get_rect(center=(self.xy[0],self.xy[1]))
        self.size = (ImgTanks[color][1],ImgTanks[color][2])
        self.direction = direction
        self.left = KeyControl[0]
        self.right = KeyControl[1]
        self.up = KeyControl[2]
        self.down = KeyControl[3]
        self.fire = KeyControl[4]
    def move(self):
        movem = [0,0]
        old_xy = self.xy
        if keys[self.left]:
            movem[0] -= 1
        if keys[self.right]:
            movem[0] += 1
        if keys[self.up]:
            movem[1] -= 1
        if keys[self.down]:
            movem[1] += 1
        if movem != [0,0]:
            self.xy = length(self.xy,movem,self.speed)
            if self.xy[0] < Wall_size or self.xy[0] > Width - Wall_size or self.xy[1] < Wall_size or self.xy[1] > Height - Wall_size:
                self.xy = old_xy
            for Tank_x in Tanks:
                if Tank_x.color != self.color and self.rect.colliderect(Tank_x.rect):  # (Tank_x.rect.collidepoint(self.rect.topleft) or Tank_x.rect.collidepoint(self.rect.topright) or Tank_x.rect.collidepoint(self.rect.bottomleft) or Tank_x.rect.collidepoint(self.rect.bottomright)):
                    distance_new = math.sqrt( ((self.xy[0]-Tank_x.xy[0])**2)+((self.xy[1]-Tank_x.xy[1])**2) )
                    distance_old = math.sqrt( ((old_xy[0] - Tank_x.xy[0]) ** 2) + ((old_xy[1] - Tank_x.xy[1]) ** 2))
                    if distance_new <= distance_old:
                        self.xy = old_xy
                    break
            for Block_x in Blocks:
                if self.rect.colliderect(Block_x.rect):
                    if (self.xy[0] < Block_x.xy[0] or self.xy[0] > Block_x.xy[0] + Block_x.width * Brick_size):
                        if (self.xy[0] < Block_x.xy[0] and self.xy[0] > old_xy[0]):
                            self.xy = old_xy
                        if (self.xy[0] > Block_x.xy[0] + Block_x.width * Brick_size and self.xy[0] < old_xy[0]):
                            self.xy = old_xy
                    if (self.xy[1] < Block_x.xy[1] or self.xy[1] > Block_x.xy[1] + Block_x.height * Brick_size):
                        if (self.xy[1] < Block_x.xy[1] and self.xy[1] > old_xy[1]):
                            self.xy = old_xy
                        if (self.xy[1] > Block_x.xy[1] + Block_x.height * Brick_size and self.xy[1] < old_xy[1]):
                            self.xy = old_xy
            if movem != self.direction:
                self.direction = movem
                self.image = ImgTanks[self.color][0][(self.direction[0],self.direction[1])]
        self.rect = self.image.get_rect(center=(self.xy[0],self.xy[1]))#(center(self.xy, Size)[0], center(self.xy, Size)[1]))
        scr.blit(self.image, self.rect)
        #pygame.draw.rect(scr, self.color, [self.xy[0], self.xy[1], Size, Size])
        #pygame.draw.line(scr, 'red', (center(self.xy,Size)[0],center(self.xy,Size)[1]), (length(center(self.xy,Size),self.direction,25)[0], length(center(self.xy,Size),self.direction,25)[1]), 4)
    def fight(self):#Bullet(self.color,self.direction,self.xy)
        if (self.patrons>0):
            Bullets.append(Bullet(self.color,(self.direction[0],self.direction[1]),[self.xy[0],self.xy[1]]))
            self.patrons -= 1
class Bullet:
    speed = 5
    def __init__(self,color,direction,start_xy):
        self.xy = start_xy
        self.color = color
        self.direction = direction
    def move(self):
        global GAME_OVER
        self.xy[0] += self.direction[0] * self.speed
        self.xy[1] += self.direction[1] * self.speed
        bullet_del = False
        if self.xy[0] < Wall_size or self.xy[0] > Width-Wall_size or self.xy[1] < Wall_size or self.xy[1] > Height-Wall_size:
            bullet_del = True
        else:
            for Block_x in Blocks:
                if Block_x.rect.collidepoint(self.xy[0], self.xy[1]):
                    bullet_del = True
                    break
        if not bullet_del:
            for Tank_x in Tanks:
                if Tank_x.color != self.color:
                    if Tank_x.rect.collidepoint(self.xy[0], self.xy[1]):
                        bullet_del = True
                        Tanks.remove(Tank_x)
                        GAME_OVER = True
                        break
        if bullet_del:
            Bullets.remove(self)
        else:
            pygame.draw.circle(scr, self.color, (self.xy[0], self.xy[1]), 2)
class Block:
    def __init__(self, xy, width, height):
        self.xy = xy
        self.width = width
        self.height = height
        self.rect = pygame.Rect(xy[0], xy[1], width * Brick_size, height * Brick_size)
    def draw(self):
        for i in range(0,self.width):
            for j in range(0,self.height):
                figure = pygame.Rect(self.xy[0] + i * Brick_size, self.xy[1] + j * Brick_size, Brick_size, Brick_size)
                scr.blit(imgBlock, figure)
# Главные переменные
Width, Height, Fps = 800, 700, 60
Wall_size = 20
Brick_size = 32
imgBlock = pygame.image.load('brick.png')
Blocks = [Block(((Width-Brick_size)/2,150),1,(Height-300)//Brick_size),
          Block((150,(Height-Brick_size)/2),(Width-300)//Brick_size,1)]
ImgTanks = {}
ImgTanks['white'] = ({(0,0):pygame.image.load('white.png')}, 25, 30)
ImgTanks['green'] = ({(0,0):pygame.image.load('green.png')}, 23, 42)
for key2 in ImgTanks.keys():
    for i in range(-1,2):
        for j in range(-1,2):
            ImgTanks[key2][0][(i,j)] = pygame.transform.rotate(ImgTanks[key2][0][(0,0)], - math.atan2(j, i)*180 / math.pi )
pygame.display.set_caption("Tanks")
scr = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()

Tank1 = Tank('green', [-1,-1], [750,650], (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER))
Tank2 = Tank('white', [1,1], [50,50], (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
Tanks=[Tank1,Tank2]
Bullets=[]
GAME_OVER = False
game_over = False
counter = 0
bg = pygame.image.load("fon2.png")
while not game_over:
    counter += 1
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            for Tank_x in Tanks:
                Tank_x.move()
                if event.key == Tank_x.fire:
                    Tank_x.fight()
    scr.fill('black')
    scr.blit(bg, (0, 0))
    wall = pygame.Rect(0, 0, Width, Wall_size)
    pygame.draw.rect(scr, 'brown', [0, 0, Width, Wall_size])
    pygame.draw.rect(scr, 'brown', [0, 0, Wall_size, Height])
    pygame.draw.rect(scr, 'brown', [Width-Wall_size, 0, Wall_size, Height])
    pygame.draw.rect(scr, 'brown', [0, Height-Wall_size, Width, Wall_size])
    txt = 'Пули: '
    for Block_x in Blocks:
        Block_x.draw()
    for Tank_x in Tanks:
        Tank_x.move()
        if (counter / Fps >= 5):
            Tank_x.patrons += 1
        txt += Tank_x.color + ':'+ str(Tank_x.patrons) + ' '
    if (counter / Fps >= 5):
        counter = 0
    draw_text(scr, txt, 20, Width - 190, 4)
    for Bullet_x in Bullets:
        Bullet_x.move()
    if GAME_OVER:
        draw_text(scr, 'GAME OVER', 30, Width/2 - 70, 30)
    pygame.display.update()
    clock.tick(Fps)
pygame.quit()
