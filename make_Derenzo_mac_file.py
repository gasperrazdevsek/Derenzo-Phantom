# -----------------------------------------------------------------------------------------------------
# Create GATE source macro file corresponding to Derenzo phantom
# -----------------------------------------------------------------------------------------------------

import numpy as np
import math

# Background cylinder
R = 150 # mm
H = 50 # mm

d_arr = np.array([1.5, 2, 2.5, 3, 4, 5]) # rod diameters (mm)
h = 40 # rod heights
r = 10 # distance of rod edges from the center

a = R - 2*r # side length of the triangular pattern
n_arr = np.ceil(np.floor(a/d_arr)/2) # number of rods forming the side of the triangular pattern

a_bgr = 0.1 # specific activity (Bq/mm3)
A_bgr = round(a_bgr*3.141592*R*R*H,3)


myfile = open('Source_Derenzo.mac', 'w')

text1 = f"""#=======================================================================
# Sources corresponding to Derenzo phantom
# Generated with: make_Derenzo_mac_file.py
# Background cylinder: height = {H} mm, radius = {R} mm
# Rod diameters: {d_arr[0]}, {d_arr[1]}, {d_arr[2]}, {d_arr[3]}, {d_arr[4]}, {d_arr[5]} mm
# Rod heights: {h} mm
# Distance of rod edges from the center: {r} mm
# Specific activity: a_bgr = {a_bgr} Bq/mm3, a_rod = 100*a_bgr
#=======================================================================

# Background cylinder
/gate/source/addSource                        bgr_cylinder
/gate/source/bgr_cylinder/gps/centre     0.0 0.0 0.0 mm
/gate/source/bgr_cylinder/gps/type       Volume
/gate/source/bgr_cylinder/gps/shape      Cylinder
/gate/source/bgr_cylinder/gps/radius     {R} mm
/gate/source/bgr_cylinder/gps/halfz      {H/2} mm
/gate/source/bgr_cylinder/setActivity    {A_bgr} Bq
/gate/source/bgr_cylinder/setIntensity   {A_bgr}
/gate/source/bgr_cylinder/setType        backtoback
/gate/source/bgr_cylinder/gps/particle   gamma
/gate/source/bgr_cylinder/gps/ene/mono   511. keV
/gate/source/bgr_cylinder/gps/angtype    iso

# Hot rods"""

myfile.write(text1)


phi = math.pi/6 # 30 deg
for i in range(np.size(n_arr)):
    transl_vec = np.array([[r + d_arr[i]*math.cos(phi), (r + d_arr[i]) * math.sin(phi)]]).T # transpose -> column vector
    rot_matrix = np.array([[math.cos(2*phi*(i)), -math.sin(2*phi*(i))],
                          [math.sin(2*phi*(i)),  math.cos(2*phi*(i))]])
    A_rod = round(100*a_bgr*3.141592*(d_arr[i]/2)*(d_arr[i]/2)*h, 3)
    cnt = 0
    for j in range(int(n_arr[i])):
        for k in range(int(n_arr[i]-j)):
            base_vec1 = np.array([[2*d_arr[i], 0]]).T
            base_vec2 = np.array([[2*d_arr[i]*math.cos(2*phi), (2*d_arr[i]) * math.sin(2*phi)]]).T
            loc_vec = j*base_vec2 + k*base_vec1 # rod location relative to center
            loc_vec = loc_vec + transl_vec # translate
            loc_vec = np.dot(rot_matrix, loc_vec) # rotate
            cnt = cnt + 1
            text_rods = f"""\n
/gate/source/addSource               rod_{int(i+1)}_{cnt}
/gate/source/rod_{int(i+1)}_{cnt}/gps/centre     {round(loc_vec[0][0], 3)} {round(loc_vec[1][0], 3)} 0.0 mm
/gate/source/rod_{int(i+1)}_{cnt}/gps/type       Volume
/gate/source/rod_{int(i+1)}_{cnt}/gps/shape      Cylinder
/gate/source/rod_{int(i+1)}_{cnt}/gps/radius     {d_arr[i]/2} mm
/gate/source/rod_{int(i+1)}_{cnt}/gps/halfz      {h/2} mm
/gate/source/rod_{int(i+1)}_{cnt}/setActivity    {A_rod} Bq
/gate/source/rod_{int(i+1)}_{cnt}/setIntensity   {A_rod}
/gate/source/rod_{int(i+1)}_{cnt}/setType        backtoback
/gate/source/rod_{int(i+1)}_{cnt}/gps/particle   gamma
/gate/source/rod_{int(i+1)}_{cnt}/gps/ene/mono   511. keV
/gate/source/rod_{int(i+1)}_{cnt}/gps/angtype    iso
/gate/source/rod_{int(i+1)}_{cnt}/visualize      30 white 1"""
            myfile.write(text_rods)






