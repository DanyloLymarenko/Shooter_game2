#Створи власний Шутер!

from pygame import *
from random import *
from time import time as timer
win_width = 700
win_height = 500




window = display.set_mode((win_width,win_height))
display.set_caption("Schooter")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))


mixer.init()
mixer.music.load("muzyka.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")
mixer.music.set_volume(0.1)
font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!))', True, (0, 255, 0))
lose = font1.render('YOU LOSE!))', True, (180, 0, 0))






class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed


 

        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x-=self.speed
        if keys[K_RIGHT] and self.rect.x < win_width-80:
            self.rect.x+=self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)

        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = -50
            self.speed = randint(1,6)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed


        if self.rect.y<-10:
            self.kill()

bullets = sprite.Group()


class Anim(sprite.Sprite):
    def __init__(self,nameDirAnim,pos_x,pos_y,countSprite):
        sprite.Sprite.__init__(self)
        self.animation_set = [transform.scale(image.load(f"{i}.png"),(50,50)) for i in range(1, countSprite)]
        self.i = 0
        self.x = pos_x
        self.y = pos_y
    
    def update(self):
        window.blit(self.animation_set[self.i], (self.x, self.y))
        self.i += 1
        if self.i > len(self.animation_set) -1:
            self.kill()

animsHit = sprite.Group()




run = True

finish = False
score = 0
lost = 0
life = 5
rel_time = False
num_fire = 0

ship = Player("rocket.png",5,win_height-100, 80,100,10)

listUfoSprite = ["ufo.png","sprite2.png","sprite3.png"]

monsters = sprite.Group()
for i in range(6):
    monster = Enemy(listUfoSprite[randint(0,len(listUfoSprite)-1)],randint(80,win_width-80),-50,80,50,randint(1,10))
    monsters.add(monster)



while run:


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    if finish != True:

        window.blit(background,(0,0))
        
        text = font2.render("Рахунок:"+str(score),True,(255,255,255))
        window.blit(text,(10,20))


        text_lose = font2.render("Пропущено:"+str(lost),True,(255,255,255))
        window.blit(text_lose,(10,50))

    
        monsters.draw(window)
        monsters.update()

        ship.reset()
        ship.update()
        
        bullets.draw(window)
        bullets.update()
        animsHit.update()



        if rel_time == True:
                now_time = timer()
                if now_time - last_time < 3:
                    reload= font2.render("Wait, reload...",1,(150,0,0))
                    window.blit(reload,(260,460))
                else:
                    num_fire = 0
                    rel_time = False

        collides = sprite.groupcollide(monsters,bullets,True,True)

        for c in collides:
            x, y = c.rect.x , c.rect.y 
            hit = Anim("anim2",x,y,4)
            animsHit.add(hit)
            score +=1
            monster = Enemy("ufo.png",randint(80,win_width-80),-50,80,50,randint(1,5))
            monsters.add(monster)


        if sprite.spritecollide(ship,monsters,False):
            sprite.spritecollide(ship,monsters,True)
            life -= 1
            monster = Enemy("ufo.png",randint(80,win_width-80),-50,80,50,randint(1,5))
            monsters.add(monster)

        if score >= 5:
            finish = True
            window.blit(win,(win_width/2-50,win_height/2))


        if life < 1 or lost >=5:
            finish = True
            window.blit(lose,(win_width/2-50,win_height/2))
        
        if life > 3:
            fill_color = (0,150,0)
        elif life > 1:
            fill_color = (150,150,0)
        else:
            fill_color = (150,0,0)

        text_life = font2.render(str(life),1,fill_color)
        window.blit(text_life,(640,20))




    
    display.update()
    time.delay(60)

    
