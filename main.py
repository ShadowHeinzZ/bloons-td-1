import pygame
import sys
import math
import button
import random

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pop = pygame.mixer.Sound('sprites\Bloons\pop.mp3')
pop.set_volume(0.1)

put = pygame.mixer.Sound('sprites\Monkeys\put.mp3')
put.set_volume(0.2)

vendersom = pygame.mixer.Sound('sprites/Monkeys/vender.mp3')
vendersom.set_volume(0.2)

upgradesom = pygame.mixer.Sound('sprites/Monkeys/upgrade.mp3')
upgradesom.set_volume(0.2)

clicksound = pygame.mixer.Sound('sprites\click.mp3')
clicksound.set_volume(0.2)

# Set up the screen
screen_width = 1022
screen_height = 532
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tower Defense Game")



# Load background image
background = pygame.image.load("sprites\map1.png").convert()
menu = pygame.image.load("sprites\Menu.png").convert_alpha()

# Set up the clock
clock = pygame.time.Clock()

# Set up the enemy class


class Bloon:
    def __init__(self, name, life, speed, x, y,pathline):
        self.x = x
        self.y = y
        self.name = name
        self.life = life
        self.speed = speed
        self.camouflage = 0
        self.sprite = pygame.image.load("sprites\Bloons\Red_Bloon.png").convert_alpha()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = [self.x, self.y]
        self.target_x = -200
        self.target_y = 180
        self.pathline = pathline
        self.anteriorx = self.x
        self.anteriory = self.y

    def overlaps(self, other_monkey):
        return self.rect.colliderect(other_monkey.rect)
    
    def move(self):
        if self.x < self.target_x:
            self.x += self.speed
        if self.y < self.target_y:
            self.y += self.speed

        if self.x > self.target_x:
            self.x -= self.speed
        if self.y > self.target_y:
            self.y -= self.speed

        if self.pathline == 1:
            self.target_x = -49
            self.target_y = 180
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 2:
            self.target_x = 390
            self.target_y = 180
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 3:
            self.target_x = 390
            self.target_y = 60
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 4:
            self.target_x = 250
            self.target_y = 60
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 5:
            self.target_x = 250
            self.target_y = 380
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 6:
            self.target_x = 120
            self.target_y = 380
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 7:
            self.target_x = 120
            self.target_y = 270
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 8:
            self.target_x = 500
            self.target_y = 270
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 9:
            self.target_x = 500
            self.target_y = 250
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 10:
            self.target_x = 510
            self.target_y = 140
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 11:
            self.target_x = 600
            self.target_y = 140
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 12:
            self.target_x = 600
            self.target_y = 310
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 13:
            self.target_x = 560
            self.target_y = 340
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 14:
            self.target_x = 350
            self.target_y = 340
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1
        if self.pathline == 15:
            self.target_x = 350
            self.target_y = 530
            if self.x == self.target_x and self.y == self.target_y:
                self.pathline += 1

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))


