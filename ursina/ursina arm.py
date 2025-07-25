from ursina import *
from ursina.shaders import lit_with_shadows_shader
import math
import time

app = Ursina(fullscreen=False, borderless=True, size=(1920,1080))
window.editor_ui.enable()
total_runtime = 0
start_time = time.time()

Sky(texture='sky_default')

spherical1 = Entity(model='sphere',
             #scale=0.5,
             color=color.red,
             position= (0,0,0),
             rotation= (0,0,0),
             shader= lit_with_shadows_shader)

box1 = Entity(model='cube',
             color=color.white,
             scale=0.8,
             texture='assets/rabbit_fur.png',
             position= (0.5,-0.5,0),
             rotation= (0,0,45),
             shader= lit_with_shadows_shader,
             parent=spherical1)



spherical2 = Entity(model='sphere',
             color=color.red,
             scale_x=1/3,
             position= (0.60,0,0),
             rotation= (0,0,0),
             shader= lit_with_shadows_shader,
             parent=box1)


box2 = Entity(model='cube',
             scale_x=3,
             color=color.white,
             texture='brick',
             position= (1.35,0,0),
             rotation= (0,0,0),
             shader= lit_with_shadows_shader,
             parent=spherical2)

model3 = Entity(model = 'assets/torus.obj')


# floor = Entity(model='plane',
#                scale=10,
#                texture='grass',
#                color=color.green,
#                position= (0,-5,0),
#                rotation=(0,0,0),
#                shader= lit_with_shadows_shader)

# dl = DirectionalLight(shadows=True,
#                       position=(0,0,0),
#                       color=rgb(2,0,0))
# dl.look_at(box)

# camera.position = (0,2,-5)
# camera.look_at(box)
# camera.look_at(Vec3(0,0,0))

def update():
    global total_runtime
    total_runtime = time.time() - start_time
    print("total runtime: ", total_runtime)

    spherical2.rotation_z += sin(time.time())
    spherical1.rotation_z += sin(time.time())

EditorCamera()

app.run()