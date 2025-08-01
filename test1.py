import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# 设置中文字体支持
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 生成示例数据
np.random.seed(42)
n_points = 2000

# Voltage数据 (x轴) - 范围从0.8V到1.2V
voltage = np.random.uniform(0.8, 1.2, n_points)

# Process (Models) 数据 (y轴) - 使用离散的工艺角名称
process_models = ['FF', 'FS', 'TT', 'SF', 'SS']
process_indices = np.random.randint(0, len(process_models), n_points)
process = [process_models[i] for i in process_indices]

# 将工艺角转换为数值以便绘图
process_mapping = {model: i for i, model in enumerate(process_models)}
process_values = np.array([process_mapping[m] for m in process])

# Temperatures数据 (z轴) - 范围从-40°C到125°C
temperature = np.random.uniform(-40, 125, n_points)

# 为每个工艺角分配不同的颜色
colors = cm.rainbow(np.linspace(0, 1, len(process_models)))
process_colors = np.array([colors[i] for i in process_indices])

# 创建3D图形
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D散点图
scatter = ax.scatter(voltage, process_values, temperature, 
                     c=process_colors, s=100, alpha=0.8, edgecolors='w')

# 设置坐标轴标签和标题
# 4. 坐标轴与标签优化
ax.set_xlabel('Voltage (V)', fontsize=14, labelpad=0)
ax.set_ylabel('Process Model', fontsize=14, labelpad=5)
ax.set_zlabel('Temperature (°C)', fontsize=14, labelpad=-2)  # ② 增加Z轴标签与轴的距离
# ax.set_title('Voltage - Process - Temperature 3D 散点图', fontsize=15)

# 设置y轴刻度为工艺角名称
ax.set_yticks(range(len(process_models)))
ax.set_yticklabels(process_models)

# 添加颜色条图例
legend = ax.legend(*scatter.legend_elements(), 
                  title="Process Models", 
                  loc="upper right", 
                  bbox_to_anchor=(1.1, 1))
ax.add_artist(legend)

# 添加网格以提高可读性
ax.grid(True)

# 设置视角
ax.view_init(elev=35, azim=45)

# 显示图形
# plt.tight_layout()
plt.show()