class Monkey:
    def __init__(self, name, x, y, damage, attacks_per_second):
        self.name = name
        self.x = x
        self.y = y
        self.transformou = False
        self.makeup = 0
        self.damage = damage
        self.pierce = 2
        self.rotation = 0
        self.range = 100  # New attribute
        self.seecamo = False
        self.kills = 0
        self.upgrade1 = 0
        self.upgrade2 = 0
        self.upgrade3 = 0
        self.projectiles = []
        self.spritedart = pygame.image.load(
            "sprites\Monkeys\darts\dart.png").convert_alpha()
        self.sprite = dart_monkey_sprite
        self.sprite_original = self.sprite
        self.attacks_per_second = attacks_per_second
        self.attack_timer = 0
        self.rect = self.sprite.get_rect()

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))
        for projectile in self.projectiles:  # New code
            projectile.draw()

    def find_target(self, value):
        min_distance = float("inf")
        target = None
        if len(Bloons) > 0:
            primeiro = Bloons[0]
            for value in Bloons:
                distance = math.sqrt((value.x - self.x) **
                                    2 + (value.y - self.y) ** 2)
                distancep = math.sqrt((primeiro.x - self.x) **
                                    2 + (primeiro.y - self.y) ** 2)
                if distancep < self.range and value.life > 0 and distance < min_distance:
                    min_distance = distance
                    target = primeiro
                elif distance < self.range and value.life > 0 and distance < min_distance:
                    min_distance = distance
                    target = value
            return target
        

    def fire_projectile(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        speed = 5
        time = distance / speed
        vx = dx / time
        vy = dy / time
        projectile = Projectile(self.x, self.y+20, vx, vy, self.damage, self.pierce, self.spritedart)
        angle = self.get_angle(target.x, target.y)

        # Rotate projectile sprite
        rotated_sprite = pygame.transform.rotate(projectile.sprite, math.degrees(angle))
        projectile.rect = rotated_sprite.get_rect(center=projectile.rect.center)
        projectile.sprite = rotated_sprite

        self.projectiles.append(projectile)
        if target.x-20 < self.x:
            if self.rotation != -90:
                self.sprite = self.sprite_original
                self.sprite = pygame.transform.rotate(self.sprite, -90)
                self.rotation = -90
        elif target.x+20 > self.x:
            if self.rotation != 90:
                self.sprite = pygame.transform.rotate(self.sprite, 90)
                self.rotation = 90

    def get_angle(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        return math.atan2(-dy, dx)

    def update_projectiles(self, Bloons):
        if len(self.projectiles) > 0:
            for projectile in self.projectiles:
                projectile.move()
                if projectile.x > self.x+self.range or projectile.x < self.x-self.range or projectile.y > self.y+self.range or projectile.y < self.y-self.range:
                    self.projectiles.remove(projectile)
                    break
                for Bloon in Bloons:
                    if projectile.collides_with(Bloon):
                        Bloon.life -= projectile.pierce
                        self.kills += 1
                        projectile.life -= 1
                        if projectile.life < 1:
                            self.projectiles.remove(projectile)
                        break


class Projectile:
    def __init__(self, x, y, vx, vy, damage, pierce, spritedart):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = pierce
        self.damage = damage
        self.pierce = pierce
        self.magic = False
        self.sprite = spritedart
        self.rect = self.sprite.get_rect()

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))

    def collides_with(self, Bloon):
        dx = Bloon.x + Bloon.sprite.get_width() / 2 - self.x
        dy = Bloon.y + Bloon.sprite.get_height() / 2 - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance-25 < Bloon.sprite.get_width() / 2:
            return True
        return False

    def update(self, Bloons):
        for Bloon in Bloons:
            if self.collides_with(Bloon):
                Bloon.life -= self.damage
                return True
        self.move()
        return False

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        screen.blit(self.sprite, (self.x, self.y))


# Set up the enemies
Bloons = []
#Bloons.append(Bloon("Red Bloon",1,0.250,-200,180,1))
#Bloons.append(Bloon("Blue Bloon",1,0.500,-200,180,1))
#Bloons.append(Bloon("Green Bloon",1,1,-200,180,1))
#Bloons.append(Bloon("Yellow Bloon",1,2.5,-200,180,1))
#Bloons.append(Bloon("Pink Bloon",1,5,-200,180,1))
Monkeys = []


spawn_timer = 0
spawn_bloon_f = 3000


dinheirox, dinheiroy = 250, 10
rodadasx, rodadasy = 700, 10
heartx, hearty = 60, 10
selmokx, selmoky = 913, 80

font = pygame.font.SysFont("Luckiest Guy Regular", 36, bold=False, italic=False)
fontc = pygame.font.SysFont("Luckiest Guy Regular", 40, bold=False, italic=False)
font2 = pygame.font.SysFont("Luckiest Guy Regular", 20, bold=False, italic=False)
font3 = pygame.font.SysFont("Luckiest Guy Regular", 15, bold=False, italic=False)
coinsimg = pygame.image.load("sprites\coins.png")
heart = pygame.image.load("sprites\heart.png")
vida = 100
mapc = pygame.image.load("sprites\mapc.png")

dart_monkey_sprite = pygame.image.load(
            "sprites\Monkeys\dart_monkey\dart_monkey.png").convert_alpha()

ninja_monkey_sprite = pygame.image.load(
            "sprites\Monkeys\mninja\mninja.png").convert_alpha()


#botoes
start_btn = pygame.image.load('sprites\play.png').convert_alpha()
start_button = button.Button(918, 445, start_btn, 1)

fast_btn = pygame.image.load('sprites\ofastb.png').convert_alpha()
fast_btn = button.Button(918, 445, fast_btn, 1)

fastest_btn = pygame.image.load('sprites\ofastestb.png').convert_alpha()
fastest_btn = button.Button(918, 445, fastest_btn, 1)

dart_monkey_btn = pygame.image.load('sprites\Monkeys\dart_monkey\dart_monkey.png').convert_alpha()
dart_monkey_btn = button.Button(849, 116, dart_monkey_btn, 1)

ninja_monkey_btn = pygame.image.load('sprites\Monkeys\mninja\mninja.png').convert_alpha()
ninja_monkey_btn = button.Button(929, 116, ninja_monkey_btn, 1)



