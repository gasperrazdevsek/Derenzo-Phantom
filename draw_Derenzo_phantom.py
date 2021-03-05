# -----------------------------------------------------------------------------------------------------
# Draw Derenzo phantom using turtle
# -----------------------------------------------------------------------------------------------------

import turtle
import numpy as np
import math

wn = turtle.Screen()
wn.setup(5120,5120)

# This turns off screen updates
wn.tracer(0)


# Creating a turtle object(pen)
pen = turtle.Turtle()

# Defining method to draw a colored circle
def ring(rad, col):
    pen.fillcolor(col)
    pen.begin_fill()
    pen.circle(rad)
    pen.end_fill()

# Draw circle
def draw_cirle(x, y, rad, col):
    pen.up()
    pen.setpos(x, y-rad)
    pen.down
    ring(rad, col)
    pen.hideturtle()



scale = 3

# Background cylinder
R = 150*scale # mm
H = 50*scale # mm

d_arr = scale*np.array([1.5, 2, 2.5, 3, 4, 5]) # rod diameters (mm)
h = 40*scale # rod heights
r = 10*scale # distance of rod edges from the center

a = R - 2*r # side length of the triangular pattern
n_arr = np.ceil(np.floor(a/d_arr)/2) # number of rods forming the side of the triangular pattern

draw_cirle(0,0,R,'black')

phi = math.pi/6 # 30 deg
for i in range(np.size(n_arr)):
    transl_vec = np.array([[r + d_arr[i]*math.cos(phi), (r + d_arr[i]) * math.sin(phi)]]).T # transpose -> column vector
    rot_matrix = np.array([[math.cos(2*phi*(i)), -math.sin(2*phi*(i))],
                          [math.sin(2*phi*(i)),  math.cos(2*phi*(i))]])
    cnt = 0
    for j in range(int(n_arr[i])):
        for k in range(int(n_arr[i]-j)):
            base_vec1 = np.array([[2*d_arr[i], 0]]).T
            base_vec2 = np.array([[2*d_arr[i]*math.cos(2*phi), (2*d_arr[i]) * math.sin(2*phi)]]).T
            loc_vec = j*base_vec2 + k*base_vec1 # rod location relative to center
            loc_vec = loc_vec + transl_vec # translate
            loc_vec = np.dot(rot_matrix, loc_vec) # rotate
            draw_cirle(loc_vec[0][0], round(loc_vec[1][0]), d_arr[i]/2, 'white')

# Update the screen to see the changes
wn.update()

# Save the image
#wn.getcanvas().postscript(file="img_Derenzo_sources.eps")

# Keep the window open
wn.mainloop()