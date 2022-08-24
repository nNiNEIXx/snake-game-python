#############  กำหนดตัวเเปล  ############## ปัน

#importโมดูมต่างๆ
import pygame as py
import sys as sys
import time as t
import random as rd


#ความยาก
difficulty = 60

#ขนาดหน้าต่าง
frame_x = 1280
frame_y = 720

#ทิศทาง
start = 'RIGHT'
direction = start

#กำหนดตัวเเปล บูลีน
food_spawn = True
Boot = False
Run = False
play1 = False


#scoreเริ่มต้น
score = 0

#สี
black = py.Color(0, 0, 0)
white = py.Color(255, 255, 255)
green = py.Color(0, 100, 0)
red = py.Color(255, 0, 0)
Brown = py.Color(150, 75, 0)

#ตำแหน่งงู
snake_pos = [100, 200]
snake_body = [[100, 200], [90, 200], [80, 200]]

#ตำแหน่งอาหาร
food = [rd.randrange(1, 128) * 10, rd.randrange(1, 72) * 10]

errors = py.init()

#ตั่งค่าหน้าจอ
Window = py.display.set_mode((frame_x, frame_y))

#ตั่งค่าfps
fps_controller = py.time.Clock()

#ตั่งค่า icon
py.display.set_caption('เกมงู')
icon = py.image.load("assets\iconsnake.png")
py.display.set_icon(icon)

#นำเข้ารูป
lose = py.image.load("assets\loes.png")
load = py.image.load('assets\loading.png')
cadis = py.image.load('assets\cadis.png')
BG_manu = py.image.load("assets/Backgroundmanu.png")
BG_game = py.image.load("assets/Backgroundgame.png")
How_to_play = py.image.load("assets\Howtoplay.png")

#นำเข้าเสียง
song = py.mixer.Sound('assets\song.mp3')
song.set_volume(0.5)
song.play(-1)

sound = py.mixer.Sound('assets\R.mp3')
sound.set_volume(0.5)

Oofsound = py.mixer.Sound('assets\Oof!.mp3')
Oofsound.set_volume(0.5)

bootsound = py.mixer.Sound('assets\Boot.mp3')
bootsound.set_volume(0.1)

dash = py.mixer.Sound('assets\Dash.mp3')
dash.set_volume(0.2)

press = py.mixer.Sound('assets\Press.mp3')
press.set_volume(0.5)

################  ฟังชั่นการเริ่มใหม่/font ###################### ฝ้าย

# ตั้งค่าfont
def get_font(size):
    return py.font.Font("assets/font.otf", size)

# การเริ่มใหม่
def re_game():
    # นำเข้า ตัวเเปลจากนอกฟังชัน
    global snake_pos, snake_body
    global food, food_spawn
    global start, direction, score

    # ตำเเหน่งงู
    snake_pos = [100, 200]
    snake_body = [[100, 200], [90, 200], [80, 200]]

    # การสุ่มอาหาร
    food = [rd.randrange(1, 128) * 10, rd.randrange(1, 72) * 10]
    food_spawn = True

    # ทิศทาง
    start = 'RIGHT'
    direction = start

    # score เริ่มต้น
    score = 0

# show_score
def show_score(choice, color, font, size):

    score_font = py.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()

    #ถ้า choice score = 1 จะโชว
    if choice == 1:
        score_rect.midtop = (frame_x / 10, 650)
    else:
        score_rect.midtop = (frame_x / 2, frame_y / 1.5)
    Window.blit(score_surface, score_rect)

# หน้าต่าง game over
def game_over():

    # ภาพพื่นหลัง
    Window.blit(lose, (0, 0))
    # เรียกใช้เสียง
    Oofsound.play()
    # เรียกใช้บรรทัด 130 ก่อนเเล้วค่อนใช้ sleep
    py.display.flip()
    # หยุดเวลา 1วิ
    t.sleep(1)
    # ใช้ฟังชัน การเริ่มใหม่
    re_game()

####################### ฟังชั่นหน้า Button ######################### โช
class Button():

    # ฟังชั่นหลักข้อความ
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):

        #กำหนดตัวเเปล
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color,self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        # ถ้าไม่มีรูป text จะกลายเป็นรูปเเทน
        if self.image is None:
            self.image = self.text

        # ตำเเหน่งของรุปกับข้อความ
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    # เเสดงข้อความ
    def update(self, screen): 
        if self.image is not None:
            screen.blit(self.image, self.rect)

        screen.blit(self.text, self.text_rect)

    # ตรวจสอบตำเเหน่งเมาส์
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    # เปลียนสี ข้อความ
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

####################### ฟังชั่นหน้า manu ######################### โอ้ต

# ฟังชันหน้า load
def game_start():

    # นำเข้าตัวเเปลจากนอกฟังชั่น
    global Run
    # พื่นหลัง load
    Window.blit(load, (0, 0))
    # เรียกใช้บรรทัด 149 ก่อนเเล้วค่อนใช้ sleep
    py.display.flip()
    # หยุดเวลา 3 วิ
    t.sleep(3)
    # กำหนดตัวเเปล run เป็น true
    Run = True
    # เรียกใช้ menu
    main_menu()

