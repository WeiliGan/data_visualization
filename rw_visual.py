import matplotlib.pyplot as plt


from random_walk import RandomWalk

# 创建一个RandomWalk实例，并将其包含的点都绘制出来
rw = RandomWalk()
rw.fill_walk()
plt.scatter(rw.x_values, rw.y_values, s=15)
plt.show()
