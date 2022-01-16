import socket
import json
import time
import threading
import random
import string

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Network:

    def __init__(self, server_addr: str, server_port: int, username: str):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = server_addr
        self.port = server_port
        self.username = username
        self.recv_size = 20480
        self.id = 0

    def settimeout(self, value):
        self.client.settimeout(value)

    def connect(self):
        self.client.connect((self.addr, self.port))
        self.id = self.client.recv(self.recv_size).decode("utf8")
        self.client.send(self.username.encode("utf8"))

    def receive_info(self):
        try:
            msg = self.client.recv(self.recv_size)
        except socket.error as e:
            print(e)
            print("receive_info报错")

        if not msg:
            return None

        msg_decoded = msg.decode("utf8")
        print(type(msg_decoded), len(msg_decoded))
        msg_jsons = []
        idx = msg_decoded.find("}{")
        while idx != -1: # 这里检测粘包现象
            left_bracket_index = 0
            # print("left_bracket_index", left_bracket_index)
            right_bracket_index = idx+1
            # print("right_bracket_index", right_bracket_index)
            msg_piece = msg_decoded[left_bracket_index:right_bracket_index]
            # print(msg_piece)
            msg_jsons.append(json.loads(msg_piece))
            msg_decoded = msg_decoded[right_bracket_index:]
            idx = msg_decoded.find("}{")
        left_bracket_index = 0
        right_bracket_index = len(msg_decoded)
        # print(msg_decoded)
        msg_jsons.append(json.loads(msg_decoded))
        return msg_jsons

    def send_player(self, player: FirstPersonController):
        player_info = {
            "object": "player",
            "id": self.id,
            "position": (player.world_x, player.world_y, player.world_z),
            "rotation": player.rotation_y,
            "joined": False, # jointed indicates new join, so it's False by default
            "left": False
        }
        player_info_encoded = json.dumps(player_info).encode("utf8")

        try:
            self.client.send(player_info_encoded)
        except socket.error as e:
            print(e)

    def send_voxel(self, id_=0, state="create", position=(0,0,0), texture="grass_block.png"):
        print(id_)
        voxel_info = {
            "object": "voxel",
            "id": int(id_),
            "state": state,
            "position": (int(position[0]), int(position[1]), int(position[2])),
            "texture": texture_idx.index(str(texture)),
            # "color": voxel.color
        }
        # print(voxel.color)
        # print(type(voxel.color))

        voxel_info_encoded = json.dumps(voxel_info).encode("utf8")

        try:
            self.client.send(voxel_info_encoded)
        except socket.error as e:
            print(e)


class Ally(Entity):
    def __init__(self, position: Vec3, identifier: str, username: str):
        super().__init__(
            position=position,
            model="cube",
            origin_y=-0.5,
            collider="box",
            texture="white_cube",
            color=color.color(0, 0, 1),
            scale=Vec3(1, 2, 1)
        )

        self.name_tag = Text(
            parent=self,
            text=username,
            position=Vec3(0, 1.3, 0),
            scale=Vec2(5, 3),
            billboard=True,
            origin=Vec2(0, 0)
        )

        self.id = identifier
        self.username = username


letters = string.ascii_lowercase + string.ascii_uppercase
username = letters = ''.join(random.choice(letters) for i in range(10))

server_addr = ""
server_port = ""
while True:
    server_addr = input("Enter server IP: ") if False else '192.168.1.217'
    server_port = input("Enter server port: ") if False else '8000'

    try:
        server_port = int(server_port)
    except ValueError:
        print("\nThe port you entered was not a number, try again with a valid port...")
        continue

    n = Network(server_addr, server_port, username)
    n.settimeout(5)

    error_occurred = False

    try:
        n.connect()
    except ConnectionRefusedError:
        print("\nConnection refused! This can be because server hasn't started or has reached it's player limit.")
        error_occurred = True
    except socket.timeout:
        print("\nServer took too long to respond, please try again...")
        error_occurred = True
    except socket.gaierror:
        print("\nThe IP address you entered is invalid, please try again with a valid address...")
        error_occurred = True
    finally:
        n.settimeout(None)

    if not error_occurred:
        break

app = Ursina()

texture_idx = [
    'grass_block.png',
    'stone_block.png',
    'brick_block.png',
    'dirt_block.png',
    'gold_block.png',
    'lava_block.png'
]
textures = []
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
gold_texture  = load_texture('assets/gold_block.png')
lava_texture  = load_texture('assets/lava_block.png')
textures.extend([grass_texture, stone_texture, brick_texture, dirt_texture, gold_texture, lava_texture])

sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound',loop = False, autoplay = False)
block_pick = 1
block_idx = 401

window.fps_counter.enabled = False
window.exit_button.visible = False
window.borderless = False

class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture, id_ = 0, state = "create", color = color.color(0,0,random.uniform(0.9,1))):
        super().__init__(
            parent = scene,
            position = position,
            model = 'assets/block',
            origin_y = 0.5,
            texture = texture,
            color = color,
            scale = 0.5)
        self.id = id_
        self.state = state

    def input(self,key):
        if self.hovered:
            if key == 'left mouse down':
                global block_idx
                punch_sound.play()
                if block_pick == 1:
                    voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture, id_ = block_idx)
                if block_pick == 2:
                    voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture, id_ = block_idx)
                if block_pick == 3: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture, id_ = block_idx)
                if block_pick == 4: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture, id_ = block_idx)
                if block_pick == 5: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = gold_texture, id_ = block_idx)
                if block_pick == 6: 
                    voxel = Voxel(position = self.position + mouse.normal, texture = lava_texture, id_ = block_idx)
                n.send_voxel(id_=voxel.id, position=voxel.position, texture=voxel.texture)
                voxels[int(block_idx)] = voxel
                block_idx += 1
            if key == 'right mouse down':
                punch_sound.play()
                # print(self.id)
                n.send_voxel(id_=self.id, state="delete")
                id_ = self.id
                destroy(self)
                del voxels[int(id_)]

def receive():
    while True:
        try:
            print("准备接受")
            infos = n.receive_info()
        except Exception as e:
            print(e)
            print("receive报错")
            continue

        if not infos:
            print("Server has stopped! Exiting...")
            sys.exit()
        for info in infos:
            if info["object"] == "player":
                ally_id = info["id"]

                if info["joined"]:
                    new_ally = Ally(Vec3(*info["position"]), ally_id, info["username"])
                    allies.append(new_ally)
                    continue

                ally = None

                for e in allies:
                    if e.id == ally_id:
                        ally = e
                        break

                if not ally:
                    continue

                if info["left"]:
                    allies.remove(ally)
                    destroy(ally)
                    continue

                ally.world_position = Vec3(*info["position"])
                ally.rotation_y = info["rotation"]

            elif info["object"] == "voxel":
                print("info", info)
                if info["state"] == "create":
                    global block_idx
                    string = "Voxel("
                    if info["position"] != None:
                        string += "position = info['position']"
                    if info["texture"]  != None:
                        info["texture"] = textures[int(info["texture"])]
                        print(type(info["texture"]), info["texture"])
                        string += ", texture = info['texture']"
                    if info["id"]       != None:
                        string += ", id_ = int(info['id'])"
                    if info["state"]    != None:
                        string += ", state = info['state']"
                    # if info["color"]    != None:
                    #     string += ", color = info['color']"
                    string += ')'
                    block_idx += 1
                    voxels[int(info["id"])] = eval(string)
                elif info["state"] == "delete":
                    print(info)
                    print(voxels.keys())

                    # del voxels[int(info["id"])]
                    # v = voxels[int(info["id"])]
                    destroy(voxels[int(info["id"])])
                    del voxels[int(info["id"])]
                    

            elif info["object"] == "voxels":
                for per_id in info["voxels"]:
                    position, texture = info["voxels"][per_id]
                    string = "Voxel("
                    if position != None:
                        string += "position = position"
                    if texture  != None:
                        texture = textures[int(texture)]
                        print(type(texture), texture)
                        string += ", texture = texture"
                    string += ', id_ = per_id)'
                    # print(string)
                    voxels[int(per_id)] = eval(string)

def update():
    global block_pick, prev_pos, prev_dir

    if prev_pos != player.world_position or prev_dir != player.world_rotation_y:
        n.send_player(player)

    prev_pos = player.world_position
    prev_dir = player.world_rotation_y

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4
    if held_keys['5']: block_pick = 5
    if held_keys['6']: block_pick = 6



class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True)

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6))

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.4,-0.6)



player = FirstPersonController()
sky = Sky()
hand = Hand()

prev_pos = player.world_position
prev_dir = player.world_rotation_y
allies = []
voxels = {}

msg_thread = threading.Thread(target=receive, daemon=True)
msg_thread.start()
# print("线程已启动, 正在sleep")
# # time.sleep(3)
# print("开始app.run")
app.run()