import pygame
import sys
from pygame.locals import *
from time import sleep
from commu import Client
from pygame import mixer


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Game:
    DB = ('  School', 'Night club', 'Warehouse', '    Nazis\n headquarter',
          '   Mekkah ', ' F.O.E.', 'Kom Shkayer\n  el 3\'adarin')
    state = ''
    clients = 0
    id = ''
    secret = None

    def __init__(self):
        pass

    def handler(self, message):
        response = message.split()
        if response[0].isnumeric() and len(response[0]) == 4:
            self.id = response[0]
        elif response[0] == 'state:':
            self.state = response[1]
        if len(response) == 4:
            if int(response[3]) != 0:
                self.secret = self.DB[int(response[2])%len(self.DB)]
            else:
                self.secret = 'SPY'


g = Game()
mixer.init()
mixer.music.load("ThePinkPantherThemeSongOriginalVersion-arabix.mp3")
mixer.music.set_volume(0.5)
mixer.music.play()

FPS = 60
FramePerSec = pygame.time.Clock()
# Setting up color objects
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (99, 98, 102)
# res = (360, 480)

pygame.init()
background = pygame.image.load("BG.jpg")
res = (background.get_width(), background.get_height())
pygame.display.set_caption("Spy Game")
screen = pygame.display.set_mode(res)

title_font = pygame.font.SysFont('Agency FB', 48)
choice_font = pygame.font.SysFont('Agency FB', 48, True)
title = title_font.render('Who\'s the SPY', True, WHITE)
create_room = choice_font.render('Create Room', True, BLACK)
join_room = choice_font.render('Join Room', True, BLACK)
quit_game = choice_font.render('Quit Game', True, BLACK)
start_game = choice_font.render('Start Game', True, BLACK)
quit_room = choice_font.render('Quit Room', True, BLACK)
room_text = choice_font.render('Room ID', True, WHITE)
enter_room = choice_font.render('Enter Room', True, BLACK)
new_game = choice_font.render('New Game', True, BLACK)


page = 0

