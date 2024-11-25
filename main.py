from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random

'''
TODO
increase floor
add sound
in game main menu
main menu graphics option
add anomalies
add some shaders or colors , so the game looks good.
add more anomalies and using random , randomize them on each floor where the condition is True by using random ofc
define the lightning.
make a pathway going to right or left before showing anomalies , as in the present game the person can see the anomalies from the lift only

'''

app = Ursina()
anomaly_text = None

#ANOMALIES

def reset_anomalies():
    for door in door_entities_left + door_entities_right:
        door.color = color.black
        door.enabled = True


def change_door_color():
    reset_anomalies()
    chosen_door = random.randint(0,4)
    door_entities_left[chosen_door].color = color.white

def change_room_text():
    pass

def light_flickering():
    pass

def door_open():
    pass

def earthquake():
    pass

def floor_texture_change():
    pass



def show_credits(messages, position, color=color.white, delay_between=3):
    def display_next_message(index=0):
        global anomaly_text
        if anomaly_text:
            anomaly_text.disable()  

        if index < len(messages): 
            anomaly_text = Text(messages[index], position=position, color=color)
            destroy(anomaly_text, delay=delay_between) 
            invoke(display_next_message, index + 1, delay=delay_between)  

    display_next_message() 


def show_temporary_text(message, position, color=color.white):
    global anomaly_text
    if anomaly_text:
        anomaly_text.disable()  
    anomaly_text = Text(message, position=position, color=color)
    destroy(anomaly_text, delay=3) 



class MainMenu(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.main_menu = Entity(parent=self, enabled=True)
        self.player = None

        def start():
            print(floors)
            print(floors[current_floor - 1])
            self.player.enable()
            mouse.locked = True
            self.main_menu.disable()
            self.player.time_running = True
            invoke(open_elevator_doors, delay=1)
            background_music = Audio('bg.mp3', loop=True, autoplay=True, volume=0.5)


        title = Entity(model="quad", texture="assets/mainmenu", parent=self.main_menu, y=0, scale_x=1.8)
        start_button = Button(text="S t a r t  G a m e", color=color.hsv(0, 0, 0, .8), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=-0.3)
        quit_button = Button(text="Q u i t", color=color.hsv(0, 0, 0, .8), scale_y=0.1, scale_x=0.3, y=-0.22, parent=self.main_menu, x=0.3)
        quit_button.on_click = application.quit
        start_button.on_click = Func(start)

# Environment setup
reflective_shader = Shader(
    vertex="""
    #version 330
    uniform mat4 modelview_projection;
    in vec3 vertex_position;
    in vec3 vertex_normal;
    out vec3 frag_normal;
    out vec3 frag_position;
    void main() {
        frag_position = vertex_position;
        frag_normal = vertex_normal;
        gl_Position = modelview_projection * vec4(vertex_position, 1.0);
    }
    """,
    fragment="""
    #version 330
    in vec3 frag_normal;
    in vec3 frag_position;
    out vec4 color;
    uniform samplerCube skybox;
    void main() {
        vec3 reflected = reflect(normalize(frag_position), normalize(frag_normal));
        color = texture(skybox, reflected);
    }
    """
)

ground = Entity(model='cube', collider='box', scale_x=49, scale_z=5, origin_y=4.5, texture='assets/floor2', scale_y=1, shader=lit_with_shadows_shader)
wall1 = Entity(model='cube', collider='box', scale_x=49, scale_z=1, texture='white_cube', scale_y=10, origin_x=0, origin_z=3, origin_y=0, color=color.dark_gray, shader=reflective_shader)
wall2 = Entity(model='cube', collider='box', scale_x=49, scale_z=1, texture='white_cube', scale_y=10, origin_x=0, origin_z=-3, origin_y=0, color=color.dark_gray, shader=reflective_shader)
wall3 = Entity(model='cube', collider='box', scale_x=1, scale_z=10, texture='white_cube', scale_y=10, origin_x=-25, origin_y=0, color=color.dark_gray, shader=reflective_shader)
wall4 = Entity(model='cube', collider='box', scale_x=1, scale_z=10, texture='white_cube', scale_y=10, origin_x=25, origin_y=0, color=color.dark_gray, shader=lit_with_shadows_shader)
roof = Entity(model='cube', collider='box', scale_x=49, scale_z=5, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.black90)
roof.y = 5

elevator_gate1 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, 1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray, collider='box')
elevator_gate2 = Entity(model='cube', scale=(0.2, 8.6, 2.5), position=(-20, 0, -1.25), texture='white_cube', shader=lit_with_shadows_shader, color=color.dark_gray, collider='box')

