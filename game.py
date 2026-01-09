import pygame as pg
from random import randint


class Car(pg.sprite.Sprite):
    def __init__(self, x, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(filename), (100, 100))
        self.rect = self.image.get_rect(center=(x, 0))

    def update(self):
        if self.rect.y < height:
            self.rect.y += 5
        else:
            self.kill()

    def move(self):
        key = pg.key.get_pressed()
        if key[pg.K_w]:
            self.rect.y -= 15
        if key[pg.K_s]:
            self.rect.y += 15
        if key[pg.K_a]:
            self.rect.x -= 15
        if key[pg.K_d]:
            self.rect.x += 15


pg.init()
pg.mixer.init()
# pg.mouse.set_visible(False)
width, height = 800, 600
window = pg.display.set_mode((width, height))
icon = pg.image.load('img/img.png')
bg = pg.image.load('img/bg2.png')
clock = pg.time.Clock()
FPS = 60
lives = 3

car_1 = Car(randint(1, width), 'img/rody.png')
car_1.image = pg.transform.scale(car_1.image, (150, 100))

rect = pg.Rect(0, 0, width, height)

cars = pg.sprite.Group()
cars.add(Car(randint(1, width), 'img/vin.png'))

pg.display.set_caption('Игра')
pg.display.set_icon(icon)

pg.time.set_timer(1, 1000)
pg.time.set_timer(2, 2000)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

click_sound = pg.mixer.Sound('sounds/click.wav')
coin_sound = pg.mixer.Sound('sounds/coin.wav')
pg.mixer.music.load('sounds/music.mp3')
pg.mixer.music.set_volume(0.3)
pg.mixer.music.play(-1)
sound_ok = True


font = pg.font.SysFont('Arial', 30)

button_play_music = pg.Rect(50, 400, 160, 40)
button_stop_music = pg.Rect(230, 400, 160, 40)
button_play_effect = pg.Rect(50, 460, 160, 40)

clicks = 0

state = True
while state:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state = False
        elif event.type == 1:
            cars.add(Car(randint(1, width), 'img/vin.png'))
        elif event.type == 2:
            cars.add(Car(randint(0, width), 'img/vin.png'))
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()

            if not (button_play_music.collidepoint(mouse_pos) or
                    button_stop_music.collidepoint(mouse_pos) or
                    button_play_effect.collidepoint(mouse_pos)):
                clicks += 1
                if sound_ok:
                    click_sound.play()

            if button_play_music.collidepoint(mouse_pos):
                pg.mixer.music.unpause()
            if button_stop_music.collidepoint(mouse_pos):
                pg.mixer.music.pause()
            if button_play_effect.collidepoint(mouse_pos):
                if sound_ok:
                    coin_sound.play()


    car_1.move()


    if pg.sprite.spritecollide(car_1, cars, True):
        lives -= 1


    window.fill(BLACK)
    window.blit(bg, (0, 0))

    cars.draw(window)
    cars.update()
    window.blit(car_1.image, car_1.rect)

    text = font.render(f'Количество жизней: {lives}', True, WHITE)
    window.blit(text, (10, 10))

    text_2 = font.render(f'Клики: {clicks}', True, WHITE)
    window.blit(text_2, (10, 40))

    pg.draw.rect(window, WHITE, button_play_music)
    pg.draw.rect(window, (255, 0, 0), button_stop_music)
    pg.draw.rect(window, BLACK, button_play_effect)

    play_text = font.render('Музыка Вкл', True, BLACK)
    stop_text = font.render('Музыка Выкл', True, BLACK)
    effect_text = font.render('Звук!', True, WHITE)

    window.blit(play_text, (button_play_music.x + 5, button_play_music.y + 5))
    window.blit(stop_text, (button_stop_music.x + 5, button_stop_music.y + 5))
    window.blit(effect_text, (button_play_effect.x + 5, button_play_effect.y + 5))

    if lives <= 0:
        pg.draw.rect(window, BLACK, rect)
        text = font.render('Игра окончена', True, WHITE)
        window.blit(text, (300, 270))


    clock.tick(FPS)
    pg.display.update()