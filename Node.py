
import sys

from PyQt5.QtNetwork import QAbstractSocket
from PyQt5.QtNetwork import QUdpSocket
from PyQt5.QtNetwork import QHostAddress
from PyQt5.QtNetwork import QNetworkDatagram

from PyQt5.QtCore import QTimer

import Proto.snakes_pb2 as protocol

from State.Models.Proto.GameAnnouncement import GameAnnouncement
from State.Models.Proto.GameState import GameState
from State.Models.Proto.NodeRole import NodeRole
from State.Models.Proto.PlayerType import PlayerType
from State.Models.Proto.Direction import Direction

from State.Models.GamesInfoListItem import GamesInfoListItem

from Config import MCAST_GRP
from Config import MCAST_PORT
from Config import MCAST_TTL

from Logger import log

from App import app


class Node:
    def __init__(self):
        
        # on windows: you should use INADDR_ANY, system will filter datagrams
        # on linux: you should listen ONLY to MCAST_GRP
        self.__mcast_host = '' if sys.platform == 'win32' else MCAST_GRP
        self.__mcast_port = MCAST_PORT
        self.__mcast_grp = MCAST_GRP
        self.__mcast_ttl = MCAST_TTL
        self.__mcast_socket = None

        self.__main_host = ''
        self.__main_port = 0
        self.__main_socket = None

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = False
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False
        
        self.__is_active = False

    def start(self):
        
        if self.__is_active:
            self.stop()
        
        log.info('Node: Starting...')

        self.__mcast_socket = QUdpSocket()
        self.__mcast_socket.bind(QHostAddress(self.__mcast_host), self.__mcast_port, QUdpSocket.ShareAddress | QUdpSocket.ReuseAddressHint)
        self.__mcast_socket.joinMulticastGroup(QHostAddress(self.__mcast_grp))
        self.__mcast_socket.readyRead.connect(self.__on_mcast_socket_ready_read)

        log.debug('Node.start: Multicast socket is ready')

        self.__main_socket = QUdpSocket()
        self.__main_socket.setSocketOption(QUdpSocket.MulticastTtlOption, self.__mcast_ttl)
        self.__main_socket.bind(QHostAddress(self.__main_host), self.__main_port)
        self.__main_socket.readyRead.connect(self.__on_main_socket_ready_read)

        log.debug('Node.start: Main socket is ready')

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = False
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False

        self.__is_active = True

        log.info('Node: Started!')

    def stop(self):
        
        if not self.__is_active:
            log.debug('Node.stop: Node is not active')
            return
        
        log.info('Node: Stopping...')

        self.__is_active = False

        for timer in self.__game_timers:
            timer.stop()

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = False
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False
        
        if self.__main_socket is not None:
            self.__main_socket.close()
        self.__main_socket = None

        log.debug('Node.stop: Main socket closed')

        if self.__mcast_socket is not None:
            self.__mcast_socket.close()
        self.__mcast_socket = None

        log.debug('Node.stop: Multicast socket closed')

        log.info('Node: Stopped!')

    def start_game(self):
        
        if app.state.game is None:
            log.debug('Node.start_game: Impossible to start Game: Game is none')
            return False

        if self.__game_is_started:
            log.debug('Node.start_game: Impossible to start Game: Game is started')
            return False

        state_delay_ms = app.state.game.config.state_delay_ms
        
        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = True
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = True
        
        timer_1 = QTimer()
        timer_1.timeout.connect(self.__send_announcement_msg)
        timer_1.start(1000)

        timer_2 = QTimer()
        timer_2.timeout.connect(self.__next_state)
        timer_2.start(state_delay_ms)

        timer_3 = QTimer()
        timer_3.timeout.connect(self.__send_ping_msg)
        timer_3.start(state_delay_ms // 10)

        self.__game_timers.append(timer_1)
        self.__game_timers.append(timer_2)
        self.__game_timers.append(timer_3)

        log.info('Node: Start Game')

    def join_game(self, master_ip: str, master_port: int, game_name: str, role: NodeRole):

        if app.state.game is not None:
            log.debug('Node.join_game: Impossible to join Game: Game is not none')
            return False

        if self.__game_is_started:
            log.debug('Node.join_game: Impossible to join Game: Game is started')
            return False

        if self.__game_join_request_accepted:
            log.debug('Node.join_game: Impossible to join Game: Join Request Accpeted')
            return False

        if self.__game_requested_for_join:
            log.debug('Node.join_game: Impossible to join Game: Joining Requested')
            return False

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = True
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False
        
        success = self.__send_join_msg(master_ip, master_port, game_name, role)
        if not success:
            log.debug('Node.join_game: Joining requested unsuccessfully')

            for timer in self.__game_timers:
                timer.stop()

            self.__game_msg_seq = 0
            self.__game_unack_messages = {}
            self.__game_neighbours = {}
            self.__game_timers = []
            self.__game_is_ready = False
            self.__game_requested_for_join = False
            self.__game_join_request_accepted = False
            self.__game_is_started = False
            
            return False

        self.__game_requested_for_join = True

        app.gui.screen_manager.gotoScreen('connecting')
        
        log.info('Node: Send Join Request')
        return True

    def setup_game(self, id: int, type: PlayerType, name: str, game_name: str, role: NodeRole):

        if app.state.game is not None:
            log.debug('Node.setup_game: Impossible to setup Game: Game is not none')
            return False

        if self.__game_is_started:
            log.debug('Node.setup_game: Impossible to setup Game: Game is started')
            return False

        if not self.__game_requested_for_join:
            log.debug('Node.setup_game: Impossible to setup Game without join request')
            return False

        if not self.__game_join_request_accepted:
            log.debug('Node.setup_game: Impossible to setup Game without accepted join request')
            return False

        if not self.__game_is_ready:
            log.debug('Node.setup_game: Impossible to setup Game: Game is not ready')
            return False
        
        app.state.setup_game(game_name, id, type, name, role)

        self.__game_is_started = True

        timer_1 = QTimer()
        timer_1.timeout.connect(self.__send_ping_msg)
        timer_1.start(app.state.game.config.state_delay_ms // 10)

        self.__game_timers.append(timer_1)

        log.info('Node: Setup Game')
        return True

    def leave_game(self):
        if app.state.game is None:
            return
        if app.state.game.me.is_viewer():
            return self.quit_game()
        return self.quit_game()

    def quit_game(self):
        for timer in self.__game_timers:
            timer.stop()

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = False
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False

        app.state.quit_game()
        app.gui.screen_manager.gotoScreen('menu')
        return True

    def steer(self, direction: Direction):
        return self.__send_steer_msg(direction)

    def __on_mcast_socket_ready_read(self):
        while self.__mcast_socket.hasPendingDatagrams():
            datagram = self.__mcast_socket.receiveDatagram()
            ip = datagram.senderAddress().toString()
            port = int(datagram.senderPort())
            data = bytes(datagram.data())
            self.__process_mcast_socket_data(ip, port, data)

    def __on_main_socket_ready_read(self):
        while self.__main_socket.hasPendingDatagrams():
            datagram = self.__main_socket.receiveDatagram()
            ip = datagram.senderAddress().toString()
            port = int(datagram.senderPort())
            data = bytes(datagram.data())
            self.__process_main_socket_data(ip, port, data)

    def __process_mcast_socket_data(self, ip: str, port: int, data: bytes):
        msg = protocol.GameMessage()
        msg.ParseFromString(data)
        
        if msg.HasField('discover'):
            return self.__process_discover_msg(ip, port, msg)
        if msg.HasField('announcement'):
            return self.__process_announcement_msg(ip, port, msg)
        return

    def __process_main_socket_data(self, ip: str, port: int, data: bytes):
        msg = protocol.GameMessage()
        msg.ParseFromString(data)

        print(list(self.__game_unack_messages.keys()))
        print(list(self.__game_neighbours.keys()))

        address = (ip, port)

        print('PROCESS MAIN SOCKET', address)

        if address in self.__game_neighbours:
            nb = self.__game_neighbours.get((ip, port))
            nb_life_timer = nb['life_timer']
            interval = nb_life_timer.interval()
            nb_life_timer.start(interval)
            print('INTERVAL', interval)

        if msg.HasField('join'):
            return self.__process_join_msg(ip, port, msg)
        if msg.HasField('error'):
            return self.__process_error_msg(ip, port, msg)
        if msg.HasField('ack'):
            return self.__process_ack_msg(ip, port, msg)
        if msg.HasField('state'):
            return self.__process_state_msg(ip, port, msg)
        if msg.HasField('steer'):
            return self.__process_steer_msg(ip, port, msg)
        if msg.HasField('ping'):
            return self.__process_ping_msg(ip, port, msg)
        if msg.HasField('role_change'):
            return self.__process_role_change_msg(ip, port, msg)
        return
        
    def __process_discover_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive DiscoverMsg, Seq: {msg.msg_seq}')

        if app.state.game is None:
            log.debug('Node.__process_discover_msg: Game is none -> Skipped!')
            return

        if not self.__game_is_started:
            log.debug('Node.__process_discover_msg: Game is not started -> Skipped!')
            return

        if app.state.game.state is None:
            log.debug('Node.__process_discover_msg: Game State is none -> Skipped!')
            return

        if not app.state.game.me.is_master():
            log.debug('Node.__process_discover_msg: This node is not MASTER -> Skipped!')
            return
        
        return self.__send_announcement_msg()

    def __process_announcement_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive AnnouncementMsg, Seq: {msg.msg_seq}')

        if self.__game_is_started:
            log.debug('Node.__process_announcement_msg: Game is started -> Skipped!')
            return
        
        announcement = GameAnnouncement.from_protobuf(msg.announcement)
        
        game_info = GamesInfoListItem(
            game_name=announcement.game_name,
            master_name=announcement.players.master.name,
            master_ip=ip,
            master_port=port,
            field_width=announcement.config.width,
            field_height=announcement.config.height,
            food_static=announcement.config.food_static,
            alive_snakes_count=announcement.players.alive_count,
            can_join=announcement.can_join,
            state_delay_ms=announcement.config.state_delay_ms
        )
        
        app.state.games_info_list[announcement.game_name] = game_info
        
        app.gui.screen_manager.updateScreen('menu')
        return

    def __process_ping_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive PingMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__process_ping_msg: Unexpected Sender -> Skipped!')
            return

        if app.state.game is None:
            log.debug('Node.__process_ping_msg: Game is none -> Skipped!')
            return
        
        if not self.__game_is_started:
            log.debug('Node.__process_ping_msg: Game is not started -> Skipped!')
            return
        
        return self.__send_ack_msg(ip, port, msg.msg_seq)

    def __process_join_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive JoinMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address in self.__game_neighbours:
            log.debug('Node.__process_join_msg: Sender is joined -> Skipped!')
            return

        if app.state.game is None:
            log.debug('Node.__process_join_msg: Game is none -> Skipped!')
            return

        if not self.__game_is_started:
            log.debug('Node.__process_join_msg: Game is not started -> Skipped!')
            return

        if app.state.game.state is None:
            log.debug('Node.__process_join_msg: Game State is none -> Skipped!')
            return

        if not app.state.game.me.is_master():
            log.debug('Node.__process_join_msg: This node is not MASTER -> Skipped!')
            return
        
        player_type = PlayerType.from_protobuf(msg.join.player_type)
        player_name = msg.join.player_name
        game_name = msg.join.game_name
        requested_role = NodeRole.from_protobuf(msg.join.requested_role)
        
        player_id = app.state.join_game(game_name, ip, port, player_type, player_name, requested_role)
        
        if player_id is None:
            log.debug('Node.__process_join_msg: Player ID is none')
            return self.__send_error_msg(ip, port, msg.msg_seq, 'Impossible to join the game')
        
        log.debug(f'Node.__process_join_msg: Player ID = {player_id}')

        life_timer = QTimer()
        life_timer.setSingleShot(True)
        life_timer.timeout.connect(lambda: self.__drop_node(life_timer, ip, port))
        life_timer.start(app.state.game.config.state_delay_ms * 8 // 10)

        self.__game_timers.append(life_timer)

        address = (ip, port)
        
        self.__game_neighbours[address] = {}
        self.__game_neighbours[address]['role'] = app.state.game.state.players[player_id].role
        self.__game_neighbours[address]['msg_seq'] = msg.msg_seq
        self.__game_neighbours[address]['life_timer'] = life_timer
        
        status = self.__send_ack_msg(ip, port, msg.msg_seq)
        
        if app.state.game.state.players.alive_count == 2:
            if app.state.game.state.players.deputy is None:
                app.state.game.state.players[player_id].role = NodeRole.DEPUTY
                self.__game_neighbours[address]['role'] = NodeRole.DEPUTY
                status = status and self.__send_role_change_msg(ip, port, NodeRole.DEPUTY)
            
        status = status and self.__send_state_msg()
        return status

    def __process_error_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive ErrorMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__process_error_msg: Unexpected Sender -> Skipped!')
            return

        sender = self.__game_neighbours[address]
        if sender['role'] != NodeRole.MASTER:
            log.debug('Node.__process_error_msg: Sender is not MASTER -> Skipped!')
            return

        if app.state.game is not None:
            log.debug('Node.__process_error_msg: Game is not none -> Skipped!')
            return

        if self.__game_is_started:
            log.debug('Node.__process_error_msg: Game is started -> Skipped!')
            return

        if not self.__game_requested_for_join:
            log.debug('Node.__process_error_msg: Join Request does not exists -> Skipped!')
            return

        for timer in self.__game_timers:
            timer.stop()

        self.__game_msg_seq = 0
        self.__game_unack_messages = {}
        self.__game_neighbours = {}
        self.__game_timers = []
        self.__game_is_ready = False
        self.__game_requested_for_join = False
        self.__game_join_request_accepted = False
        self.__game_is_started = False
        
        app.gui.screen_manager.gotoScreen('menu')
        return

    def __process_ack_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive AckMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__process_ack_msg: Unexpected Sender -> Skipped!')
            return

        if not self.__game_is_ready:
            log.debug('Node.__process_ack_msg: Game is not ready -> Skipped!')
            return
        
        if msg.msg_seq not in self.__game_unack_messages:
            log.debug('Node.__process_ack_msg: Unexpected acknowledge message -> Skipped!')
            return
        
        message_info = self.__game_unack_messages.pop(msg.msg_seq)
        ack_src = message_info['src']
        ack_timer = message_info['timer']

        ack_timer.stop()
        
        if ack_timer in self.__game_timers:
            self.__game_timers.remove(ack_timer)
        
        if ack_src.HasField('join'):
            
            if not self.__game_requested_for_join:
                log.debug('Node.__process_ack_msg: Unexpected acknowledge for Join Request')
                return False
            
            player_id = msg.receiver_id
            
            player_type = PlayerType.from_protobuf(ack_src.join.player_type)
            player_name = ack_src.join.player_name
            game_name = ack_src.join.game_name
            role = NodeRole.from_protobuf(ack_src.join.requested_role)
            
            log.debug(f'Node.__process_ack_msg: Join Player ID: {player_id}')

            self.__game_join_request_accepted = True
            
            self.setup_game(player_id, player_type, player_name, game_name, role)

            if (ip, port) in self.__game_neighbours:
                nb = self.__game_neighbours.get((ip, port))
                nb_life_timer = nb['life_timer']
                nb_life_timer.start(app.state.game.config.state_delay_ms // 10 * 8)
                
            return
        return

    def __process_state_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive StateMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__process_state_msg: Unexpected Sender -> Skipped!')
            return

        sender = self.__game_neighbours[address]
        if sender['role'] != NodeRole.MASTER:
            log.debug('Node.__process_state_msg: Sender is not MASTER -> Skipped!')
            return

        if app.state.game is None:
            log.debug('Node.__process_state_msg: Game is none -> Skipped!')
            return

        if not self.__game_is_started:
            log.debug('Node.__process_state_msg: Game is not started -> Skipped!')
            return

        me = app.state.game.me

        if me is None:
            log.debug('Node.__process_state_msg: This node is none -> Skipped!')
            return self.quit_game()

        if me.is_master():
            log.debug('Node.__process_state_msg: This node is MASTER -> Skipped!')
            return
        
        is_first_state_message = app.state.game.state is None

        app.state.game.state = GameState.from_protobuf(msg.state.state)

        master = app.state.game.state.players.master
        master.ip_address = ip
        master.port = port

        for player in app.state.game.state.players.players:
            if player.ip_address is None or player.port is None:
                continue
            if player.id == me.id:
                continue
            address = (player.ip_address, player.port)

            if address in self.__game_neighbours:
                self.__game_neighbours[address]['role'] = player.role
                continue

            life_timer = QTimer()
            life_timer.setSingleShot(True)
            life_timer.timeout.connect(lambda: self.__drop_node(life_timer, player.ip_address, player.port))
            life_timer.start(app.state.game.config.state_delay_ms * 8 // 10)

            self.__game_timers.append(life_timer)
            
            self.__game_neighbours[address] = {}
            self.__game_neighbours[address]['role'] = player.role
            self.__game_neighbours[address]['msg_seq'] = 0
            self.__game_neighbours[address]['life_timer'] = life_timer
        
        if is_first_state_message:
            log.debug('Node.__process_state_msg: First Game State Inited!')
            app.gui.screen_manager.gotoScreen('game')
            return self.__send_ack_msg(ip, port, msg.msg_seq)

        if app.state.game.my_snake is None and not me.is_viewer():
            return self.leave_game()
        
        app.gui.screen_manager.updateScreen('game')

        return self.__send_ack_msg(ip, port, msg.msg_seq)

    def __process_steer_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive SteerMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__process_steer_msg: Unexpected Sender -> Skipped!')
            return

        sender = self.__game_neighbours[address]
        if sender['role'] == NodeRole.MASTER:
            log.debug('Node.__process_steer_msg: Sender is MASTER -> Skipped!')
            return

        if app.state.game is None:
            log.debug(f'Node.__process_steer_msg: Game is none -> Skipped!')
            return

        if not self.__game_is_started:
            log.debug(f'Node.__process_steer_msg: Game is not started -> Skipped!')
            return

        me = app.state.game.me

        if me is None:
            log.debug('Node.__process_steer_msg: This node is none -> Skipped!')
            return self.quit_game()

        if not me.is_master():
            log.debug('Node.__process_steer_msg: This node is not MASTER -> Skipped!')
            return

        if app.state.game.state is None:
            log.debug('Node.__process_steer_msg: Game State is none -> Skipped!')
            return
        
        player = app.state.game.state.players.get_player_by_address(ip, port)
        
        if player is None:
            log.debug('Node.__process_steer_msg: Player is none -> Skipped!')
            return

        snake = app.state.game.state.get_snake(player.id)
        
        if snake is None:
            log.debug('Node.__process_steer_msg: Snake is none -> Skipped!')
            return
        
        direction = Direction.from_protobuf(msg.steer.direction)

        log.debug(f'Node.__process_steer_msg: msg.steer.direction = {msg.steer.direction}')
        log.debug(f'Node.__process_steer_msg: previous snake head direction = {snake.head_direction}')
        log.debug(f'Node.__process_steer_msg: direction = {direction}')

        snake.head_direction = direction
        
        log.debug(f'Node.__process_steer_msg: current snake head direction = {snake.head_direction}')
        
        return self.__send_ack_msg(ip, port, msg.msg_seq)

    def __process_role_change_msg(self, ip: str, port: int, msg: protocol.GameMessage):
        log.debug(f'Node: Receive RoleChangeMsg, Seq: {msg.msg_seq}')

        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug(f'Node.__process_role_change_msg: Unexpected Sender -> Skipped!')
            return False

        if app.state.game is None:
            log.debug(f'Node.__process_role_change_msg: Game is none -> Skipped!')
            return False

        if app.state.game.state is None:
            log.debug(f'Node.__process_role_change_msg: Game State is None -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug(f'Node.__process_role_change_msg: Game is not started -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug(f'Node.__process_role_change_msg: This node is none -> Skipped!')
            return self.quit_game()

        if me.id != msg.receiver_id:
            log.debug(f'Node.__process_role_change_msg: This node ID does not match with receiver ID -> Skipped!')
            return False

        sender = app.state.game.state.players[msg.sender_id]

        if sender is None:
            log.debug(f'Node.__process_role_change_msg: Player {msg.sender_id} not found -> Skipped!')
            return False

        receiver = me

        if msg.role_change.HasField('sender_role'):
            sender_role = NodeRole.from_protobuf(msg.role_change.sender_role)
        else:
            sender_role = None

        if msg.role_change.HasField('receiver_role'):
            receiver_role = NodeRole.from_protobuf(msg.role_change.receiver_role)
        else:
            receiver_role = None

        if sender_role is not None:
            sender.role = sender_role
            self.__game_neighbours[address]['role'] = sender.role
        
        if receiver_role is not None:
            receiver.role = receiver_role
        
        return self.__send_ack_msg(ip, port, msg.msg_seq)

    def __send_announcement_msg(self):
        
        if app.state.game is None:
            log.debug('Node.__send_announcement_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_announcement_msg: Game is not started -> Skipped!')
            return False

        if app.state.game.state is None:
            log.debug('Node.__send_announcement_msg: Game State is none -> Skipped!')
            return False

        if not app.state.game.me.is_master():
            log.debug('Node.__send_announcement_msg: This node is not MASTER -> Skipped!')
            return False
        
        game = app.state.game
        
        game = GameAnnouncement(game.name, game.config, game.state.players, game.can_join)
        
        announcement_msg = protocol.GameMessage.AnnouncementMsg()
        announcement_msg.games.extend([game.to_protobuf()])
        
        msg = protocol.GameMessage()
        msg.announcement.CopyFrom(announcement_msg)
        
        self.__game_msg_seq = self.__game_msg_seq + 1
        msg.msg_seq = self.__game_msg_seq
        
        host = QHostAddress(self.__mcast_grp)
        port = self.__mcast_port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)
        
        self.__main_socket.writeDatagram(datagram)
        
        log.debug(f'Node: Send AnnouncementMsg, Seq: {msg.msg_seq}')
        return True

    def __send_ack_msg(self, ip: str, port: int, msg_seq: int):
        
        address = (ip, port)
        
        if address not in self.__game_neighbours:
            log.debug('Node.__send_ack_msg: Unexpected Receiver -> Skipped!')
            return False
        
        if app.state.game is None:
            log.debug('Node.__send_ack_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_ack_msg: Game is not started -> Skipped!')
            return False
        
        if app.state.game.state is None:
            log.debug('Node.__send_ack_msg: Game State is none -> Skipped!')
            return False

        receiver = app.state.game.state.players.get_player_by_address(ip, port)
        
        if receiver is None:
            log.debug('Node.__send_ack_msg: Receiver is not a player -> Skipped!')
            return False

        sender = app.state.game.me
        
        if sender is None:
            log.debug('Node.__send_ack_msg: This node is none -> Skipped!')
            return self.quit_game()
        
        ack_msg = protocol.GameMessage.AckMsg()
        msg = protocol.GameMessage()
        msg.ack.CopyFrom(ack_msg)
        
        msg.msg_seq = msg_seq
        msg.sender_id = sender.id
        msg.receiver_id = receiver.id
        
        host = QHostAddress(ip)
        port = port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

        self.__main_socket.writeDatagram(datagram)
        
        log.debug(f'Node: Send AckMsg, Seq: {msg.msg_seq}')
        return True

    def __send_ping_msg(self):
        
        if app.state.game is None:
            log.debug('Node.__send_ping_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_ping_msg: Game is not started -> Skipped!')
            return False
        
        if app.state.game.state is None:
            log.debug('Node.__send_ping_msg: Game State is none -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug('Node.__send_ping_msg: This node is none -> Skipped!')
            return self.quit_game()
        
        for player in app.state.game.state.players.players:
            if player.id == me.id:
                continue
            if player.ip_address is None or player.port is None:
                continue
            
            ping_msg = protocol.GameMessage.PingMsg()
            msg = protocol.GameMessage()
            msg.ping.CopyFrom(ping_msg)
            
            self.__game_msg_seq = self.__game_msg_seq + 1
            msg.msg_seq = self.__game_msg_seq
            
            host = QHostAddress(player.ip_address)
            port = player.port
            datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

            ack_timer = QTimer()
            ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, msg))
            ack_timer.start(app.state.game.config.state_delay_ms // 10)

            self.__game_timers.append(ack_timer)

            self.__game_unack_messages[msg.msg_seq] = {}
            self.__game_unack_messages[msg.msg_seq]['src'] = msg
            self.__game_unack_messages[msg.msg_seq]['timer'] = ack_timer
            self.__game_unack_messages[msg.msg_seq]['ip'] = player.ip_address
            self.__game_unack_messages[msg.msg_seq]['port'] = player.port
            self.__game_unack_messages[msg.msg_seq]['resends'] = 0
            
            self.__main_socket.writeDatagram(datagram)
            
            log.debug(f'Node: Send PingMsg, Seq: {msg.msg_seq}')
        return True

    def __send_join_msg(self, master_ip: str, master_port: int, game_name: str, role: NodeRole):

        if app.state.game is not None:
            log.debug('Node.__send_join_msg: Game is not none -> Skipped!')
            return False

        if self.__game_is_started:
            log.debug('Node.__send_join_msg: Game is started -> Skipped!')
            return False

        if not self.__game_is_ready:
            log.debug('Node.__send_join_msg: Game is not ready -> Skipped!')
            return False

        if self.__game_requested_for_join:
            log.debug('Node.__send_join_msg: Joining Requested -> Skipped!')
            return False
        
        if role != NodeRole.VIEWER and role != NodeRole.NORMAL:
            log.debug('Node.__send_join_msg: Unexpected requested role -> Skipped!')
            return False
        
        join_msg = protocol.GameMessage.JoinMsg()
        join_msg.player_type = PlayerType.HUMAN.to_protobuf()
        join_msg.player_name = app.state.user.name
        join_msg.game_name = game_name
        join_msg.requested_role = role.to_protobuf()

        msg = protocol.GameMessage()
        msg.join.CopyFrom(join_msg)
        
        self.__game_msg_seq = self.__game_msg_seq + 1
        msg.msg_seq = self.__game_msg_seq
        
        host = QHostAddress(master_ip)
        port = master_port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

        state_delay_ms = app.state.game_config.state_delay_ms

        ack_timer = QTimer()
        ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, msg))
        ack_timer.start(state_delay_ms // 10)

        self.__game_timers.append(ack_timer)

        self.__game_unack_messages[msg.msg_seq] = {}
        self.__game_unack_messages[msg.msg_seq]['src'] = msg
        self.__game_unack_messages[msg.msg_seq]['timer'] = ack_timer
        self.__game_unack_messages[msg.msg_seq]['ip'] = master_ip
        self.__game_unack_messages[msg.msg_seq]['port'] = master_port
        self.__game_unack_messages[msg.msg_seq]['resends'] = 0

        address = (master_ip, master_port)

        life_timer = QTimer()
        life_timer.setSingleShot(True)
        life_timer.timeout.connect(lambda: self.__drop_node(life_timer, master_ip, master_port))
        life_timer.start(state_delay_ms * 8 // 10)

        self.__game_timers.append(life_timer)

        self.__game_neighbours[address] = {}
        self.__game_neighbours[address]['role'] = NodeRole.MASTER
        self.__game_neighbours[address]['msg_seq'] = 0
        self.__game_neighbours[address]['life_timer'] = life_timer
        
        self.__main_socket.writeDatagram(datagram)
        
        log.debug(f'Node: Send JoinMsg, Seq: {msg.msg_seq}')
        return True

    def __send_error_msg(self, ip: str, port: int, msg_seq: int, message: str):

        if app.state.game is None:
            log.debug('Node.__send_error_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_error_msg: Game is not started -> Skipped!')
            return False

        if app.state.game.state is None:
            log.debug('Node.__send_error_msg: Game State is none -> Skipped!')
            return False

        if not app.state.game.me.is_master():
            log.debug('Node.__send_error_msg: This node is not MASTER -> Skipped!')
            return False
        
        error_msg = protocol.GameMessage.ErrorMsg()
        error_msg.error_message = message
        
        msg = protocol.GameMessage()
        msg.error.CopyFrom(error_msg)

        msg.msg_seq = msg_seq

        host = QHostAddress(ip)
        port = port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)
        
        self.__main_socket.writeDatagram(datagram)
        
        log.debug(f'Node: Send ErrorMsg, Seq: {msg.msg_seq}')
        return True

    def __send_state_msg(self):
        
        if app.state.game is None:
            log.debug('Node.__send_state_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_state_msg: Game is not started -> Skipped!')
            return False
        
        if app.state.game.state is None:
            log.debug('Node.__send_state_msg: Game State is none -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug('Node.__send_state_msg: This node is none -> Skipped!')
            return self.quit_game()

        if not me.is_master():
            log.debug('Node.__send_state_msg: This node is not MASTER -> Skipped!')
            return False
        
        for player in app.state.game.state.players.players:
            if player.id == me.id:
                continue
            if player.ip_address is None or player.port is None:
                continue
            
            state_msg = protocol.GameMessage.StateMsg()
            state_msg.state.CopyFrom(app.state.game.state.to_protobuf())
            
            msg = protocol.GameMessage()
            msg.state.CopyFrom(state_msg)

            self.__game_msg_seq = self.__game_msg_seq + 1
            msg.msg_seq = self.__game_msg_seq
            
            host = QHostAddress(player.ip_address)
            port = player.port
            datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

            ack_timer = QTimer()
            ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, msg))
            ack_timer.start(app.state.game.config.state_delay_ms // 10)

            self.__game_timers.append(ack_timer)

            self.__game_unack_messages[msg.msg_seq] = {}
            self.__game_unack_messages[msg.msg_seq]['src'] = msg
            self.__game_unack_messages[msg.msg_seq]['timer'] = ack_timer
            self.__game_unack_messages[msg.msg_seq]['ip'] = player.ip_address
            self.__game_unack_messages[msg.msg_seq]['port'] = player.port
            self.__game_unack_messages[msg.msg_seq]['resends'] = 0
            
            self.__main_socket.writeDatagram(datagram)
            log.debug(f'Node: Send StateMsg, Seq: {msg.msg_seq}')
        return True

    def __send_steer_msg(self, direction: Direction):
        
        if app.state.game is None:
            log.debug('Node.__send_steer_msg: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_steer_msg: Game is not started -> Skipped!')
            return False
        
        if app.state.game.state is None:
            log.debug('Node.__send_steer_msg: Game State is none -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug('Node.__send_steer_msg: This node is none -> Skipped!')
            return self.quit_game()

        if me.is_master():
            log.debug('Node.__send_steer_msg: This node is MASTER -> Skipped!')
            return False

        if me.is_viewer():
            log.debug('Node.__send_steer_msg: This node is VIEWER -> Skipped!')
            return False
        
        steer_msg = protocol.GameMessage.SteerMsg()
        steer_msg.direction = direction.to_protobuf()

        log.debug(f'Node.__send_steer_msg: direction = {direction}')
        log.debug(f'Node.__send_steer_msg: steer_msg.direction = {steer_msg.direction}')

        msg = protocol.GameMessage()
        msg.steer.CopyFrom(steer_msg)

        self.__game_msg_seq = self.__game_msg_seq + 1
        msg.msg_seq = self.__game_msg_seq

        master = app.state.game.state.players.master
        
        host = QHostAddress(master.ip_address)
        port = master.port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

        ack_timer = QTimer()
        ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, msg))
        ack_timer.start(app.state.game.config.state_delay_ms // 10)

        self.__game_timers.append(ack_timer)

        self.__game_unack_messages[msg.msg_seq] = {}
        self.__game_unack_messages[msg.msg_seq]['src'] = msg
        self.__game_unack_messages[msg.msg_seq]['timer'] = ack_timer
        self.__game_unack_messages[msg.msg_seq]['ip'] = master.ip_address
        self.__game_unack_messages[msg.msg_seq]['port'] = master.port
        self.__game_unack_messages[msg.msg_seq]['resends'] = 0
        
        self.__main_socket.writeDatagram(datagram)
        log.debug(f'Node: Send SteerMsg, Seq: {msg.msg_seq}')
        return True

    def __send_role_change_msg(self, ip: str, port: int, receiver_role: NodeRole | None = None):

        if app.state.game is None:
            log.debug('Node.__send_role_change_msg: Game is none -> Skipped!')
            return False

        if app.state.game.state is None:
            log.debug('Node.__send_role_change_msg: Game State is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__send_role_change_msg: Game is not started -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug('Node.__send_role_change_msg: This node is none -> Skipped!')
            return self.quit_game()

        receiver = app.state.game.state.players.get_player_by_address(ip, port)
        
        if receiver is None:
            log.debug('Node.__send_role_change_msg: Receiver is none -> Skipped!')
            return False
        
        role_change_msg = protocol.GameMessage.RoleChangeMsg()
        role_change_msg.sender_role = me.role.to_protobuf()
        if receiver_role is not None:
            role_change_msg.receiver_role = receiver_role.to_protobuf()

        log.debug(f'Node.__send_role_change_msg: sender_role = {me.role}')
        log.debug(f'Node.__send_role_change_msg: receiver_role = {receiver_role}')

        msg = protocol.GameMessage()
        msg.role_change.CopyFrom(role_change_msg)

        self.__game_msg_seq = self.__game_msg_seq + 1
        msg.msg_seq = self.__game_msg_seq

        msg.sender_id = me.id
        msg.receiver_id = receiver.id
        
        host = QHostAddress(ip)
        port = port
        datagram = QNetworkDatagram(msg.SerializeToString(), host, port)

        ack_timer = QTimer()
        ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, msg))
        ack_timer.start(app.state.game.config.state_delay_ms // 10)

        self.__game_timers.append(ack_timer)

        self.__game_unack_messages[msg.msg_seq] = {}
        self.__game_unack_messages[msg.msg_seq]['src'] = msg
        self.__game_unack_messages[msg.msg_seq]['timer'] = ack_timer
        self.__game_unack_messages[msg.msg_seq]['ip'] = ip
        self.__game_unack_messages[msg.msg_seq]['port'] = port
        self.__game_unack_messages[msg.msg_seq]['resends'] = 0
        
        self.__main_socket.writeDatagram(datagram)
        
        log.debug(f'Node: Send RoleChangeMsg, Seq: {msg.msg_seq}')
        return True

    def __resend_game_msg(self, timer: QTimer, host: QHostAddress, port: int, msg: protocol.GameMessage):
        if not timer.isActive():
            if timer is self.__game_timers:
                self.__game_timers.remove(timer)
            timer.stop()

        if not self.__game_is_ready:
            log.debug('Node.__resend_game_msg: Game is not ready -> Skipped!')
            return False

        ip = host.toString()
        port = port

        address = (ip, port)
        
        if address not in self.__game_neighbours:           
            if timer is self.__game_timers:
                self.__game_timers.remove(timer)
            timer.stop()

            log.debug('Node.__resend_game_msg: Unexpected neighbour -> Skipped!')
            return False
        
        if msg.msg_seq not in self.__game_unack_messages:
            if timer is self.__game_timers:
                self.__game_timers.remove(timer)
            timer.stop()
            
            log.debug('Node.__resend_game_msg: Unexpected Unacknowledged Message -> Skipped!')
            return False
        
        self.__main_socket.writeDatagram(QNetworkDatagram(msg.SerializeToString(), host, port))
        self.__game_unack_messages[msg.msg_seq]['resends'] += 1

        if self.__game_unack_messages[msg.msg_seq]['resends'] > 10:
            timer = self.__game_unack_messages[msg.msg_seq]['timer']
            if timer is self.__game_timers:
                self.__game_timers.remove(timer)
            timer.stop()
            
            self.__game_unack_messages.pop(msg.msg_seq)
            
            life_timer = self.__game_neighbours.get(address)['life_timer']
            self.__drop_node(life_timer, ip, port)
        
        log.debug(f'Node: Resend GameMessage, Seq: {msg.msg_seq}')
        return True
    
    def __next_state(self):
        
        if app.state.game is None:
            log.debug('Node.__next_state: Game is none -> Skipped!')
            return False

        if not self.__game_is_started:
            log.debug('Node.__next_state: Game is not started -> Skipped!')
            return False
        
        if app.state.game.state is None:
            log.debug('Node.__next_state: Game State is none -> Skipped!')
            return False

        if not app.state.game.me.is_master():
            log.debug('Node.__next_state: This node is not MASTER -> Skipped!')
            return False
        
        app.state.game.next()
        
        if app.state.game.my_snake is None:
            return self.leave_game()
        
        app.gui.screen_manager.updateScreen('game')
        
        return self.__send_state_msg()        

    def __drop_node(self, timer: QTimer, ip: str, port: int):

        if not self.__game_is_ready:
            log.debug('Node.__drop_node: Game is not ready -> Skipped!')
            return False

        if self.__game_requested_for_join and not self.__game_join_request_accepted:
            log.debug('Node.__drop_node: MASTER node is not available -> Skipped!')
            return self.quit_game()

        address = (ip, port)

        if address not in self.__game_neighbours:
            if timer in self.__game_timers:
                self.__game_timers.remove(timer)
            timer.stop()
            
            log.debug('Node.__drop_node: Neighbour not found -> Skipped!')
            return False

        me = app.state.game.me

        if me is None:
            log.debug('Node.__drop_node: This node is none -> Skipped!')
            return self.quit_game()
        neighbour = self.__game_neighbours.get(address)

        print(neighbour)
        
        nb_life_timer = neighbour['life_timer']
        nb_role = neighbour['role']

        if nb_life_timer in self.__game_timers:
            self.__game_timers.remove(nb_life_timer)
        nb_life_timer.stop()

        self.__game_neighbours.pop(address)

        if (me.is_normal() or me.is_viewer()) and nb_role == NodeRole.MASTER:
            log.debug(f'Node.__drop_node: ME: NORMAL = {me.is_normal()}, VIEWER = {me.is_viewer()}, NB: MASTER')

            if app.state.game.state is None:
                log.debug('Node.__drop_node: Game State is none -> Skipped!')
                return self.quit_game()

            deputy = app.state.game.state.players.deputy

            if deputy is None:
                log.debug('Node.__drop_node: DEPUTY is none -> Skipped!')
                return self.quit_game()

            if deputy.ip_address is None or deputy.port is None:
                log.debug('Node.__drop_node: DEPUTY address is none -> Skipped!')
                return False

            nb_deputy = self.__game_neighbours.get((deputy.ip_address, deputy.port))
            
            if nb_deputy is None:
                log.debug('Node.__drop_node: DEPUTY is not neighbour -> Skipped!')
                return False
            
            for msg_seq in list(self.__game_unack_messages.keys()):
                message = self.__game_unack_messages.get(msg_seq)

                ack_src = message['src']
                ack_timer = message['timer']
                ack_ip = message['ip']
                ack_port = message['port']

                if ack_ip != ip or ack_port != port:
                    continue

                if ack_timer in self.__game_timers:
                    self.__game_timers.remove(ack_timer)
                ack_timer.stop()

                host = QHostAddress(deputy.ip_address)
                port = deputy.port

                ack_timer = QTimer()
                ack_timer.timeout.connect(lambda: self.__resend_game_msg(ack_timer, host, port, ack_src))
                ack_timer.start(app.state.game.config.state_delay_ms // 10)

                self.__game_timers.append(ack_timer)

                ack_src.receiver_id = deputy.id

                self.__game_unack_messages[msg_seq] = {}
                self.__game_unack_messages[msg_seq]['src'] = ack_src
                self.__game_unack_messages[msg_seq]['timer'] = ack_timer
                self.__game_unack_messages[msg_seq]['ip'] = deputy.ip_address
                self.__game_unack_messages[msg_seq]['port'] = deputy.port
                self.__game_unack_messages[msg_seq]['resends'] = 0
            
            return True
        
        if me.is_master() and nb_role == NodeRole.DEPUTY:
            log.debug(f'Node.__drop_node: ME: MASTER, NB: DEPUTY')

            if app.state.game.state is None:
                log.debug('Node.__drop_node: Game State is none -> Skipped!')
                return False

            normal = app.state.game.state.players.get_normal(me.id)
            deputy = app.state.game.state.players.deputy
            
            if deputy is None:
                log.debug('Node.__drop_node: DEPUTY is none -> Skipped!')
                return False
            
            for msg_seq in list(self.__game_unack_messages.keys()):
                message = self.__game_unack_messages.get(msg_seq)

                ack_src = message['src']
                ack_timer = message['timer']
                ack_ip = message['ip']
                ack_port = message['port']

                if ack_ip != ip or ack_port != port:
                    continue

                if ack_timer in self.__game_timers:
                    self.__game_timers.remove(ack_timer)
                ack_timer.stop()

                self.__game_unack_messages.pop(msg_seq)

            app.state.game.state.players.remove(deputy.id)
            
            snake = app.state.game.state.get_snake(deputy.id)
            if snake is not None:
                snake.zombify()

            if normal is not None and normal.ip_address is not None and normal.port is not None:
                normal.role = NodeRole.DEPUTY
                self.__game_neighbours[(normal.ip_address, normal.port)]['role'] = NodeRole.DEPUTY
                return self.__send_role_change_msg(normal.ip_address, normal.port, NodeRole.DEPUTY)
            
            return True

        if me.is_deputy() and nb_role == NodeRole.MASTER:
            log.debug(f'Node.__drop_node: ME: DEPUTY, NB: MASTER')

            if app.state.game.state is None:
                log.debug('Node.__drop_node: Game State is none -> Skipped!')
                return False

            normal = app.state.game.state.players.get_normal(me.id)
            master = app.state.game.state.players.master
            
            if master is None:
                log.debug('Node.__drop_node: MASTER is none -> Skipped!')
                return False

            for msg_seq in list(self.__game_unack_messages.keys()):
                message = self.__game_unack_messages.get(msg_seq)

                ack_src = message['src']
                ack_timer = message['timer']
                ack_ip = message['ip']
                ack_port = message['port']

                if ack_ip != ip or ack_port != port:
                    continue

                if ack_timer in self.__game_timers:
                    self.__game_timers.remove(ack_timer)
                ack_timer.stop()

                self.__game_unack_messages.pop(msg_seq)

            print('PLAYERS:', app.state.game.state.players.players)
            app.state.game.state.players.remove(master.id)
            print('PLAYERS:', app.state.game.state.players.players)
            
            snake = app.state.game.state.get_snake(master.id)
            if snake is not None:
                snake.zombify()

            me.role = NodeRole.MASTER

            timer_1 = QTimer()
            timer_1.timeout.connect(self.__send_announcement_msg)
            timer_1.start(1000)

            timer_2 = QTimer()
            timer_2.timeout.connect(self.__next_state)
            timer_2.start(app.state.game.config.state_delay_ms)

            self.__game_timers.append(timer_1)
            self.__game_timers.append(timer_2)

            if normal is None:
                log.debug('Node.__drop_node: No any NORMAL node')
                return True

            if normal.ip_address is None or normal.port is None:
                log.debug('Node.__drop_node: NORMAL address is none')
                return True

            normal.role = NodeRole.DEPUTY

            self.__game_neighbours[(normal.ip_address, normal.port)]['role'] = NodeRole.DEPUTY
            status = self.__send_role_change_msg(normal.ip_address, normal.port, NodeRole.DEPUTY)
            
            for player in app.state.game.state.players.players:
                if player.ip_address is None or player.port is None:
                    continue
                if player.id == me.id:
                    continue
                if player.id == normal.id:
                    continue
                status = status and self.__send_role_change_msg(player.ip_address, player.port)
            return status

        log.debug(f'Node.__drop_node: OTHER')
        print(me.is_master(), me.is_viewer(), me.is_deputy(), me.is_normal(), nb_role)

        if app.state.game.state is None:
            log.debug('Node.__drop_node: Game State is none -> Skipped!')
            return False

        player = app.state.game.state.players.get_player_by_address(ip, port)

        if player is None:
            log.debug('Node.__drop_node: Player is none -> Skipped!')
            return False

        for msg_seq in list(self.__game_unack_messages.keys()):
            message = self.__game_unack_messages.get(msg_seq)

            ack_src = message['src']
            ack_timer = message['timer']
            ack_ip = message['ip']
            ack_port = message['port']

            if ack_ip != ip or ack_port != port:
                continue

            if ack_timer in self.__game_timers:
                self.__game_timers.remove(ack_timer)
            ack_timer.stop()

            self.__game_unack_messages.pop(msg_seq)

        app.state.game.state.players.remove(player.id)
        
        snake = app.state.game.state.get_snake(player.id)
        if snake is not None:
            snake.zombify()

        return True

        
        
