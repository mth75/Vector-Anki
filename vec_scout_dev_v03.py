import anki_vector, time, math, requests
from anki_vector.util import degrees, distance_mm, speed_mmps
from PIL import Image, ImageStat
from anki_vector.events import Events
import functools
import threading
import os

robot = anki_vector.Robot()
robot.connect()

angle = 90

#determine distance
def dist():
    with anki_vector.Robot(requires_behavior_control=False) as robot:
        proximity_data = robot.proximity.last_sensor_reading.distance
        distance_mm = (int(proximity_data.distance_mm))
    return distance_mm

if __name__ == "__dist__":
    dist()

def img_brightness():
    with anki_vector.Robot(enable_camera_feed=True, requires_behavior_control=True) as robot:
        while not robot.camera.latest_image:
            time.sleep(0.5)
        image = robot.camera.latest_image
        #image.show()
        stat = ImageStat.Stat(image)
        r,g,b = stat.mean
        actual_light_value = math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))
    return actual_light_value

if __name__ == "__img_brightness__":
    img_brightness()


def drive_straight():
    dynamic_speed = dist() * 0.18333333
    dynamic_distance = dist() * 0.75
    print("average brightness:", img_brightness(), "dynamic speed:", dynamic_speed, "dynamic distance", dynamic_distance, "/", dist())
    with anki_vector.Robot(requires_behavior_control=True) as robot:
        # determine distance
        proximity_data = robot.proximity.last_sensor_reading.distance
        distance_mm = (int(proximity_data.distance_mm))
        robot.behavior.drive_straight(distance_mm(dynamic_distance),speed_mmps(dynamic_speed))

def drive_turn():
    with anki_vector.Robot(requires_behavior_control=True) as robot:
        robot.behavior.turn_in_place(degrees(angle))

#driving "loop" determined by proximity and environment illumination
while dist() > 50 or img_brightness() > 25:
    drive_straight()
    while dist() < 50 or img_brightness() < 25:
        drive_turn()
        while dist() > 50 or img_brightness() < 25:
            drive_straight()

# drive straight
# until
# event (proximity meter)
# increase speed while proximity is <=500
# then turn
# if brightness is < x
# then turn
# until brightness is > x
# then drive straight
