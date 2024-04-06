#Создай собственный Шутер!

from pygame import *
import random



init()



font1 = font.SysFont('Arial', 70)
fontr = font.SysFont('Arial', 30)
win = font1.render(
    'You lose', True, (255, 0, 0)
    )

def health_draw():
    if health == 3:
        window.blit(health_d, (60, 60))
        window.blit(health_d, (120, 60))
        window.blit(health_d, (180, 60))
    if health == 2:
        window.blit(health_d, (60, 60))
        window.blit(health_d, (120, 60))
    if health == 1:      
        window.blit(health_d, (60, 60))

window = display.set_mode((700, 500))
display.set_caption('Шутер')

checker = 0
AI_work = 1
losed = 0
health = 3
score = 0
c_skin = 'rocket.png'
c_speed = 10

class GameProcessor(sprite.Sprite):
    def __init__(self, img, x, y, xs, ys, w, h, speed):
        super().__init__()
        self.w = w
        self.h = h
        self.img = img
        self.image = transform.scale(image.load(self.img), (self.w, self.h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xs = xs
        self.ys = ys
    def rendering(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ufo(GameProcessor):
    def update(self):
        global AI_work
        global checker
        if AI_work == 1:
            self.rect.y += self.speed
            if self.rect.y >= 500:
                checker += 1
                self.rect.y = -50
                self.rect.x = random.randint(10, 630)

class Rocket(GameProcessor):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def restart(self):
        self.rect.x = self.xs
        self.rect.y = self.ys

class Bullet(GameProcessor):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

class Meteor(GameProcessor):
    def update(self):
        global AI_work
        if AI_work == 1:
            self.rect.y += self.speed
            if self.rect.y >= 550:
                self.kill()



meteor1 = Meteor('asteroid.png', random.randint(0, 640), -60, 0, 0, 20, 20, 10)
meteor2 = Meteor('asteroid.png', random.randint(0, 640), -60, 0, 0, 20, 20, 10)
meteors = sprite.Group()
meteors.add(meteor1)
meteors.add(meteor2)


hero = Rocket('rocket.png', 300, 400, 300, 400, 65, 65, 10)
enemy = Ufo('ufo.png', 364, 55, 300, 55, 65, 65, 3)
enemy2 = Ufo('ufo.png', 250, 86, 291, 86, 65, 65, 3)
enemy3 = Ufo('ufo.png', 350, 45, 280, 45, 65, 65, 3)

ufos = sprite.Group()
ufos.add(enemy)
ufos.add(enemy2)
ufos.add(enemy3)

bullets = sprite.Group()

background = transform.scale(
    image.load('galaxy.jpg'),
    (700, 500)
)

health_d = transform.scale(
    image.load('free-icon-heart-2107845.png'),
    (50, 50)
)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


clock = time.Clock()


game = True
while game:
    scorer = fontr.render(
    'Очки: '+ str(score), True, (255, 255, 255)
    )
    window.blit(background, (0, 0))

    if losed == 1:
        window.blit(win, (150, 200))
    #draw
    ufos.draw(window)
    meteors.draw(window)
    hero.rendering()
    bullets.draw(window)
    health_draw()
    window.blit(scorer, (600, 400))
    if len(ufos) <= 3:
        ufos.add(Ufo('ufo.png', random.randint(10, 630), -60, 0, 0, 65, 65, 3))
    if len(meteors) <= 1:
        meteors.add(Meteor('asteroid.png', random.randint(0, 640), -60, 0, 0, 20, 20, 10))
    #move
    ufos.update()
    hero.move()
    bullets.update()
    meteors.update()
    if sprite.spritecollide(hero, ufos, False):
        health = 0
        losed = 1
        AI_work = 0

    if sprite.spritecollide(hero, meteors, True):
        health -= 1
        if health <= 0:
            losed = 1
            AI_work = 0

    if sprite.groupcollide(bullets, ufos, True, True):
        score += 1


    if checker >= 5:
        losed = 1
        AI_work = 0
    key_pressed = key.get_pressed()
    if key_pressed[K_r]:
        checker = 0
        AI_work = 1
        losed = 0
        health = 3
        score = 0
        hero.restart()

    for evnt in event.get():
        if evnt.type == QUIT:
            game = False
        if evnt.type == KEYDOWN:
            if evnt.key == K_SPACE:
                bullets.add(Bullet('bullet.png', hero.rect.centerx-7, hero.rect.top, 0, 0, 30, 15, 30)) 

    clock.tick(60)
    display.update()


