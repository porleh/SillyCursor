# v1.0.0

from gc import callbacks
import obspython as S
import time
import random
import pyautogui
from itertools import cycle

_version_ = "v1.0.0"
lastX = 0
lastY = 0
lastMove = time.time()

isCursor = False


def update_text():
    global image_x, image_y, x_speed, y_speed, isCursor, lastX, lastY, lastMove
    scene = S.obs_get_scene_by_name(scene_name)
    scene_item = S.obs_scene_find_source(scene, source_name)
    if scene_item:
        pos = S.vec2()
        try:
            x, y = pyautogui.position()
        except:
            x = 0
            y = 0
        if (x != lastX or y != lastY) and x > image_half  and y > image_half:
            lastX = x 
            lastY = y
            lastMove = time.time()
        if x > monitor_x-image_half or x < image_half or y < image_half or y > monitor_y-image_half or (time.time() - lastMove) > input_s:
            if isCursor:
                image_x = min(lastX, monitor_x - image_half)
                image_y = min(lastY, monitor_y - image_half)
                x_speed = speed_var
                y_speed = speed_var
            if (image_x >= (monitor_x - image_half)) or (image_x < image_half):
                x_speed = -x_speed
            if (image_y >= (monitor_y - image_half)) or (image_y < image_half):
                y_speed = -y_speed
            image_x += x_speed
            image_y += y_speed
            pos.x = image_x - image_half
            pos.y = image_y - image_half
            isCursor = False
        else:
            pos.x = x - image_half 
            pos.y = y - image_half
            isCursor = True
        S.obs_sceneitem_set_pos(scene_item, pos)
    S.obs_scene_release(scene)


description = """
<h2 style="color:lightpink">SillyCursor Version : {_version_}</h2>
<a>ponicursor edit , credits: </a><a style="color:lightpink" href="https://github.com/jojoe77777">jojoe77777</a>
<h3>Author:</h3>
<a style="color:lightpink" href="https://www.twitch.tv/pauule">pauule</a> 
""".format(
    **locals()
)

def script_description():
    print("hey :3")
    return description

def script_update(settings):
    S.timer_remove(update_text)
    S.timer_add(update_text, 10)

    global scene_name
    scene_name = S.obs_data_get_string(settings, "_scene")
    print(scene_name) 

    global source_name
    source_name = S.obs_data_get_string(settings, "_source")
    print(source_name) 

    global speed_var
    speed_var = S.obs_data_get_double(settings, "_speed")
    print(speed_var) 

    global monitor_x
    monitor_x = S.obs_data_get_double(settings, "_monitor_x")
    print(monitor_x) 

    global monitor_y
    monitor_y = S.obs_data_get_double(settings, "_monitor_y")
    print(monitor_y) 

    global input_s
    input_s = S.obs_data_get_double(settings, "_seconds")
    print(input_s) 

    global image_xy
    image_xy = S.obs_data_get_double(settings, "_image_xy")
    print(image_xy)

    global image_x
    image_x = image_xy

    global image_y
    image_y = image_xy

    global image_half
    image_half = image_xy/2

def script_properties():
    props = S.obs_properties_create()
    # disabled = S.obs_properties_add_bool(props,"_disabled","disable? ")
    # S.obs_property_set_long_description(disabled, """<a style="color:lightpink">do you want to disable the cursor?</a>""")
    S.obs_properties_add_int(props,"_monitor_x","monitor res (x)",696,10000,1)
    S.obs_properties_add_int(props,"_monitor_y","monitor res (y)",392,10000,1)
    S.obs_properties_add_int(props,"_seconds","no input (s)",0,10,1)
    S.obs_properties_add_float_slider(props,"_speed","speed",0.5,10,0.1)
    p1 = S.obs_properties_add_list(props,"_scene","cursor scene",S.OBS_COMBO_TYPE_EDITABLE,S.OBS_COMBO_FORMAT_STRING,)
    p2 = S.obs_properties_add_list(props, "_source", "source", S.OBS_COMBO_TYPE_EDITABLE,S.OBS_COMBO_FORMAT_STRING,) 
    S.obs_properties_add_int_slider(props,"_image_xy","image size",25,500,1)
   
    scenes = S.obs_frontend_get_scenes()
    for scene in scenes:
        name = S.obs_source_get_name(scene)
        S.obs_property_list_add_string(p1, name, name)
    S.source_list_release(scenes)

    sources = S.obs_enum_sources()
    for source in sources:
        name = S.obs_source_get_name(source)
        S.obs_property_list_add_string(p2, name, name)
    S.source_list_release(sources)

    return props

