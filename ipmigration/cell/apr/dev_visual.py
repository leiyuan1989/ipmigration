# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 16:00:22 2024

@author: Administrator
"""

import matplotlib.pyplot as plt
import numpy as np

ax = plt.figure().add_subplot(projection='3d')

# Plot a sin curve using the x and y axes.
x = np.linspace(0, 1, 100)
y = np.sin(x * 2 * np.pi) / 2 + 0.5
ax.plot(x, y, zs=0, zdir='z', label='curve in (x, y)')

# Plot scatterplot data (20 2D points per colour) on the x and z axes.
colors = ('r', 'g', 'b', 'k')

# Fixing random state for reproducibility
np.random.seed(19680801)

x = np.random.sample(20 * len(colors))
y = np.random.sample(20 * len(colors))
c_list = []
for c in colors:
    c_list.extend([c] * 20)
# By using zdir='y', the y value of these points is fixed to the zs value 0
# and the (x, y) points are plotted on the x and z axes.
ax.scatter(x, y, zs=0, zdir='y', c=c_list, label='points in (x, z)')

# Make legend, set axes limits and labels
ax.legend()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_zlim(0, 1)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Customize the view angle so it's easier to see that the scatter points lie
# on the plane y=0
ax.view_init(elev=20., azim=-35, roll=0)

plt.show()

import matplotlib.pyplot as plt
import numpy as np

# Fixing random state for reproducibility
np.random.seed(19680801)


def randrange(n, vmin, vmax):
    """
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    """
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, marker=m,color='red')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()






# Prepare arrays x, y, z
theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
z = np.linspace(-2, 2, 100)
r = z**2 + 1
x = r * np.sin(theta)
y = r * np.cos(theta)




# ax.plot(x, y, z, linestyle = '--', label='parametric curve')
# ax.plot([1], [1], [-1], linestyle = 'o', label='parametric curve')



# n = 100





# # For each set of style and range settings, plot n random points in the box
# # defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zlow, zhigh)
#     ax.scatter(xs, ys, zs, marker=m, alpha=0.3, edgecolors='none', color=['red']*100)


# gg
import matplotlib.pyplot as plt
import numpy as np
FIG_SIZE = (20, 20)
# ax = plt.figure(). add_subplot(projection='3d')
fig = plt.figure(figsize = FIG_SIZE)
ax = fig.add_subplot(111, projection='3d')


xs = []
ys = []
zs = []
color = []
for node in g.nodes:
    data = g.nodes[node]
    xs.append(data['pos'][0])
    ys.append(data['pos'][1])
    zs.append(-1*data['pos'][2])
    color.append(data['color'])
    
ax.scatter(xs, ys, zs, marker='o', s= 250, alpha=0.3, edgecolors='none', color=color)    

for edge in g.edges:
    data = g.edges[edge]
    p1 =  g.nodes[edge[0]]['pos']
    p2 =  g.nodes[edge[1]]['pos']
    x = [p1[0],p2[0]]
    y = [p1[1],p2[1]]
    z = [-1*p1[2],-1*p2[2]]
    
    ax.plot(x, y, z, linestyle = data['linestyle'],color='grey')




ax.legend()

ax.set_zlim(-3,-10)
ax.set_xticks([])
ax.set_yticks([])
# ax.set_zticks([])
# ax.set_axis_off()



# ax.view_init(-140, 10) 
# plt.show()



ax.view_init(45, 45) 
plt.show()






import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)


fig, ax = plt.subplots()
for color in ['tab:blue', 'tab:orange', 'tab:green']:
    n = 750
    x, y = np.random.rand(2, n)
    scale = 200.0 * np.random.rand(n)
    ax.scatter(x, y, c=color, s=scale, label=color,
               alpha=0.3, edgecolors='none')

ax.legend()
ax.grid(True)

plt.show()