# directional_light = DirectionalLight(parent=scene,rotation=Vec3(80, 0, 0),position=(0,-5,0))

# directional_light.intensity = 0.5 

light1 = PointLight(parent=scene, rotation=Vec3(90, 0, 0))
light2 = PointLight(parent=scene, rotation=Vec3(90, 0, 0),position=(-27,0,0))







# wall1.shader = reflective_shader
# wall2.shader = reflective_shader
# wall3.shader = reflective_shader
# wall4.shader = reflective_shader
# ground.shader = reflective_shader

liftroof = Entity(model='cube', collider='box', scale_x=4, scale_z=6, texture='white_cube', scale_y=1, shader=lit_with_shadows_shader, color=color.dark_gray, position=(-22.5, 3, 0))

door_entities_left = []
door_entities_right = []
text_entities_left = []
text_entities_right = []

door_texts_left = ["Room 1", "Room 2", "Room 3", "Room 4", "Room 5"]
door_texts_right = ["Room 10", "Room 9", "Room 8", "Room 7", "Room 6"]

for i in range(5):
    door1 = Entity(model='cube', collider='box', scale=(2, 3.8, 0.05), texture='white_cube', origin=(i * -3, 0.6, -49), color=color.black, x=-12, shader=lit_with_shadows_shader)
    door2 = Entity(model='cube', collider='box', scale=(2, 3.8, 0.05), scale_x=2, texture='white_cube', origin=(i * -3, 0.6, 49), color=color.black, x=-12, shader=lit_with_shadows_shader)
    text = Text(text=door_texts_left[i], parent=door1, scale=(3, 3, 3), color=color.black)
    text2 = Text(text=door_texts_right[i], parent=door2, scale=(3, 3, 3), color=color.black, rotation=(180, 0, 180))
    text.position = ((i * 3) - 0.1, 0, 49)
    text2.position = ((i * 3) + 0.1, 0, -49)
    door_entities_left.append(door1)
    door_entities_right.append(door2)
    text_entities_left.append(text)
    text_entities_right.append(text2)

m = MainMenu()
# EditorCamera()
player = FirstPersonController()
player.y = -4
player.x = -24
player.rotation_y = 90
player.disable()
player.speed = 9
m.player = player
player.height = 4
player.cursor.color = color.red

shift_player = 3
s = Sky(texture='assets/walltext.png')
# light2 = SpotLight(parent=camera.ui, rotation=Vec3(0, 0, 90),position=(0,3,0))
# light2.look_at(player,axis='up')



floors = [False, False, False, False, False, False, False, False] 
current_floor = 8

foot = Audio('foot.mp3', autoplay=False,loop=False)


def randomize_floors():
    global floors
    floors = [random.choice([True, False]) for _ in range(8)]
    if not any(floors):
        floors[random.randint(0, 7)] = True
    


def reset_game():
    global current_floor
    current_floor = 8
    randomize_floors()
    apply_anomalies()
    player.y = -4 
def apply_anomalies():
    
    if floors[current_floor - 1]: 
        anomaly_index = current_floor - 1  
        
        change_door_color()
    else:
        reset_anomalies()

def destroy_doors():
    for door in door_entities_left:
        destroy(door)

    for door in door_entities_right:
        destroy(door)

