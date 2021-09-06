import matplotlib.pyplot as plt
import matplotlib.image as mpimg

fig, ax = plt.subplots()

atlas_data = [['Kookaburra',
   51.441334059998,
   3.5958241584686],
 ['White-faced heron',
   52.098821802977,
   5.1797058644882]]

def mapping_data(atlas_data):
    x, y = [], []
    for i in range(len(atlas_data)):
        x.append(atlas_data[i][1])
        y.append(atlas_data[i][2])
    return x, y

y, x = mapping_data(atlas_data)

print(x,y)

ax.scatter(x, y, edgecolors='red', linewidths=1, zorder=2)
#ax.annotate('local max', xy=(5,52), xytext=(5.3,52.1),arrowprops=dict(facecolor='black', shrink=1),)

for i in range(len(atlas_data)):
    ax.annotate(atlas_data[i][0], xy=(atlas_data[i][2],atlas_data[i][1]), xytext=(atlas_data[i][2],atlas_data[i][1]+0.1),arrowprops=dict(facecolor='black', shrink=0.1),)

ax.imshow(mpimg.imread('https://i.ibb.co/8xKy10y/Kaart-Nederland-grijs.png'), extent=(  3.2674058600277225, 7.222483905734761, 50.74706431634171, 53.54700518476279), zorder=1)

plt.show()