# ฟังชันหน้า Cadis
def Cadis():
    # นำเข้าตัวเเปลจากนอกฟังชั่น
    global Run
    # loopCadis
    while Run:
        Window.blit(cadis, (0, 0))
        MENU_MOUSE_POS = py.mouse.get_pos()
        Back_BUTTON = Button(image=py.image.load("assets/lucent.png"), pos=(70, 650),
                             text_input=" Back", font=get_font(40), base_color="white", hovering_color="Brown")

        for button in [Back_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(Window)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if Back_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press.play()
                    return


        py.display.update()

# ฟังชันหน้า how to play
def play():

    # นำเข้าตัวเเปลจากนอกฟังชั่น
    global Run
    # พื่นหลัง How_to_play
    Window.blit(How_to_play, (0, 0))
    # เรียกใช้บรรทัด 192 ก่อนเเล้วค่อนใช้ sleep
    py.display.flip()
    # หยุกเวลา 5 วิ
    t.sleep(5)
    # กำหนดตัวเเปล run เป็น False
    Run = False
    # เรียกใช้ฟังชั่น re_game
    re_game()

# ฟังชันหลัก หน้า manu
def main_menu():
    while Run:
        Window.blit(BG_manu, (0, 0))
        MENU_MOUSE_POS = py.mouse.get_pos()
        PLAY_BUTTON = Button(image=py.image.load("assets/lucent.png"), pos=(180, 260),
                             text_input="PLAY", font=get_font(120), base_color="#FFFFFF", hovering_color="Brown")
        QUIT_BUTTON = Button(image=py.image.load("assets/lucent.png"), pos=(180, 460),
                             text_input="QUIT", font=get_font(120), base_color="#FFFFFF", hovering_color="Brown")
        Cadis_BUTTON = Button(image=py.image.load("assets/lucent.png"), pos=(1110, 100),
                             text_input="Credit", font=get_font(70), base_color="#FFFFFF", hovering_color="Brown")

        for button in [PLAY_BUTTON, QUIT_BUTTON,Cadis_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(Window)

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()
            if event.type == py.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press.play()
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    py.quit()
                    sys.exit()
                if Cadis_BUTTON.checkForInput(MENU_MOUSE_POS):
                    press.play()
                    Cadis()

        py.display.update()

#เรื่มใช้ฟังชันเมื่อโค้ต run
game_start()

############################################################## นาย

while True:
    for event in py.event.get():  
        #การควบคุมจากคีบอด
        if event.type == py.KEYDOWN:
            if event.key == py.K_UP or event.key == ord('w'):
                direction = 'UP'
            if event.key == py.K_DOWN or event.key == ord('s'):
                direction = 'DOWN'
            if event.key == py.K_LEFT or event.key == ord('a'):
                direction = 'LEFT'
            if event.key == py.K_RIGHT or event.key == ord('d'):
                direction = 'RIGHT'
            if event.key == py.K_ESCAPE:
                Run = True
                main_menu()

    #ไม่ให้การบังคับส่วนทาง
    if direction == 'UP' and start != 'DOWN':
        start = 'UP'
    if direction == 'DOWN' and start != 'UP':
        start = 'DOWN'
    if direction == 'LEFT' and start != 'RIGHT':
        start = 'LEFT'
    if direction == 'RIGHT' and start != 'LEFT':
        start = 'RIGHT'

    if start == 'UP':
        snake_pos[1] -= 10
    if start == 'DOWN':
        snake_pos[1] += 10
    if start == 'LEFT':
        snake_pos[0] -= 10
    if start == 'RIGHT':
        snake_pos[0] += 10
    snake_body.insert(0, list(snake_pos))

    #การ boot
    Key = py.key.get_pressed()

    if Boot is False and Key[py.K_SPACE]:
        bootsound.play()
        Boot = True
    if Boot is True and not Key[py.K_SPACE]:
        Boot = False
    
    if Boot is True:
        difficulty = 80
    if Boot is False:
        difficulty = 60

############################################################### โอ้ต

    #การเพื่มคะเเนน
    if snake_pos[0] == food[0] and snake_pos[1] == food[1]:
        sound.play()
        score += 1
        food_spawn = False
    else:
        snake_body.pop()
    if not food_spawn:
        food = [rd.randrange(1, 128) * 10, rd.randrange(1, 72) * 10]
    food_spawn = True

    #การเเสดงผลในเกม
    Window.blit(BG_game,(0,0))

    for pos in snake_body:
        py.draw.rect(Window, green, py.Rect(pos[0], pos[1], 12, 12))
    py.draw.rect(Window, red, py.Rect(food[0], food[1], 10, 10))

#################################################################### ฝ้าย


    #gmae over
    if snake_pos[0] < 0 or snake_pos[0] > frame_x - 10:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] > frame_y - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()


################################################################ นาย

    #หน้าต่าง score
    show_score(1, white, 'consolas', 30)
    py.display.update()
    fps_controller.tick(difficulty)

##############################################################