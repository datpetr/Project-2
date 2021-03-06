import pygame
import random
from os import path


def load_image(name, colorkey=None):
    fullname = path.join('data', name)
    if colorkey is not None:
        image = pygame.image.load(fullname).convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = pygame.image.load(fullname).convert_alpha()
    return image


img_dir = path.join(path.dirname(__file__), 'sounds')

size = WIDTH, HEIGHT = [1536, 864]
screen = pygame.display.set_mode(size)
FPS = 60
x_pos = 1450
y_pos = 50

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
colors = [(255, 255, 255), (0, 0, 255), (30, 144, 255), (255, 69, 0), (255, 255, 0)]
count_of_life = 100
count_of_bullet = 0
k_hit = []
# Создаем игру и окно
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("STAR BATTLE")
clock = pygame.time.Clock()
snd_dir = path.join(path.dirname(__file__), 'sounds')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.shield = 100
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        meteor_list = ['meteor.png', 'meteor2.png', 'meteor4.png']
        self.image_orig = load_image(meteor_list[random.randint(0, 2)])
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                screen.blit(font.render('+ {}'.format(count_of_bullet),
                                        1, (0, 0, 0)), self.rect)


def paused():
    pausing = True
    while pausing:
        for event in pygame.event.get():
            # проверка для закрытия окна
            if event.type == pygame.QUIT:
                pausing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pausing = False


# Загрузка всей игровой графики
player_img = load_image("falcon.png")
meteor_img = load_image("meteor.png")
bullet_img = load_image("laser.png")
pygame.mixer.pre_init(44100, -16, 2, 2048)
# Загрузка всех звуков
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
break_sound = pygame.mixer.Sound(path.join(snd_dir, 'break.wav'))
fly_sound = pygame.mixer.Sound(path.join(snd_dir, 'fly.wav'))
Order66 = pygame.mixer.Sound(path.join(snd_dir, 'Order-66.wav'))
Break_falcon = pygame.mixer.Sound(path.join(snd_dir, 'break_falcon.wav'))
explosion_anim = {'lg': [], 'sm': []}

for j in range(4):
    for i in range(8):
        img = load_image('explosions.png')
        rect = pygame.Rect(0, 0, img.get_width() // 8,
                           img.get_height() // 4)
        explosion_anim['lg'].append(img.subsurface(pygame.Rect(
            (rect.w * i, rect.h * j), rect.size)))
        explosion_anim['sm'].append(img.subsurface(pygame.Rect(
            (rect.w * i, rect.h * j), rect.size)))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
star_list = []

for i in range(15):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Добавляем 1000 звезд со случайными координатами
for i in range(1000):
    x = random.randrange(0, WIDTH)
    y = random.randrange(0, WIDTH)
    star_list.append([x, y, 2])
clock = pygame.time.Clock()

# Цикл игры
running = True
while running:
    # Ввод процесса (события)
    screen.fill(BLACK)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                hit_sound.play()
                player.shoot()
            if event.key == pygame.K_ESCAPE:
                paused()

    font = pygame.font.Font(None, 36)
    screen.blit(pygame.font.Font(None, 36)
                .render("Health: {}%".format(count_of_life),
                        1, (0, 180, 0)), (WIDTH - 200, 50))
    screen.blit(pygame.font.Font(None, 36)
                .render("Score: {}".format(count_of_bullet),
                        1, (0, 180, 0)), (WIDTH - 200, 100))
    # Обновление
    all_sprites.update()
    for star in star_list:
        # Рисуем звезду
        pygame.draw.circle(screen,
                           colors[random.randint(0, 4)],
                           star[0:2], 2)

        # Смещаем звезду вниз
        star[1] += star[2]

        # Если звезда упала за низ окна
        if star[1] > WIDTH:
            # Устанавливаем для нее новые случайные координаты (конечноже выше экрана)
            star[0] = random.randrange(0, WIDTH)
            star[1] = random.randrange(-50, -10)

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)

    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        break_sound.play()
        count_of_bullet += hit.radius // 2
        all_sprites.add(Explosion(hit.rect.center, 'lg'))
        screen.blit(font.render("Hits: {}".format(count_of_bullet), 1, (0, 180, 0)), (WIDTH - 200, 100))

    # Проверка, не ударил ли метеор игрока
    hits = pygame.sprite.spritecollide(player, mobs, False)
    for hit in hits:
        count_of_life -= 1
        screen.blit(font.render("Health: {}%".format(count_of_life), 1, (0, 180, 0)), (WIDTH - 200, 50))
        player.shield -= hit.radius * 2
        all_sprites.add(Explosion(hit.rect.center, 'sm'))
        Break_falcon.play()
        if count_of_life <= 0:
            running = False
    # Выводим на экран все что нарисовали
    all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
