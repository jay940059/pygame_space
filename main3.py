import pygame
import random
import math
import time

pygame.init()
pygame.font.init()

# 參數設定
screen_width = 600
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height))
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
VEL = 3
FPS = 60
# kill=0
# welcome、play、end
state = 'welcome'
# life = 10
clock = pygame.time.Clock()
player_bullet = []
start_time = time.time()

def welcome_screen():

    screen.fill(BLACK)

    font = pygame.font.Font(None, 50)

    text = font.render("press ENTER to start", False, YELLOW)

    screen.blit(text, (screen_width / 2 - text.get_width() / 2, 225))

def play_screen():
    screen.fill((0,0,0))
    show_player()
    show_enemy()
    show_player_bullett()
    show_life()
    show_timer()
    show_kill()
    which_level(now_time)

def end_screen():

    screen.fill((0,0,0))
    font = pygame.font.Font(None, 30)
    game_over = font.render("GAME OVER", False, (255,255,255))
    font = pygame.font.Font(None, 25)
    points = font.render("score: " + str(kill), False, (255,255,255))
    font = pygame.font.Font(None, 22)
    restart = font.render("press ENTER to play again", False, (255,255,255))
    screen.blit(game_over,(600 / 2 - game_over.get_width() / 2, 100))
    screen.blit(points, (600 / 2 - points.get_width() / 2, 200))
    screen.blit(restart, (600 / 2 - restart.get_width() / 2, 300))

# 處理首頁
def handle_welcome(e):
    # 顯示歡迎畫面
    welcome_screen()
    # 偵測鍵盤 Enter 事件
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        play()


def handle_play(e):
    play_screen()
    key = pygame.key.get_pressed()
    player_move(key)

def handle_end(e):
    # 偵測鍵盤 Enter 事件
    end_screen()
    if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
        print('yes')
        play()

# Player設定
player_height = 60
player_width = 60
player = pygame.Rect(430,400,player_width,player_height)
playerImg = pygame.image.load('gun.png')
playerImg = pygame.transform.scale(playerImg,(player_width,player_height))

def player_move(key):
    if key[pygame.K_LEFT] and player.x>=0 : #LEFT
        player.x -= VEL
    if key[pygame.K_RIGHT] and player.x+VEL+player.width<=screen_width: #RIGHT
        player.x += VEL
    if key[pygame.K_SPACE] :
        if (len(player_bullet)>0 and player_bullet[-1].y<=350) or len(player_bullet)== 0 :
            bullet = pygame.Rect(player.x + player.width//2-15, player.y - 5,30,30)
            player_bullet.append(bullet)
        

def show_player():
    screen.blit(playerImg,(player.x,player.y))


def show_timer():
    # 現在的時間 - 開始時間 = 經過的秒數
    global now_time
    now_time = time.time()-start_time
    font = pygame.font.Font(None, 28)
    text = font.render(str(int(now_time)), False, (255,255,255))
    screen.blit(text, (370, 0))

def play():
    global state,life,now_time,start_time,kill,all_enemy
    all_enemy=[]
    kill=0
    start_time = time.time()
    life = 10
    state = 'play'
    
def end():
    global state,kill
    state = 'end'
    
def show_kill():
    font = pygame.font.Font(None, 100)
    text = font.render(str(kill), False, (255,255,0))
    screen.blit(text,(0,50))
# enemy設定
class enemy:
    def __init__(self) -> None:
        self.life = 3
        self.x = random.randint(0,500)
        self.y = 0
        self.x_change = random.randint(0,3)
        

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2)) + (math.pow(enemyY-bulletY,2)))
    if distance < 30:
        return True

enemy_height = 60
enemy_width = 60

all_enemy = []
enemyImg = pygame.image.load('enemy.png')
enemyImg = pygame.transform.scale(enemyImg,(enemy_width,enemy_height))

def which_level(now_time):
    level = now_time//5 +1 
    if int(now_time)%10 == 0 :
        for i in range(int(level)-len(all_enemy)):
            if len(all_enemy)>0 and all_enemy[-1].y<200:
                next_enemy = enemy()
                next_enemy.y = all_enemy[-1].y-50
                all_enemy.append(next_enemy)
            elif len(all_enemy)==0:
                all_enemy.append(enemy())

def show_enemy():
    global life,kill
    font = pygame.font.Font(None, 30)
    for i in all_enemy:
        i.x+= i.x_change
        i.y+=1
        if i.x<0 or i.x>=570:
            i.x_change *= -1
        if i.life<= 0 or i.y>= 500:
            if i.life<=0:
                kill += 1
            all_enemy.remove(i)
        if i.life>0:
            text = font.render(str(i.life), False, (255,255,0))
            screen.blit(enemyImg,(i.x,i.y))
            screen.blit(text,(i.x+15,i.y-10))
        if isCollision(i.x,i.y,player.x,player.y):
            if i in all_enemy:
                all_enemy.remove(i)
                life -=1

bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg,(30,30))

def show_player_bullett():
    for i in player_bullet:
        i.y -= 5
        screen.blit(bulletImg,(i.x,i.y))
        if i.y < 0:
            player_bullet.remove(i)
        for j in all_enemy:
            if isCollision(j.x+30,j.y+30,i.x+30,i.y+30):
                if i in player_bullet:
                    player_bullet.remove(i)
                    j.life-=1

def show_life():
    if life<=0:
        end()
    font = pygame.font.Font(None, 100)
    text = font.render(str(life), False, (255,255,0))
    screen.blit(text,(0,0))




run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    if state == 'welcome':
        handle_welcome(event)
    if state == 'play':
        handle_play(event)
    if state == 'end':
        handle_end(event)

    pygame.display.update()