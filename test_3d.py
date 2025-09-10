import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
# 新增：导入动画模块
import matplotlib.animation as animation

def plot_3d_polygons(polygons, thicknesses, elev=30, azim=45, figsize=(10, 8)):
    """
    绘制多个带有厚度的3D多边形（原函数保持不变）
    """
    if len(polygons) != len(thicknesses):
        raise ValueError("多边形数量与厚度数量必须相等")
    
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    colors = plt.cm.Set3(np.linspace(0, 1, len(polygons)))
    
    for i, (poly_points, thickness) in enumerate(zip(polygons, thicknesses)):
        vertices = np.array(poly_points)
        # 计算法向量（确定厚度方向）
        v1 = vertices[1] - vertices[0]
        v2 = vertices[2] - vertices[0]
        normal = np.cross(v1, v2)
        normal = normal / np.linalg.norm(normal)
        # 偏移顶点（生成厚度）
        offset_vertices = vertices + normal * thickness
        
        # 生成侧面多边形
        sides = []
        for j in range(len(vertices)):
            k = (j + 1) % len(vertices)
            side = [vertices[j], vertices[k], offset_vertices[k], offset_vertices[j]]
            sides.append(side)
        
        # 合并顶面、底面、侧面
        all_faces = [offset_vertices] + [vertices] + sides
        # 创建3D多边形集合
        poly3d = Poly3DCollection(all_faces, alpha=0.7)
        poly3d.set_facecolor(colors[i])
        poly3d.set_edgecolor('k')
        ax.add_collection3d(poly3d)
    
    # 自动调整坐标轴范围
    all_points = np.concatenate(polygons)
    max_range = np.array([
        all_points[:, 0].max() - all_points[:, 0].min(),
        all_points[:, 1].max() - all_points[:, 1].min(),
        all_points[:, 2].max() - all_points[:, 2].min()
    ]).max() / 2.0
    
    mid_x = (all_points[:, 0].max() + all_points[:, 0].min()) * 0.5
    mid_y = (all_points[:, 1].max() + all_points[:, 1].min()) * 0.5
    mid_z = (all_points[:, 2].max() + all_points[:, 2].min()) * 0.5
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D 多边形集合（旋转动画）')
    
    return fig, ax

# -------------------------- 新增：动画核心逻辑 --------------------------
def animate_3d_rotation(fig, ax, total_frames=360, interval=50, save_path='3d_polygons_rotation.gif'):
    """
    让3D图绕Y轴旋转（通过更新方位角azim实现）
    
    参数:
        fig: matplotlib.figure.Figure
            已创建的图形对象
        ax: mpl_toolkits.mplot3d.Axes3D
            已创建的3D轴对象
        total_frames: int, 可选
            总帧数（360帧对应旋转360度），默认360
        interval: int, 可选
            帧间隔（毫秒），越小旋转越快，默认50
        save_path: str, 可选
            动画保存路径（GIF格式），默认当前目录
    """
    # 定义每一帧的更新函数：仅改变方位角azim
    def update(frame):
        # 每帧旋转1度（frame从0到total_frames-1，对应azim从0到359度）
        ax.view_init(elev=ax.elev, azim=frame % 360)
        return ax,  # 返回更新后的轴对象
    
    # 创建动画对象
    ani = animation.FuncAnimation(
        fig=fig,          # 绑定的图形
        func=update,      # 每帧执行的更新函数
        frames=total_frames,  # 总帧数
        interval=interval,    # 帧间隔（毫秒）
        blit=False        # 3D图建议关闭blit（避免渲染异常）
    )
    
    # 保存动画（需安装pillow库：pip install pillow）
    try:
        ani.save(save_path, writer='pillow', fps=1000/interval)
        print(f"动画已保存至：{save_path}")
    except Exception as e:
        print(f"保存动画失败：{e}")
        print("提示：需安装pillow库（执行命令：pip install pillow）")
    
    return ani

# 示例用法（含旋转动画）
if __name__ == "__main__":
    # 1. 定义3D多边形（与原代码一致）
    polygon1 = [(0, 0, 0), (2, 0, 0), (2, 2, 0), (0, 2, 0)]  # 正方形
    polygon2 = [(3, 1, 1), (5, 1, 1), (5, 3, 1), (4, 4, 1), (3, 3, 1)]  # 五边形
    polygon3 = [(1, 3, 2), (3, 5, 2), (5, 3, 2)]  # 三角形
    polygons = [polygon1, polygon2, polygon3]
    thicknesses = [0.5, 0.8, 0.6]  # 对应每个多边形的厚度
    
    # 2. 绘制静态3D多边形
    fig, ax = plot_3d_polygons(polygons, thicknesses, elev=30, azim=0)
    
    # 3. 启动旋转动画并保存
    ani = animate_3d_rotation(
        fig=fig,
        ax=ax,
        total_frames=360,  # 旋转360度
        interval=50,       # 每50毫秒一帧（20 FPS）
        save_path='3d_polygons_rotation.gif'  # 保存路径
    )
    
    # 显示动画（需保持plt.show()，否则窗口会立即关闭）
    plt.show()