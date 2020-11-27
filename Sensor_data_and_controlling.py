import glob
import os
import sys
import time
import random
import numpy as np

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass


import carla

IM_WIDTH = 640
IM_HEIGHT = 480

def process_img(image):
    i = np.array(image.raw_data)
    print(dir(image))

actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(10.0)

    world = client.get_world()

    blueprint_library = world.get_blueprint_library()

    bp = blueprint_library.filter('model3')[0]
    print(bp)

    spawn_point = random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp, spawn_point)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    actor_list.append(vehicle)

    cam_bp = blueprint_library.find("sensor.camera.rgb")
    cam_bp.set_attribute("image_size_x",f"(IM_WIDTH)")
    cam_bp.set_attribute("image_size_y",f"(IM_HEIGHT)")
    cam_bp.set_attribute("fov","110")

    spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))

    sensor = world.spawn_actor(cam_bp, spawn_point, attach_to=vehicle)

    actor_list.append(sensor)

    sensor.listen(lambda data: process_img(data))



    # sleep for 5 seconds, then finish:
    time.sleep(5)

finally:

    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('All Cleaned up')