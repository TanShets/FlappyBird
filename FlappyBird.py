import pygame as pg
if False:
	import pygame._view
import random
class Character:
    image = [
        pg.image.load('assets/yellowbird-midflap.png'), 
        pg.image.load('assets/yellowbird-downflap.png'), 
        pg.image.load('assets/yellowbird-upflap.png')
    ]
    current_image = image[0]
    MAX_ANGLE = 60
    MIN_ANGLE = -90
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.isJump = False
        self.jumpCount = 6
        self.angle = 0
        self.isend = False
    
    def jump(self):
        if self.jumpCount >= 0:
            negFact = 1    
        else:
            negFact = -1
        self.y -= 0.5 * (self.jumpCount ** 2) * negFact
        self.angle += 5 * negFact
        if self.angle > self.MAX_ANGLE:
            self.angle = self.MAX_ANGLE
        elif self.angle < self.MIN_ANGLE:
            self.angle = self.MIN_ANGLE
        self.jumpCount -= 1
        if self.y >= screenHeight - 40:
            self.y = screenHeight - 40
            self.isend = True
            self.angle = -90
        elif self.y < -20:
            self.y = -20
    
    def draw(self, window, isSpace, isOver = False):
        if (pg.mouse.get_pressed()[0] or isSpace) and not isOver:
            self.jumpCount = 6
        self.jump()
        #pg.draw.rect(window, self.colour, (self.x, self.y, self.width, self.height))
        if self.jumpCount == 0:
            self.angle = 0
            self.current_image = pg.transform.rotate(self.image[0], self.angle)
            #window.blit(self.image[0], (self.x, self.y))
            #window.blit(self.current_image, (self.x, self.y))
        else:
            if self.jumpCount > 0:
                self.current_image = pg.transform.rotate(self.image[1], self.angle)
                #window.blit(self.image[1], (self.x, self.y))
            else:
                self.current_image = pg.transform.rotate(self.image[2], self.angle)
                #window.blit(self.image[2], (self.x, self.y))
        window.blit(self.current_image, (self.x, self.y))
        #pg.draw.rect(window, (255, 0, 0), (self.x, self.y, self.current_image.get_rect().size[0], self.current_image.get_rect().size[1]), 1)

class PipePair:
    image = pg.image.load('assets/pipe-green.png')
    pipe1 = pg.transform.rotate(image, 0)
    pipe1 = pg.transform.scale(pipe1, (pipe1.get_rect().size[0] + 20, pipe1.get_rect().size[1] * 2))
    pipe2 = pg.transform.rotate(image, 180)
    pipe2 = pg.transform.scale(pipe2, (pipe2.get_rect().size[0] + 20, pipe2.get_rect().size[1] * 2))
    y_gap = 160
    speed = -4
    passed = False
    def __init__(self, x, y):
        self.x = x
        self.y1 = y #The coordinate of the top left corner of lower pipe
        self.y2 = y - self.y_gap - self.pipe1.get_rect().size[1]
        self.isend = False
        self.width = self.pipe1.get_rect().size[0]
        self.height = self.pipe1.get_rect().size[1]
    
    def draw(self, window, isOver = False):
        if not isOver:
            self.x += self.speed
        
        if self.x < -self.pipe1.get_rect().size[0]:
            self.isend = True
        else:
            window.blit(self.pipe1, (self.x, self.y1))
            #pg.draw.rect(window, (255, 0, 0), (self.x, self.y1, self.pipe1.get_rect().size[0], self.pipe1.get_rect().size[1]), 1)
            window.blit(self.pipe2, (self.x, self.y2))
            #pg.draw.rect(window, (255, 0, 0), (self.x, self.y2, self.pipe1.get_rect().size[0], self.pipe1.get_rect().size[1]), 1)
        #pg.display.update()
    
    def isColliding(self, character):
        global score
        if character.x in range(self.x, self.x + self.width) or character.x + character.current_image.get_rect().size[0] in range(self.x, self.x + self.width):
            if not self.passed:
                score += 1
                self.passed = True

            if character.y + character.current_image.get_rect().size[1] >= self.y1:
                return True
            elif character.y <= self.y2 + self.height:
                return True
        return False

def initialise():
    isOver = False
    pipe = [PipePair(500, screenHeight - 100), PipePair(500 + dist, screenHeight - 120)]
    score = 0
    #PipePair.speed = -50
    char = Character(250, 270)
    return isOver, pipe, char, score
pg.init()
limit = 2
dist = 200
screenWidth = 700
screenHeight = 500
window = pg.display.set_mode((screenWidth, screenHeight))
pg.display.set_caption("FlappyBird - FanMade")
clock = pg.time.Clock()
bg = pg.image.load('assets/background-day.png')
bg = pg.transform.scale(bg, (screenWidth, screenHeight))
floor = pg.image.load('assets/base.png')
floor = pg.transform.scale(floor, (screenWidth, floor.get_rect().size[1]))
font = pg.font.SysFont('comicsans', 30, True)
gameOver = pg.image.load('assets/gameover.png')
#gameOver = pg.transform.scale(gameOver, (round(floor.get_rect().size[0] * 1.001), floor.get_rect().size[1]))
run = True
beginning = True
start_bg = pg.image.load('assets/title.jpg')
start_bg = pg.transform.scale(start_bg, bg.get_rect().size)
isOver, pipe, char, score = initialise()
while run:
    clock.tick(30)
    #pg.time.delay(1)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
    if beginning:
        window.blit(start_bg, (0, 0))
        pg.display.update()
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN] or keys[pg.K_SPACE] or pg.mouse.get_pressed()[0]:
            beginning = False
    elif not isOver:
        keys = pg.key.get_pressed()
        window.blit(bg, (0, 0))
        #window.blit(pipe, (0, 0))
        #pipe.draw(window)
        if len(pipe) <= limit:
            pipe.append(PipePair(pipe[-1].x + dist, screenHeight - max(40, round(random.random() * screenHeight * 0.75))))
        
        for i in range(len(pipe)):
            pipe[i].draw(window)
            isOver = pipe[i].isColliding(char)
            if isOver:
                break
        
        if not isOver:
            if pipe[0].isend:
                pipe.pop(0)

            window.blit(floor, (0, screenHeight - 20))
            text = font.render('Score: ' + str(score), 1, (0, 0, 0))
            window.blit(text, (round(screenWidth * 0.8 - text.get_rect().size[0] / 2), round(0.5 * text.get_rect().size[1])))
            char.draw(window, keys[pg.K_SPACE])
            isOver = char.isend #Since isOVer is already false here, equating it to isend would yield the same result
            pg.display.update()
    else:
        window.blit(bg, (0, 0))
        keys = pg.key.get_pressed()
        for i in pipe:
            i.draw(window, isOver)
        window.blit(floor, (0, screenHeight - 20))
        char.draw(window, False, isOver)
        text = font.render('Score: ' + str(score), 1, (0, 0, 0))
        window.blit(text, (round(screenWidth * 0.8 - text.get_rect().size[0] / 2), round(0.5 * text.get_rect().size[1])))
        window.blit(gameOver, (round((screenWidth - gameOver.get_rect().size[0]) / 2), round((screenHeight - gameOver.get_rect().size[1]) / 2)))
        pg.display.update()
        if keys[pg.K_RETURN] or pg.mouse.get_pressed()[0]:
            isOver, pipe, char, score = initialise()
        
pg.quit()