def update_floor(floor_delta):
    global current_floor
    global floors
    next_floor = current_floor + floor_delta

    if next_floor < 1:
        current_floor = 1
        show_temporary_text("Congratulations, you cleared the game!", position=(0.38, -0.3))
        player.rotation_y = 90
        player.rotation_x = 10
        player.x = -19
        s.texture="sky_default"
        player.cursor.disable()
        player.disable()
        credits = ['Thank you for playing our python project',
                    'Made by team Bit Benders']

        show_credits(credits, position=(-0.2, 0), color=color.white, delay_between=5)
        

    elif next_floor > 8:
        current_floor = 8
        show_temporary_text("Same floor again.", position=(0.38, 0))
    else:
        current_floor = next_floor
        # show_temporary_text(f"Correct! Moving to floor {current_floor}", position=(0.38, 0))

    apply_anomalies()
    print(f"Current floor: {current_floor}, Floors: {floors}")

keys_pressed = {'w': False, 'a': False, 's': False, 'd': False}

def update():
    if player.y < -40:
        player.y = 3
    if player.x > -20:
        if doors_open:
            invoke(close_elevator_doors, delay=2)
    

    

    
    
    Text(text=f"Current floor: {current_floor}", position=(0.38, 1))

sound_playing=True
keys_held = {'w': False, 'a': False, 's': False, 'd': False}
def input(key):
    global doors_open, sound_playing, keys_held,light1
    player.speed = shift_player if held_keys['shift'] else 7

    if key == "h":
        invoke(open_elevator_doors, delay=0)
    
   
    if key in keys_held:
        if not keys_held[key]:
            keys_held[key] = True
            if any(keys_held.values()):  # If any movement key is held
                foot.play()

    elif key in [f'{key} up' for key in keys_held]:
        keys_held[key[0]] = False
        if not any(keys_held.values()):  # Stop sound when no movement keys are held
            foot.stop()

    
    
    

    

doors_open = False

def open_elevator_doors():
    global doors_open
    elevator_gate1.position = Vec3(-20, 0, 1.25)
    elevator_gate2.position = Vec3(-20, 0, -1.25)
    elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, 2), duration=1)
    elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, -2), duration=1) 
    doors_open = True
    invoke(close_elevator_doors, delay=3)  

def close_elevator_doors():
    global doors_open
    if doors_open:
        elevator_gate1.animate_position(elevator_gate1.position + Vec3(0, 0, -2), duration=1) 
        elevator_gate2.animate_position(elevator_gate2.position + Vec3(0, 0, 2), duration=1) 
        doors_open = False


class ElevatorUp(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="Anomaly Spotted", 
            color=color.hsv(0, 0, .5, .5),
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-1,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if floors[current_floor - 1]:  
                    show_temporary_text(f"Correct! Moving down to {current_floor-1}", position=(0.38, -0.3))
                    update_floor(-1) 
                    invoke(open_elevator_doors, delay=2)

                else:
                    show_temporary_text(f"Wrong! Moving back up to {current_floor+1}", position=(0.38, 0.3))
                    update_floor(1) 
                    invoke(open_elevator_doors, delay=2)

class ElevatorDown(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            text="No Anomaly Spotted", 
            color=color.hsv(0, 0, .5, .5), 
            scale_y=0.5,
            scale_x=1.5, 
            parent=scene,
            rotation=(0,180,0), 
            position=(-22,-2,-2.4),
            shader=lit_with_shadows_shader)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                if not floors[current_floor - 1]:  
                        show_temporary_text(f"Correct! Moving down to {current_floor-1}", position=(0.38, -0.3))
                        update_floor(-1)
                        invoke(open_elevator_doors, delay=2)
                else: 
                    show_temporary_text(f"Wrong! Moving back up to {current_floor+1}", position=(0.38, 0.3))
                    update_floor(1)
                    invoke(open_elevator_doors, delay=2)
                    


up = ElevatorUp()
down = ElevatorDown()

up.text_entity.scale = (4, 10)
up.text_entity.color = color.white
down.text_entity.scale = (4, 10)
down.text_entity.color = color.white

# spotlight = PointLight(parent=camera, position=(0, 0, 0), rotation=(0, 0, 0),fov=90, color=color.rgb(5,5,5), shadows=True)

reset_game()
window.render_mode = 'default'
window.borderless = False
app.run()