velocidadegame = 60
dt = clock.tick(velocidadegame)
spawningtimes = 50
spawningtimes2 = 50
rodada = 1
grana = 999999
autostart = False
rodadainiciou = False
SelectedMonkey = "Nenhum"
upgradec = False
menuupgrade = False
menuupgradei = pygame.image.load("sprites/Monkeys/upgrades/Menuc.png").convert_alpha()
selectup1 = pygame.image.load("sprites/Monkeys/upgrades/comprar.png").convert_alpha()
selectup1 = button.Button(571, 191, selectup1, 1)
selectup2 = pygame.image.load("sprites/Monkeys/upgrades/comprar.png").convert_alpha()
selectup2 = button.Button(571, 241, selectup2, 1)
selectup3 = pygame.image.load("sprites/Monkeys/upgrades/comprar.png").convert_alpha()
selectup3 = button.Button(571, 291, selectup3, 1)
fecharup = pygame.image.load("sprites/Monkeys/upgrades/fechar.png").convert_alpha()
fecharbtn = button.Button(797, 49, fecharup, 1)
fechar = pygame.image.load("sprites\cancel.png").convert_alpha()
fechar2btn = button.Button(771, 483, fechar, 1)
vender = pygame.image.load("sprites/Monkeys/upgrades/vender.png").convert_alpha()
venderbtn = button.Button(694, 365, vender, 1)
autoinicio = pygame.image.load("sprites\oflashb.png").convert_alpha()
autoiniciobtn = button.Button(831, 446, autoinicio, 1)
autoinicio2 = pygame.image.load("sprites\oflashb2.png").convert_alpha()
autoiniciobtn2 = button.Button(831, 446, autoinicio2, 1)
baloesnatela = 0
while True:
    
    upgrade1ap = 1
    upgrade2ap = 1
    upgrade3ap = 1

    upgrade1texto = ""
    upgrade2texto = ""
    upgrade3texto = ""
    upgrade1preco = ""
    upgrade2preco = ""
    upgrade3preco = ""
    RedBloon = Bloon("Red Bloon",1,1,-100,180,1)
    RedMoab = Bloon("Red Moab",100,1,-100,180,1)
    BlueBloon = Bloon("Blue Bloon",1,2,-100,180,1)
    GreenBloon = Bloon("Green Bloon",1,8,-200,180,1)
    YellowBloon = Bloon("Yellow Bloon",1,5,-200,180,1)
    PinkBloon = Bloon("Pink Bloon",1,10,-200,180,1)
    if SelectedMonkey == "Macaco Dardo":
        spritemacaco = dart_monkey_sprite
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            espaco = 1
            for value in Monkeys:
                dx = value.x + value.sprite.get_width() / 2 - mouse_pos[0]
                dy = value.y + value.sprite.get_height() / 2 - mouse_pos[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if SelectedMonkey == "Nenhum":
                    if distance-1 < value.sprite.get_width() / 2:
                        for value2 in Monkeys:
                            if value2.makeup == 1:
                                value2.makeup = 0
                                menuupgrade = False
                        menuupgrade = True
                        value.makeup = 1
                if SelectedMonkey == "Macaco Dardo":
                    if distance-25 < value.sprite.get_width() / 2:
                        espaco = 0
                if SelectedMonkey == "Macaco Dardo":
                    if distance-30 < value.sprite.get_width() / 2:
                        espaco = 0
            if espaco == 1:
                color = mapc.get_at((mouse_pos[0], mouse_pos[1]))
                if color == (0, 255, 0, 255):
                    if SelectedMonkey == "Macaco Dardo":
                        if grana >= 215:
                            grana -= 215
                            Monkeys.append(Monkey(SelectedMonkey, mouse_pos[0]-20, mouse_pos[1]-20, 2, 0.5))
                            menuupgrade = False
                            put.play()
                    if SelectedMonkey == "Macaco Ninja":
                        if grana >= 540:
                            grana -= 540
                            Monkeys.append(Monkey(SelectedMonkey, mouse_pos[0]-20, mouse_pos[1]-20, 2, 0.7))
                            menuupgrade = False
                            put.play()
                SelectedMonkey = "Nenhum"
                break

    # Draw the background
    screen.blit(background, (0, 0))
    screen.blit(menu, (822, 0))

    if SelectedMonkey != "Nenhum":
        if fechar2btn.draw(screen):
            SelectedMonkey = "Nenhum"
                
    if autoiniciobtn2.draw(screen):
        autostart = True

    if autostart:
        if not rodadainiciou:
            rodadainiciou = True
            velocidadegame = 480
        if autoiniciobtn.draw(screen):
            autostart = False

    
    #Rounds
    if rodadainiciou:
        spawn_timer += dt
        if spawningtimes >= 1:
            if spawn_timer >= spawn_bloon_f:
                if rodada == 1:
                    Bloons.append(RedBloon)
                if rodada < 5 and rodada > 1:
                    percentage_chance_blue = 0.30
                    percentage_chance_red = 0.50
                    if random.random() < percentage_chance_red:
                        Bloons.append(RedBloon)
                    if random.random() < percentage_chance_blue:
                        Bloons.append(BlueBloon)
                if rodada == 5:
                    percentage_chance_blue = 0.50
                    if random.random() < percentage_chance_blue:
                        Bloons.append(BlueBloon)
                    percentage_chance_red = 0.20
                    if random.random() < percentage_chance_red:
                        Bloons.append(RedBloon)
                if rodada > 5 and rodada < 10:
                    percentage_chance_blue = 0.50
                    if random.random() < percentage_chance_blue:
                        Bloons.append(BlueBloon)
                    percentage_chance_red = 0.20
                    if random.random() < percentage_chance_red:
                        Bloons.append(RedBloon)
                    percentage_chance_green = 0.20
                    if random.random() < percentage_chance_green:
                        Bloons.append(GreenBloon)
                if rodada == 10:
                    spawn_bloon_f = 2000
                    percentage_chance_blue = 1
                    if random.random() < percentage_chance_blue:
                        Bloons.append(BlueBloon)
                if rodada > 10 and rodada < 15:
                    percentage_chance_blue = 0.2
                    if random.random() < percentage_chance_blue:
                        Bloons.append(BlueBloon)
                    percentage_chance_red = 0.5
                    if random.random() < percentage_chance_red:
                        Bloons.append(RedBloon)
                    percentage_chance_green = 0.3
                    if random.random() < percentage_chance_green:
                        Bloons.append(GreenBloon)
                    percentage_chance_yellow = 0.3
                    if random.random() < percentage_chance_yellow:
                        Bloons.append(YellowBloon)
                if rodada >= 15 and rodada < 20:
                    percentage_chance_green = 0.7
                    if random.random() < percentage_chance_green:
                        Bloons.append(GreenBloon)
                    percentage_chance_yellow = 0.5
                    if random.random() < percentage_chance_yellow:
                        Bloons.append(YellowBloon)
                    percentage_chance_pink = 0.4
                    if random.random() < percentage_chance_pink:
                        Bloons.append(PinkBloon)
                if rodada == 20:
                    spawningtimes = 1
                    Bloons.append(RedMoab)
                spawn_timer = 0
                spawningtimes -= 1
        elif len(Bloons) == 0:
            spawningtimes2 += 15
            if spawn_bloon_f > 300:
                spawn_bloon_f -= 50
            spawningtimes = spawningtimes2
            rodada += 1
            grana += 50+spawningtimes+rodada
            rodadainiciou = False
            velocidadegame = 60


    # Move and draw the enemies
    for value in Monkeys:
        value.draw()
        target = value.find_target(Bloons)
        if target:
            if value.attack_timer >= 1000 / value.attacks_per_second:
                value.fire_projectile(target)
                value.attack_timer = dt / value.attacks_per_second
            else:
                value.attack_timer += dt
        if value.name == "Macaco Ninja":
            if value.transformou == False:
                if value.sprite != pygame.image.load("sprites\Monkeys\mninja\mninja.png").convert_alpha():
                    value.sprite = pygame.image.load("sprites\Monkeys\mninja\mninja.png").convert_alpha()
                    value.sprite_original = value.sprite
                    value.rotation = 0
                    value.range = 125
                    value.transformou = True
                    value.spritedart = pygame.image.load("sprites\Monkeys\darts\shuriken.png").convert_alpha()
        if len(value.projectiles) > 0:
            value.update_projectiles(Bloons)

    for value in Bloons[:20]:
        if value.name == "Blue Bloon":
            if value.sprite != pygame.image.load("sprites\Bloons\Blue_Bloon.png").convert_alpha():
                value.sprite = pygame.image.load("sprites\Bloons\Blue_Bloon.png").convert_alpha()
        if value.name == "Green Bloon":
            if value.sprite != pygame.image.load("sprites\Bloons\Green_Bloon.png").convert_alpha():
                value.sprite = pygame.image.load("sprites\Bloons\Green_Bloon.png").convert_alpha()
        if value.name == "Yellow Bloon":
            if value.sprite != pygame.image.load("sprites\Bloons\Yellow_Bloon.png").convert_alpha():
                value.sprite = pygame.image.load("sprites\Bloons\Yellow_Bloon.png").convert_alpha()
        if value.name == "Pink Bloon":
            if value.sprite != pygame.image.load("sprites\Bloons\Pink_Bloon.png").convert_alpha():
                value.sprite = pygame.image.load("sprites\Bloons\Pink_Bloon.png").convert_alpha()
        if value.name == "Red Moab":
            if value.sprite != pygame.image.load("sprites\Bloons\moabs\Red_moab.png").convert_alpha():
                value.sprite = pygame.image.load("sprites\Bloons\moabs\Red_moab.png").convert_alpha()

        
        value.anteriorx = value.x
        value.anteriory = value.y
        value.move()
        value.draw()

        if value.y == value.anteriory and value.x == value.anteriorx:
            value.x = value.target_x
            value.y = value.target_y
            value.move()
        
        if value.life < 1:
            if(value.name == "Blue Bloon"):
                Bloons.append(Bloon("Red Bloon", 1,1,value.x-5, value.y-5,value.pathline))
                Bloons.append(Bloon("Red Bloon", 1,1,value.x+5, value.y+5,value.pathline))
            if(value.name == "Green Bloon"):
                Bloons.append(Bloon("Blue Bloon", 1,2,value.x-5, value.y-5,value.pathline))
                Bloons.append(Bloon("Blue Bloon", 1,2,value.x+5, value.y+5,value.pathline))
            if(value.name == "Yellow Bloon"):
                Bloons.append(Bloon("Green Bloon", 1,2,value.x-5, value.y-5,value.pathline))
                Bloons.append(Bloon("Green Bloon", 1,2,value.x+5, value.y+5,value.pathline))
            if(value.name == "Pink Bloon"):
                Bloons.append(Bloon("Yellow Bloon", 1,5,value.x-5, value.y-5,value.pathline))
                Bloons.append(Bloon("Yellow Bloon", 1,5,value.x+5, value.y+5,value.pathline))

            #Moabs abaixo

            if(value.name == "Red Moab"):
                for i in range(13):
                    Bloons.append(Bloon("Red Bloon", 1,1,value.x-i, value.y,value.pathline))
                    Bloons.append(Bloon("Red Bloon", 1,1,value.x+i, value.y,value.pathline))
                    Bloons.append(Bloon("Red Bloon", 1,1,value.x, value.y-i,value.pathline))
                    Bloons.append(Bloon("Red Bloon", 1,1,value.x, value.y+i,value.pathline))
                    Bloons.append(Bloon("Blue Bloon", 1,2,value.x, value.y,value.pathline))
                    Bloons.append(Bloon("Green Bloon", 1,2.5,value.x, value.y,value.pathline))
                    Bloons.append(Bloon("Yellow Bloon", 1,5,value.x, value.y,value.pathline))
                    Bloons.append(Bloon("Pink Bloon", 1,10,value.x, value.y,value.pathline))
            grana += 2
            pop.play()
            Bloons.remove(value)
        if value.pathline == 16:
            vida -= value.life
            Bloons.remove(value)
      
    

    # Update the display
    dinheiro = font.render(f"${grana}", True, (255, 255, 255))
    contornodinheiro = fontc.render(f"${grana}", True, (0, 0, 0))
    screen.blit(contornodinheiro, (dinheirox-2, dinheiroy+2))
    screen.blit(dinheiro, (dinheirox, dinheiroy))
    screen.blit(coinsimg, (dinheirox-55, dinheiroy-2))

    vidatexto = font.render(f"{vida}", True, (255, 255, 255))
    contornovida = fontc.render(f"{vida}", True, (0, 0, 0))
    screen.blit(contornovida, (heartx-2, hearty+2))
    screen.blit(vidatexto, (heartx, hearty))
    screen.blit(heart, (heartx-55, hearty-2))

    rodadastexto = font.render(f"{rodada}/100", True, (255, 255, 255))
    contornorodadas = font.render(f"{rodada}/100", True, (0, 0, 0))
    screen.blit(contornorodadas, (rodadasx-2, rodadasy+2))
    screen.blit(rodadastexto, (rodadasx, rodadasy))

    selmoktext = font2.render(f"{SelectedMonkey}", True, (255, 255, 255))
    selmokcontorn = font2.render(f"{SelectedMonkey}", True, (0, 0, 0))
    selmokrect = selmoktext.get_rect()
    selmokrect.center = selmokx, selmoky
    screen.blit(selmokcontorn, (selmokrect.x-2, selmokrect.y+2))
    screen.blit(selmoktext, selmokrect)

    dartmonkeyprice = font2.render(f"$215", True, (255, 255, 255))
    dartmonkeypricerect = dartmonkeyprice.get_rect()
    dartmonkeypricerect.center = 870, 175
    screen.blit(dartmonkeyprice, dartmonkeypricerect)

    ninjamonkeyprice = font2.render(f"$540", True, (255, 255, 255))
    ninjamonkeypricerect = ninjamonkeyprice.get_rect()
    ninjamonkeypricerect.center = 950, 175
    screen.blit(ninjamonkeyprice, ninjamonkeypricerect)


    #Botões
    if start_button.draw(screen):
        rodadainiciou = True
    if rodadainiciou:
        if fast_btn.draw(screen):
            velocidadegame = 480
    if velocidadegame == 480:
        if fastest_btn.draw(screen):
            velocidadegame = 60
    

    if SelectedMonkey == "Macaco Ninja":
        monkey_surface = pygame.Surface((SelectedMonkey2.get_width(), SelectedMonkey2.get_height()), pygame.SRCALPHA)
        monkey_surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(monkey_surface, (255, 255, 255), monkey_surface.get_rect(), 2)
        screen.blit(monkey_surface, (929, 116))
    elif SelectedMonkey == "Macaco Dardo":
        monkey_surface = pygame.Surface((SelectedMonkey2.get_width(), SelectedMonkey2.get_height()), pygame.SRCALPHA)
        monkey_surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(monkey_surface, (255, 255, 255), monkey_surface.get_rect(), 2)
        screen.blit(monkey_surface, (849, 116))


    if dart_monkey_btn.draw(screen):
        SelectedMonkey = "Macaco Dardo"
        SelectedMonkey2 = dart_monkey_sprite
    if ninja_monkey_btn.draw(screen):
        SelectedMonkey = "Macaco Ninja"
        SelectedMonkey2 = ninja_monkey_sprite


    #Menu upgrade ---------------------------------------------------------------------------
    if menuupgrade:
        for value in Monkeys:
            if value.makeup == 1:
                if value.name == "Macaco Dardo":
                    selmok3 = dart_monkey_sprite
                    monkey_surface2 = pygame.Surface((selmok3.get_width()+value.range, selmok3.get_height()+value.range), pygame.SRCALPHA)
                    monkey_surface2.fill((0, 0, 0, 0))
                    pygame.draw.ellipse(monkey_surface2, (255, 255, 255), monkey_surface2.get_rect(), 2)
                    screen.blit(monkey_surface2, (value.x-value.range/2, value.y-value.range/2))
        screen.blit(menuupgradei, (542,43))
        for value in Monkeys:
            if value.makeup == 1:
                if value.name == "Macaco Dardo":
                    selmok3 = "Macaco Dardo"
                    precovenda = 115
                    screen.blit(value.sprite, (658, 110))
                    #UPGRADE 100
                    if value.upgrade2 == 0 or value.upgrade3 == 0:
                        if value.upgrade1 == 0:
                            upgrade1texto = "Tiro certo"
                            upgrade1preco = 150
                            if selectup1.draw(screen):
                                if grana >= upgrade1preco:
                                    grana -= upgrade1preco
                                    value.pierce += 1
                                    upgradesom.play()
                                    value.upgrade1 += 1
                        if value.upgrade1 == 1:
                            upgrade1texto = "Tiro certo de lâminas"
                            upgrade1preco = 235
                            if selectup1.draw(screen):
                                if grana >= upgrade1preco:
                                    grana -= upgrade1preco
                                    value.pierce += 2
                                    upgradesom.play()
                                    value.upgrade1 += 1
                        if value.upgrade1 == 2:
                            if value.upgrade2 < 3 and value.upgrade3 < 3:
                                upgrade1texto = "Catapulta de espinhos"
                                upgrade1preco = 325
                                if selectup1.draw(screen):
                                    if grana >= upgrade1preco:
                                        grana -= upgrade1preco
                                        value.spritedart = pygame.image.load(
            "sprites/Monkeys/darts/jamanta.png").convert_alpha()
                                        value.range += (value.range/100)*25
                                        value.attacks_per_second -= (value.attacks_per_second/100)*25
                                        upgradesom.play()
                                        value.upgrade1 += 1
                            else:
                                upgrade1ap = 0
                        if value.upgrade1 == 3:
                            upgrade1texto = "Jamanta"
                            upgrade1preco = 1945
                            if selectup1.draw(screen):
                                if grana >= upgrade1preco:
                                    grana -= upgrade1preco
                                    value.pierce = value.pierce*2
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/jamanta.png").convert_alpha()
                                    value.sprite_original = value.sprite
                                    value.rotation = 0
                                    value.rect = value.sprite.get_rect()
                                    value.spritedart = pygame.image.load(
            "sprites/Monkeys/darts/jamanta.png").convert_alpha()
                                    upgradesom.play()
                                    value.upgrade1 += 1
                        if value.upgrade1 == 4:
                            upgrade1texto = "UltraJamanta"
                            upgrade1preco = 16200
                            if selectup1.draw(screen):
                                if grana >= upgrade1preco:
                                    grana -= upgrade1preco
                                    value.pierce = value.pierce*3
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/ultrajamanta.png").convert_alpha()
                                    value.sprite_original = value.sprite
                                    value.rotation = 0
                                    value.spritedart = pygame.image.load(
            "sprites/Monkeys/darts/ultrajamanta.png").convert_alpha()
                                    upgradesom.play()
                                    value.upgrade1 += 1
                        if value.upgrade1 == 5:
                            upgrade1ap = 0
                    else:
                        upgrade1ap = 0
                    #UPGRADE 010
                    if value.upgrade1 == 0 or value.upgrade3 == 0:
                        if value.upgrade2 == 0:
                            upgrade2texto = "Tiros rápidos"
                            upgrade2preco = 110
                            if selectup2.draw(screen):
                                if grana >= upgrade2preco:
                                    value.attacks_per_second += (value.attacks_per_second/100)*17.6
                                    upgradesom.play()
                                    value.upgrade2 += 1
                        if value.upgrade2 == 1:
                            upgrade2texto = "Tiros muito rápidos"
                            upgrade2preco = 295
                            if selectup2.draw(screen):
                                if grana >= upgrade2preco:
                                    value.attacks_per_second += (value.attacks_per_second/100)*50
                                    upgradesom.play()
                                    value.upgrade2 += 1
                        if value.upgrade2 == 2:
                            if value.upgrade1 < 3 and value.upgrade3 < 3: 
                                upgrade2texto = "Tiro Triplo"
                                upgrade2preco = 430
                                if selectup2.draw(screen):
                                    if grana >= upgrade2preco:
                                        upgradesom.play()
                                        value.pierce += value.pierce*3
                                        value.upgrade2 += 1
                            else:
                                upgrade2ap = 0
                        if value.upgrade2 == 3:
                            upgrade2texto = "Fã clube do super macaco"
                            upgrade2preco = 8640
                            if selectup2.draw(screen):
                                if grana >= upgrade2preco:
                                    grana -= upgrade2preco
                                    value.range += (value.range/100)*25
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/supermonkey.png").convert_alpha()
                                    value.rotation = 0
                                    value.sprite_original = value.sprite
                                    upgradesom.play()
                                    value.upgrade2 += 1
                        if value.upgrade2 == 4:
                            upgrade2texto = "Fã clube do super macaco de plasma"
                            upgrade2preco = 48600
                            if selectup2.draw(screen):
                                if grana >= upgrade2preco:
                                    grana -= upgrade2preco
                                    value.pierce += 5
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/plasmamoki.png").convert_alpha()
                                    value.sprite_original = value.sprite
                                    value.rotation = 0
                                    value.attacks_per_second = value.attacks_per_second*2
                                    upgradesom.play()
                                    value.upgrade2 += 1
                        if value.upgrade2 == 5:
                            upgrade2ap = 0
                    else:
                        upgrade2ap = 0
                    #UPGRADE 001
                    if value.upgrade1 == 0 or value.upgrade2 == 0:
                        if value.upgrade3 == 0:
                            upgrade3texto = "Dardos de longo alcance"
                            upgrade3preco = 95
                            if selectup3.draw(screen):
                                if grana >= upgrade3preco:
                                    grana -= upgrade3preco
                                    value.range += (value.range/100)*25
                                    value.upgrade3 += 1
                        if value.upgrade3 == 1:
                            upgrade3texto = "Mira melhorada"
                            upgrade3preco = 215
                            if selectup3.draw(screen):
                                if grana >= upgrade3preco:
                                    value.seecamo = True
                                    value.range += (value.range/100)*25
                                    grana -= upgrade3preco
                                    value.upgrade3 += 1
                        if value.upgrade3 == 2:
                            if value.upgrade1 < 3 and value.upgrade2 < 3: 
                                upgrade3texto = "Besta"
                                upgrade3preco = 675
                                if selectup3.draw(screen):
                                    if grana >= upgrade3preco:
                                        value.damage += 1
                                        value.pierce += 1
                                        value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/crossbow1.png").convert_alpha()
                                        value.sprite_original = value.sprite
                                        grana -= upgrade3preco
                                        value.range += (value.range/100)*25
                                        value.upgrade3 += 1
                            else:
                                upgrade3ap = 0
                        if value.upgrade3 == 3:
                            upgrade3texto = "Atirador afiado"
                            upgrade3preco = 2160
                            if selectup3.draw(screen):
                                if grana >= upgrade3preco:
                                    grana -= upgrade3preco
                                    value.attacks_per_second = value.attacks_per_second*2
                                    value.damage += 3
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/crossbow2.png").convert_alpha()
                                    value.sprite_original = value.sprite
                                    value.rotation = 0
                                    upgradesom.play()
                                    value.upgrade3 += 1
                        if value.upgrade3 == 4:
                            upgrade3texto = "Mestre da besta"
                            upgrade3preco = 48600
                            if selectup3.draw(screen):
                                if grana >= upgrade3preco:
                                    grana -= upgrade3preco
                                    value.pierce += 2
                                    value.sprite = pygame.image.load(
            "sprites/Monkeys/dart_monkey/upgrades/crossbow3.png").convert_alpha()
                                    value.sprite_original = value.sprite
                                    value.rotation = 0
                                    value.attacks_per_second = value.attacks_per_second*5.8
                                    upgradesom.play()
                                    value.upgrade3 += 1
                        if value.upgrade3 == 5:
                            upgrade3ap = 0
                    else:
                        upgrade3ap = 0
                elif value.name == "Macaco Ninja":
                    selmok3 = "Macaco Ninja"
                    precovenda = 415
                    screen.blit(ninja_monkey_sprite, (658, 110))

                if value.upgrade2 == 0 or value.upgrade3 == 0:
                    if upgrade1ap == 1:
                        upgrade1text = font3.render(f"{upgrade1texto}  ${upgrade1preco}", True, (0, 128, 0))
                        selectup1rect = upgrade1text.get_rect()
                        selectup1rect.center = selectup1.rect.center
                        screen.blit(upgrade1text, (selectup1rect))
                    else:
                        upgrade1text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                        selectup1rect = upgrade1text.get_rect()
                        selectup1rect.center = selectup1.rect.center
                        screen.blit(upgrade1text, (selectup1rect))
                else:
                    upgrade1text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                    selectup1rect = upgrade1text.get_rect()
                    selectup1rect.center = selectup1.rect.center
                    screen.blit(upgrade1text, (selectup1rect))
                if value.upgrade1 == 0 or value.upgrade3 == 0:
                    if upgrade2ap == 1:
                        upgrade2text = font3.render(f"{upgrade2texto}  ${upgrade2preco}", True, (0, 128, 0))
                        selectup2rect = upgrade2text.get_rect()
                        selectup2rect.center = selectup2.rect.center
                        screen.blit(upgrade2text, (selectup2rect))
                    else:
                        upgrade2text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                        selectup2rect = upgrade2text.get_rect()
                        selectup2rect.center = selectup2.rect.center
                        screen.blit(upgrade2text, (selectup2rect))
                else:
                    upgrade2text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                    selectup2rect = upgrade2text.get_rect()
                    selectup2rect.center = selectup2.rect.center
                    screen.blit(upgrade2text, (selectup2rect))
                if value.upgrade1 == 0 or value.upgrade2 == 0:
                    if upgrade3ap == 1:  
                        upgrade3text = font3.render(f"{upgrade3texto}  ${upgrade3preco}", True, (0, 128, 0))
                        selectup3rect = upgrade3text.get_rect()
                        selectup3rect.center = selectup3.rect.center
                        screen.blit(upgrade3text, (selectup3rect))
                    else:
                        upgrade3text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                        selectup3rect = upgrade3text.get_rect()
                        selectup3rect.center = selectup3.rect.center
                        screen.blit(upgrade3text, (selectup3rect))
                else:
                    upgrade3text = font2.render(f"Caminho Fechado / Max", True, (255, 255, 255))
                    selectup3rect = upgrade3text.get_rect()
                    selectup3rect.center = selectup3.rect.center
                    screen.blit(upgrade3text, (selectup3rect))

                selmok3text = font2.render(f"{selmok3}", True, (255, 255, 255))
                selmok3rect = selmok3text.get_rect()
                selmok3rect.center = 682, 60
                screen.blit(selmok3text, selmok3rect)

                kills = font2.render(f"{value.kills}", True, (255, 255, 255))
                screen.blit(kills, (664, 76))

                vendert = font2.render(f"${precovenda}", True, (255, 255, 255))
                screen.blit(vendert, (596, 382))



                
                if fecharbtn.draw(screen):
                    menuupgrade = False

                if venderbtn.draw(screen):
                    menuupgrade = False
                    grana += precovenda
                    Monkeys.remove(value)
                    vendersom.play()

    



    pygame.display.update()
    if vida < 1:
        pygame.quit()
        sys.exit()
    

    # Limit the frame rate
    clock.tick(velocidadegame)
