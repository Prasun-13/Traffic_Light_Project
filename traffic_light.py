# ---------------------------------------------------------
# Traffic Light Simulation (Project #9 - GVC Submission)
# Author : Prasun Kumar
# Roll No : 29
# Tool : Autodesk Maya + Python (maya.cmds)
# ---------------------------------------------------------

import maya.cmds as cmds

# ---------------- PARAMETERS ----------------
roll_no = 29                          # Used for identity / variation
green_frames = 60                     # Duration of green light
yellow_frames = 20                    # Duration of yellow light
red_frames = 60                       # Duration of red light
cycles = 4                            # How many full cycles to animate
start_frame = 1                       # Start of the animation timeline
# ----------------------------------------------------------

# --- Delete old traffic light if re-running script ---
if cmds.objExists("traffic_light_grp"):
    cmds.delete("traffic_light_grp")

# --- Create group for the whole setup ---
grp = cmds.group(empty=True, name="traffic_light_grp")

# --- Housing (traffic light box) ---
housing = cmds.polyCube(w=3, h=10, d=2, name="housing_geo")[0]
cmds.parent(housing, grp)
cmds.move(0, 5, 0, housing)

# --- Three light spheres: Red, Yellow, Green ---
red_s = cmds.polySphere(r=0.8, name="red_light")[0]
yellow_s = cmds.polySphere(r=0.8, name="yellow_light")[0]
green_s = cmds.polySphere(r=0.8, name="green_light")[0]

cmds.parent([red_s, yellow_s, green_s], grp)

cmds.move(0, 7, 1.01, red_s)
cmds.move(0, 4, 1.01, yellow_s)
cmds.move(0, 1, 1.01, green_s)

# Slight scale for nicer look
for s in (red_s, yellow_s, green_s):
    cmds.setAttr(s + ".scaleX", 0.95)
    cmds.setAttr(s + ".scaleZ", 0.95)

# --- Create colored lambert materials ---
def make_mat(name, color, inc=0.8):
    mat = name + "_mat"
    if cmds.objExists(mat):
        cmds.delete(mat)
    mat = cmds.shadingNode("lambert", asShader=True, name=mat)
    cmds.setAttr(mat + ".color", color[0], color[1], color[2], type="double3")
    cmds.setAttr(mat + ".incandescence", color[0]*inc, color[1]*inc, color[2]*inc, type="double3")
    sg = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=mat + "SG")
    cmds.connectAttr(mat + ".outColor", sg + ".surfaceShader")
    return sg

red_sg = make_mat("red", (1,0,0))
yellow_sg = make_mat("yellow", (1,1,0))
green_sg = make_mat("green", (0,1,0))

cmds.sets(red_s, e=True, forceElement=red_sg)
cmds.sets(yellow_s, e=True, forceElement=yellow_sg)
cmds.sets(green_s, e=True, forceElement=green_sg)

# Start with all OFF
cmds.setAttr(red_s + ".visibility", 0)
cmds.setAttr(yellow_s + ".visibility", 0)
cmds.setAttr(green_s + ".visibility", 0)

# -------------------- ANIMATION ---------------------
frame = start_frame
total = green_frames + yellow_frames + red_frames

cmds.playbackOptions(min=start_frame, max=start_frame + cycles*total)

for _ in range(cycles):

    # GREEN ON
    cmds.setKeyframe(green_s, attribute="visibility", t=frame, v=1)
    cmds.setKeyframe(yellow_s, attribute="visibility", t=frame, v=0)
    cmds.setKeyframe(red_s, attribute="visibility", t=frame, v=0)
    frame += green_frames

    # YELLOW ON
    cmds.setKeyframe(green_s, attribute="visibility", t=frame, v=0)
    cmds.setKeyframe(yellow_s, attribute="visibility", t=frame, v=1)
    cmds.setKeyframe(red_s, attribute="visibility", t=frame, v=0)
    frame += yellow_frames

    # RED ON
    cmds.setKeyframe(green_s, attribute="visibility", t=frame, v=0)
    cmds.setKeyframe(yellow_s, attribute="visibility", t=frame, v=0)
    cmds.setKeyframe(red_s, attribute="visibility", t=frame, v=1)
    frame += red_frames

print("Traffic Light Simulation Ready!")
