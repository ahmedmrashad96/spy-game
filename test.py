import random
from _thread import *
import commu


class Game:
    __port = 40674
    __active_players = []
    rooms = []
    rooms_id = []

    def __init__(self):
        self.server = commu.Server('0.0.0.0', self.__port, 100, self.__handler)

    def __handler(self, connection):
        player = Player(connection)
        self.__active_players.append(player)


class Room(Game):
    full = False

    def __init__(self, host, max_clients=10, min_clients=2):
        self.secret = None
        self.players = [host]
        self.room_id = random.choice(list(set(range(1000, 9999)) - set(self.rooms_id)))
        self.rooms_id.append(self.room_id)
        self.host = host
        self.max_clients = max_clients
        self.min_clients = min_clients

    def start(self):
        i = random.randint(0, len(self.players)-1)
        self.secret = ' ' + str(random.randint(1, 1000))
        for z in range(len(self.players)):
            if z == i:
                self.players[z].secret = ' 0'
            else:
                self.players[z].secret = self.secret
            self.players[z].state = self.players[z].player_states[2]
        self.rooms.remove(self)
        self.rooms_id.remove(self.room_id)

    def join(self, player):
        self.players.append(player)
        if len(self.players) >= self.max_clients:
            self.full = True

    def leave(self, player):
        if player == self.host:
            self.close()
        elif player in self.players:
            self.players.remove(player)

    def close(self):
        for player in self.players:
            player.state = player.player_states[2]
        self.rooms.remove(self)
        self.rooms_id.remove(self.room_id)



class Player(Game):
    player_states = ('Connected', 'In_room', 'Room_closed')
    player_commands = ('join', 'leave', 'start')
    player_responses = ('ack', 'wrong_command')
    state = player_states[0]
    alive = True
    room = None
    host = False
    secret = None

    def __init__(self, connection):
        self.channel = commu.Channel(connection, self.__handler)
        start_new_thread(self.__loop, ())

    def __handler(self, message):
        response = message.split()
        print(response)
        match response[0]:
            case 'join':
                if len(response) == 2:
                    self.__join_room(int(response[1]))
                else:
                    self.__create_room()
            case 'leave':
                self.__leave_room()
            case 'start':
                self.__start_room()
            case _:
                self.channel.send('wrong_command')

    def __loop(self):
        n = 0
        self.channel.send('state: ' + self.state + ' ' + str(n))
        while self.room is None:
            pass
        while self.alive:
            old_state = self.state
            n = len(self.room.players)
            if old_state == self.player_states[2]:
                if self.secret is None:
                    self.channel.send('state: ' + old_state + ' ' + str(n))
                else:
                    self.channel.send('state: ' + old_state + ' ' + str(n) + self.secret)
                self.die()
                break
            else:
                if n >= self.room.min_clients:
                    self.channel.send('state: ' + old_state + '_ready ' + str(n))
                else:
                    self.channel.send('state: ' + old_state + ' ' + str(n))
            while old_state == self.state and n == len(self.room.players):
                pass

    def __join_room(self, room_id):
        if self.room is None:
            for room in self.rooms:
                if room.room_id == room_id:
                    if not room.full:
                        self.room = room
                        self.room.join(self)
                        self.state = self.player_states[1]
                        return
        self.channel.send('wrong_room')

    def __leave_room(self):
        if self.room is not None:
            self.room.leave(self)

    def __create_room(self):
        if self.room is None:
            self.room = Room(self)
            self.rooms.append(self.room)
            self.host = True
            self.state = self.player_states[1]
            self.channel.send(str(self.room.room_id))
        else:
            self.channel.send(self.player_responses[1])

    def __start_room(self):
        if self.host:
            self.room.start()

    def die(self):
        self.channel.close()
        self.channel = None
        self.alive = False


g = Game()