while True:
    ready = g.state.split('_')[-1] == 'ready'
    mouse = pygame.mouse.get_pos()
    hovered1 = (res[0] - 230 <= mouse[0] <= res[0]) and (150 <= mouse[1] <= 210)
    hovered2 = (res[0] - 230 <= mouse[0] <= res[0]) and (230 <= mouse[1] <= 290)
    hovered3 = (res[0] - 230 <= mouse[0] <= res[0]) and (310 <= mouse[1] <= 370)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # if client is not None:
            if client is not None:
                client.send('leave')
                while client.is_alive():
                    pass
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if page == 0:  # first menu
                if hovered1:
                    client = Client('127.0.0.1', 40674, g.handler)
                    client.send('join')
                    room_id_list = g.id
                    page = 1
                elif hovered2:
                    page = 2
                elif hovered3:
                    pygame.quit()
                    sys.exit()
            elif page == 1:  # host room
                if hovered1 and ready:
                    client.send('start')
                    page = 3
                elif hovered2:
                    page = 0
                    client.send('leave')
                elif hovered3:
                    client.send('leave')
                    pygame.quit()
                    sys.exit()
            elif page == 2: # before join
                if hovered1 and room_id:
                    client = Client('127.0.0.1', 40674, g.handler)
                    client.send('join ' + room_id_list)
                    page = 4
                elif hovered2:
                    page = 0
                elif hovered3:
                    pygame.quit()
                    sys.exit()
            elif page == 3:  # started game
                if hovered2:
                    page = 0
                if hovered3:
                    pygame.quit()
                    sys.exit()
            elif page == 4:  # joined
                if hovered2:
                    page = 0
                elif hovered3:
                    pygame.quit()
                    sys.exit()

    screen.blit(background, background.get_rect())
    screen.blit(title, (res[0] - title.get_width() - 50, 40))

    if page == 0:
        room_id_list = ''
        room_id = False
        g.secret = None

        if hovered1:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210

        if hovered2:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290

        if hovered3:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370

        screen.blit(create_room, (res[0] - create_room.get_width() - 10, 150))
        screen.blit(join_room, (res[0] - join_room.get_width() - 10, 230))
        screen.blit(quit_game, (res[0] - quit_game.get_width() - 10, 310))

    elif page == 1:

        if hovered1 and ready:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210

        if hovered2:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290

        if hovered3:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370

        screen.blit(start_game, (res[0] - start_game.get_width() - 10, 150))
        screen.blit(quit_room, (res[0] - quit_room.get_width() - 10, 230))
        screen.blit(quit_game, (res[0] - quit_game.get_width() - 10, 310))
        room_id_text = choice_font.render('Room id: ' + g.id, True, WHITE)
        screen.blit(room_id_text, (res[0] - enter_room.get_width() - 300, 150))
    elif page == 2:
        pygame.draw.rect(screen, WHITE, (res[0] - 380, 150, 150, 60))
        if hovered1 and room_id:
            pygame.draw.rect(screen, WHITE, (res[0] - 230, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 150, 430, 60))  # res[0]-230 -> res[0]  , 150 -> 210

        if hovered2:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290

        if hovered3:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370

        screen.blit(room_text, (res[0] - enter_room.get_width() - 240 - 100, 150))
        screen.blit(enter_room, (res[0] - enter_room.get_width() - 10, 150))
        screen.blit(quit_room, (res[0] - quit_room.get_width() - 10, 230))
        screen.blit(quit_game, (res[0] - quit_game.get_width() - 10, 310))

        pressed_keys = pygame.key.get_pressed()
        if len(room_id_list) < 4:
            room_id = False
            if pressed_keys[K_0] or pressed_keys[K_KP0]:
                room_id_list += '0'
                sleep(0.2)
            elif pressed_keys[K_1] or pressed_keys[K_KP1]:
                room_id_list += '1'
                sleep(0.2)
            elif pressed_keys[K_2] or pressed_keys[K_KP2]:
                room_id_list += '2'
                sleep(0.2)
            elif pressed_keys[K_3] or pressed_keys[K_KP3]:
                room_id_list += '3'
                sleep(0.2)
            elif pressed_keys[K_4] or pressed_keys[K_KP4]:
                room_id_list += '4'
                sleep(0.2)
            elif pressed_keys[K_5] or pressed_keys[K_KP5]:
                room_id_list += '5'
                sleep(0.2)
            elif pressed_keys[K_6] or pressed_keys[K_KP6]:
                room_id_list += '6'
                sleep(0.2)
            elif pressed_keys[K_7] or pressed_keys[K_KP7]:
                room_id_list += '7'
                sleep(0.2)
            elif pressed_keys[K_8] or pressed_keys[K_KP8]:
                room_id_list += '8'
                sleep(0.2)
            elif pressed_keys[K_9] or pressed_keys[K_KP9]:
                room_id_list += '9'
                sleep(0.2)
        else:
            room_id = True
        if pressed_keys[K_BACKSPACE]:
            room_id_list = room_id_list[:-1]
            sleep(0.2)
        elif (pressed_keys[K_KP_ENTER] or pressed_keys[K_RETURN]) and room_id:
            client = Client('127.0.0.1', 40674, g.handler)
            client.send('join ' + room_id_list)
            page = 4
        room_id_text = choice_font.render(room_id_list, True, BLACK)
        screen.blit(room_id_text, (res[0] - enter_room.get_width() - 150, 150))
    elif page == 3:

        if hovered2:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290

        if hovered3:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370

        screen.blit(new_game, (res[0] - new_game.get_width() - 10, 230))
        screen.blit(quit_game, (res[0] - quit_game.get_width() - 10, 310))
        if g.secret is not None:
            room_id_text = choice_font.render(g.secret, True, WHITE)
            screen.blit(room_id_text, (res[0] - enter_room.get_width() - 150, 150))
    elif page == 4:

        if hovered2:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 230, 430, 60))  # res[0]-230 -> res[0]  , 230 -> 290

        if hovered3:
            pygame.draw.rect(screen, WHITE, (res[0] - 430, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370
        else:
            pygame.draw.rect(screen, GREY, (res[0] - 230, 310, 430, 60))  # res[0]-230 -> res[0]  , 310 -> 370

        screen.blit(quit_room, (res[0] - quit_room.get_width() - 10, 230))
        screen.blit(quit_game, (res[0] - quit_game.get_width() - 10, 310))
        if g.secret is not None:
            page = 3
        if g.state == 'Room_closed' and g.secret is None:
            page = 0
    pygame.display.update()
    FramePerSec.tick(FPS)
