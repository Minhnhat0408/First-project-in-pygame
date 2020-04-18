import pygame, random
pygame.init()
pygame.font.init()

window = pygame.display.set_mode((500, 500))


class Maincharacter:
    walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png')
        , pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
                 pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
    walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png')
        , pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
                pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
    char = pygame.image.load('standing.png')

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left = False
        self.right = False
        self.walkcount = 0
        self.Jumppxl = 10
        self.Jump = False
        self.stand = True
        self.toward = False
        self.hitbox = (self.x + 15, self.y + 10, self.w - 30, self.h - 10)
        self.choice = ()

    def animations(self, screen):
        if self.walkcount + 1 >= 27:
            self.walkcount = 0
        if not self.stand:
            if self.left:
                screen.blit(Maincharacter.walkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.right:
                screen.blit(Maincharacter.walkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            elif self.toward:
                screen.blit(Maincharacter.char, (self.x, self.y))

        else:
            if self.right:
                screen.blit(Maincharacter.walkRight[0], (self.x, self.y))
            elif self.left:
                screen.blit(Maincharacter.walkLeft[0], (self.x, self.y))
            else:
                screen.blit(Maincharacter.char, (self.x, self.y))
        self.hitbox = (self.x + 15, self.y + 10, self.w - 30, self.h - 10)

        # pygame.draw.rect(screen,(255,0,0),self.hitbox,2)

    def hit(self):
        self.Jump = False
        self.Jumppxl = 10
        self.x = 260
        self.y = 320
        self.walkCount = 0


class Bullet:
    blimg = [pygame.image.load("fireballleft.png"), pygame.image.load("fireballr.png"),
             pygame.image.load("fireballup.png")]

    def __init__(self, x, y, w, h, facing):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.facing = facing
        self.vel = 10 * facing

    def draw(self, screen):
        if self.facing == 1:
            screen.blit(Bullet.blimg[1], (self.x, self.y))
        elif self.facing == -1:
            screen.blit(Bullet.blimg[0], (self.x-25, self.y))
        else:
            screen.blit(Bullet.blimg[2], (self.x-10, self.y))
        # pygame.draw.rect(screen,(255,0,0),(self.x,self.y,self.w,self.h),2)


class Enemy:
    EwalkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                  pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                  pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                  pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    EwalkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                 pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                 pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                 pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, w, h, end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.end = end
        self.walkcount = 0
        self.hitbox = (self.x + 20, self.y + 5, self.w - 35, self.h - 10)
        self.path = [self.x, self.end]
        self.vel = 3
        self.health = 10
        self.visible = True

    def draw(self, screen):
        self.automove()
        if self.visible:
            if self.walkcount >= 33:
                self.walkcount = 0

            if self.vel < 0:
                screen.blit(Enemy.EwalkLeft[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            else:
                screen.blit(Enemy.EwalkRight[self.walkcount // 3], (self.x, self.y))
                self.walkcount += 1
            self.hitbox = (self.x + 20, self.y + 5, self.w - 30, self.h - 10)
            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 30, 5))
            pygame.draw.rect(screen, (0, 255, 0),(self.hitbox[0], self.hitbox[1] - 20, 30 - (3 * (10 - self.health)), 5))
            pygame.draw.rect(screen, (0, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 30, 5), 1)
            #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def automove(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount += 1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkcount += 1

    def hit(self, choice):

        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            self.respawn(choice)

    def respawn(self, choice):
        i = 0
        while i < 100:
            i += 1
            pygame.time.delay(10)
        else:
            self.x = random.choice(choice)
            self.walkcount = 0
            self.visible = True
            self.health = 10


class Score:
    def __init__(self, score):
        self.score = score

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", 30, True)
        text = font.render(f"Score :{self.score}", 10, (165, 95, 250))
        screen.blit(text, (200, 10))


def Settings(Fps, caption):
    pygame.display.set_caption(caption)
    FPS = pygame.time.Clock()
    FPS.tick(Fps)


def text(text, size, color, pos):
    font = pygame.font.SysFont("comicsans", size, True)
    display = font.render(text, 10, color)
    window.blit(display, pos)


def main():
    bg = pygame.image.load("anotherbg.jpg")
    GameWork = False
    bulletleftright = []
    bulletupdown = []
    Shootloop = 0
    GameOver = False
    Start = False
    enemy = Enemy(-20, 320, 64, 64, 450)
    score = Score(0)
    main = Maincharacter(260, 320, 64, 64)
    while not Start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GameWork = False
        intro = pygame.image.load("intro.jpg")
        bt = pygame.image.load("start_button.png")
        intro = pygame.transform.scale(intro, (500, 500))
        window.blit(intro, (0, 0))
        window.blit(bt, (170, 10))
        cur = pygame.mouse.get_pos()
        if 170 < cur[0] < 290 and 10 < cur[1] < 70:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                Start = True
                GameWork = True
        pygame.display.update()
    choice = ()
    while GameWork:
        Settings(27, "Adventure!!")
        kw = pygame.key.get_pressed()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                GameWork = False
        if enemy.visible:
            if main.hitbox[1] < enemy.hitbox[1] + enemy.hitbox[3] and main.hitbox[1] + main.hitbox[3] > enemy.hitbox[1]:
                if main.hitbox[0] + main.hitbox[2] > enemy.hitbox[0] and main.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
                    GameOver = True
                    choice = list(range(1, main.x - 40)) + list(range(main.x + 40, 450))
        if Shootloop > 0:
            Shootloop += 1
        if Shootloop > 4:
            Shootloop = 0
        for i in bulletupdown:
            if i.y > 0:
                i.y -= 8
            else:
                bulletupdown.pop(bulletupdown.index(i))

        for i in bulletleftright:
            if enemy.visible:
                if i.y + i.h < enemy.hitbox[1] + enemy.hitbox[3] and i.y > enemy.hitbox[1]:
                    if i.x + i.w + 15 > enemy.hitbox[0] and i.x < enemy.hitbox[0] + enemy.hitbox[2]:
                        if enemy.health == 0:
                            choice = list(range(1, main.x - 40)) + list(range(main.x + 40, 450))
                        score.score += 1
                        enemy.hit(choice)
                        bulletleftright.pop(bulletleftright.index(i))

                if 0 < i.x < 500:
                    i.x = i.x + i.vel
                else:
                    bulletleftright.pop(bulletleftright.index(i))
            else:
                if 0 < i.x < 500:
                    i.x = i.x + i.vel
                else:
                    bulletleftright.pop(bulletleftright.index(i))

        if kw[pygame.K_a] and main.x > 0 - 20:
            main.x -= 5
            main.left = True
            main.right = False
            main.stand = False
            main.toward = False
        elif kw[pygame.K_d] and main.x < 500 - 50:
            main.x += 5
            main.left = False
            main.right = True
            main.stand = False
            main.toward = False
        elif kw[pygame.K_w]:
            main.toward = True
            main.left = False
            main.right = False
            main.stand = False
        else:
            main.stand = True
            main.walkcount = 0
        if kw[pygame.K_j] and Shootloop == 0:
            if main.left:
                face = -1
            elif main.right:
                face = 1
            else:
                face = 0
            if main.left or main.right:
                if len(bulletleftright) < 2:
                    bulletleftright.append(Bullet(round(main.x + main.w // 2), round(main.y + main.h * 1 / 3), 32, 32, face))
            else:
                if len(bulletupdown) < 4:
                    bulletupdown.append(Bullet(round(main.x + main.w // 2), round(main.y + main.h * 1 / 3), 32, 32, face))
            Shootloop = 1
        if not main.Jump:
            if kw[pygame.K_SPACE]:
                main.Jump = True
                main.stand = False
                main.walkcount = 0
        else:
            if main.Jumppxl >= -10:
                main.y -= (main.Jumppxl * abs(main.Jumppxl))*0.3
                main.Jumppxl -= 1
            else:
                main.Jump = False
                main.Jumppxl = 10
        while GameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            text("GAME OVER", 50, (255, 0, 0), (140, 230))
            text("Try again", 30, (255, 0, 0), (60, 400))
            text("Quit", 30, (255, 0, 0), (350, 400))
            pygame.draw.rect(window, (255, 0, 0), (50, 390, 130, 40), 4)
            pygame.draw.rect(window, (255, 0, 0), (310, 390, 130, 40), 4)
            cur = pygame.mouse.get_pos()
            if 50 < cur[0] < 180 and 390 < cur[1] < 430:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    GameOver = False
                    score.score = 0
                    main.hit()
                    choice = list(range(1, main.x - 20)) + list(range(main.x + 20, 450))
                    enemy.respawn(choice)

            if 310 < cur[0] < 440 and 390 < cur[1] < 430:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    GameWork = False
                    pygame.quit()
            pygame.display.update()
        window.blit(bg, (0, 0))
        main.animations(window)
        enemy.draw(window)
        score.draw(window)
        for i in bulletleftright:
            i.draw(window)
        for h in bulletupdown:
            h.draw(window)
        pygame.display.update()


main()
