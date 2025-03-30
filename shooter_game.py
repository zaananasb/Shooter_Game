from pygame import *
from random import randint
from time import time as timer
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            lost = lost + 1

display.set_caption("Shooter")
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(0,620), randint(0,15), 80, 50, randint(1,2))
    monsters.add(monster)

lost = 0
score = 0
ship = Player("rocket.png", 5, 400, 80, 100, 10)
finish = False
run = True
shop_text = font1.render("Магазин:", 1, (255,255,255))
upgrade_shoot_text = font1.render("Пробивающий выстрел - 5", 1, (255,255,255))
win_text = font2.render("Вы выйграли!", 1, (20, 255, 20)) 
lose_text = font2.render("Вы проиграли!", 1, (255, 30, 30))
ne_probivat = True
num_shoot = 0 #количество выстрелов. если больше 5, то перезарядка
shoot_reload = False #перезарядка

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: #if e.type == MOUSEBUTTONDOWN:
            if e.key == K_SPACE and not shoot_reload:  #e.button == LEFT:
                ship.fire()                  
                fire_sound.play()
                num_shoot += 1
                last_time = timer()
            if e.key == K_b and score >=5:
                score -= 5
                ne_probivat = False
                upgrade_shoot_text = font1.render("Улучшение куплено", 1, (255,255,255))
    if not finish:
        window.blit(background,(0,0))
        if num_shoot >= 5 and shoot_reload==False:
            shoot_reload = True
        if shoot_reload == True:
            now_time = timer() #считываем время
            if now_time - last_time < 3: #пока не прошло 3 секунды выводим информацию о перезарядке
                reload = font1.render('Перезарядка!', 1, (150, 0, 0))
                window.blit(reload, (260, 250))
            else:
                num_shoot = 0
                shoot_reload = False 
                
        num_shoot_text = font1.render("Выстрелов:" + str(num_shoot), 1, (255,255,255))
        text = font1.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        window.blit(upgrade_shoot_text, (350, 40))
        window.blit(shop_text, (570, 20))
        text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        window.blit(num_shoot_text, (10, 80))
        if sprite.groupcollide(bullets, monsters, ne_probivat, True):
            score += 1
            monster = Enemy("ufo.png", randint(0,620), randint(0,15), 80, 50, randint(1,2))
            monsters.add(monster)
        if score >= 10:
            window.blit(win_text, (250,240))
            finish = True
        if lost >= 10 or sprite.spritecollide(ship, monsters, False):
            window.blit(lose_text, (250, 240))
            finish = True
        ship.update()
        ship.reset()
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        display.update()
    time.delay(30)
