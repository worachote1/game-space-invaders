import pygame
from pygame import mixer # mixer คือ classที่ช่วยเราจัดการเรื่อง เสียงภายใน game ของเรา
import random
import math

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1) # ใส่ -1 แล้วจะเล่นดนตรี แบบ วนloopให้

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo (1).png")
pygame.display.set_icon(icon)

# Player ตัวจรวด
playerImg = pygame.image.load("space-invaders.png")
playerX = 370
playerY = 470
playerX_Change = 0

# Enemy ตัวเอเลี่ยน
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6 # มี enemy เป็นเอเลี่ยน 6 ตัว

for i in range(0,num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,(800-64)))
    enemyY.append(random.randint(0,150))
    enemyX_Change.append(2)
    enemyY_Change.append(15)

# Bullet ตัวกระสุน

# สถานะของ bullet มี 2 อันได้แก่
# ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletx = 0
bulletY = 470
bulletX_Change = 0
bulletY_Change = 6
bullet_state = "ready"

# Score นับคะแนน

score_value = 0
font = pygame.font.Font("freesansbold.ttf",34)
textX = 10
textY = 10

# Game Over text
gameover_font = pygame.font.Font("freesansbold.ttf",84)



def show_score(x,y):
    score = font.render("Score : "+str(score_value),True,(0,128,128))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = font.render("GAME OVER ", True, (0, 128 , 128))
    screen.blit(over_text, (200, 300))


def player(x, y):  # ผู้เล่นเป็นจรวด
    screen.blit(playerImg, (x, y))  # ใช้ blit() วาดรูป player ใน screen


def enemy(x, y,i):  # ศัตรูเป็นเอเลี่ยน
    screen.blit(enemyImg[i ], (x, y))  # ใช้ blit() วาดรูป enemy ใน screen

def fire_bullet(x,y): #การยิงกระสุน
    global bullet_state #access bullet_state inside function เลยต้องเป็น global
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10)) #ถ้าไม่บวก x และ y เพิ่มตามนี้ bullet จะถูกยิงไปทางซ้ายนิดนึง

def isCollision(enemyX,enemyY,bulletx,bulletY) : # การชนกันของ bullet กับ enemy
    distance = math.sqrt((math.pow(enemyX-bulletx,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27 :
        return True
    else:
        return False

# Game Loop
running = True
while running: # เราอยากให้อะไรคงอยู่่ใน pygame เราต้อง ใส่ code ส่วนนั้นใน while loop
    screen.fill((0, 128,128))  # ทําให้ background ของ screen เป็น RGB = red,green,blue และ ต้องให้โค้ดนี้อยู่บน ทุก image เพราะ screen ถูกวาดก่อนเสมอไม่งั้นรูปที่มาก่อนจะถูกทับ

    #วาด Background Image
    screen.blit(background,(0,0))

    for event in pygame.event.get():  # วน loop through all the events that are being stored inside
        if event.type == pygame.QUIT:  # ช่วยทําให้กดปุ่มปิด Window ได้(การกดปุ่มปิดเกม เป็น event ที่เกิดขึ้นในโปรแกรมของเรา) ซึ่งทําให้ออกจากโปรแกรมได้
            running = False
        if event.type == pygame.KEYDOWN:  # if keystroke is pressed check whether it's right or left
            print("A keystoke is pressed")
            if event.key == pygame.K_LEFT:
                print("Left arrow is pressed")
                playerX_Change = -5

            if event.key == pygame.K_RIGHT:
                print("Right arrow is pressed")
                playerX_Change = 5

            if event.key == pygame.K_SPACE: #เมื่อกด spacebar จะเริ่มการ move ของ bullet
                if bullet_state is "ready" :
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # Get the current x cordinate of spaceship (bullet อยู่ในscreen ตําแหน่งเดียวกับจรวดในตอนแรก)
                    bulletx = playerX
                    fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change

    # กําหนดขอบเขตไม่ให้ จรวด moveแนวแกน x ออกนอก window
    if playerX <= 0:
            playerX = 0
    elif playerX >= (800 - 64):  # ที่ต้องลบ 64 เพราะ ขนาดรูปจรวดที่เรานํามาใช้ มี ขนาด 64 pixels มันจึงกว้าง 64 แต่เราต้องการให้ move ออกจากขอบไม่ไดแม้แต่ส่วนเดียวของจรวด
            playerX = 800 - 64

    #Enemy monement
    for i in range(0,num_of_enemies): #มี enemy เป็น เอเลี่ยน 6 ตัว

        #Game over
        if enemyY[i] > 440 :
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break






        enemyX[i] += enemyX_Change[i]
        # กําหนดขอบเขตไม่ให้ เอเลี่ยน moveแนวแกน x ออกนอก window
        if enemyX[i] <= 0:
                enemyX_Change[i] = 2
                enemyY[i] += enemyY_Change[i]

        elif enemyX[i] >= (800 - 64):  # ที่ต้องลบ 64 เพราะ ขนาดรูปเอเลี่ยนที่เรานํามาใช้ มี ขนาด 64 pixels มันจึงกว้าง 64 แต่เราต้องการให้ move ออกจากขอบไม่ไดแม้แต่ส่วนเดียวของจรวด
                enemyX_Change[i] = -2
                enemyY[i] += enemyY_Change[i]

        # Collision การชนกัน
        collision = isCollision(enemyX[i], enemyY[i], bulletx, bulletY)
        if collision:  # ยิงโดน enemy
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1  # ทุกครั้งที่ยิงโดน เพิ่ม 1 คะแนน

            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(0, 150)

        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement

    if bullet_state is "fire" :
        fire_bullet(bulletx,bulletY)
        bulletY -= bulletY_Change

    if bulletY <= 0:
        bulletY = 470
        bullet_state = "ready"


    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()  # update

# Trick เล็กๆใน pycharm กด Ctrl+Alt+L จะ จัดรูป code ให้เป็นระเบียบมากขึ้น