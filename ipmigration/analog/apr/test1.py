import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def rotate(box, transform, center_point):
    """
    对矩形进行旋转和镜像变换，所有变换围绕指定点进行
    """
    left, right, top, bottom = box
    center_x, center_y = center_point
    
    # 计算宽度和高度
    width = right - left
    height = bottom - top
    
    if transform == 'R0':
        new_left, new_right = left, right
        new_top, new_bottom = top, bottom
    
    elif transform == 'R90':
        # 围绕指定点顺时针旋转90度
        new_left = center_x - (bottom - center_y)
        new_right = center_x - (top - center_y)
        new_top = center_y + (left - center_x)
        new_bottom = center_y + (right - center_x)
    
    elif transform == 'R180':
        # 围绕指定点旋转180度
        new_left = 2 * center_x - right
        new_right = 2 * center_x - left
        new_top = 2 * center_y - bottom
        new_bottom = 2 * center_y - top
    
    elif transform == 'R270':
        # 围绕指定点顺时针旋转270度
        new_left = center_x + (top - center_y)
        new_right = center_x + (bottom - center_y)
        new_top = center_y - (right - center_x)
        new_bottom = center_y - (left - center_x)
    
    elif transform == 'MY':
        # 围绕指定点沿Y轴镜像
        new_left = 2 * center_x - right
        new_right = 2 * center_x - left
        new_top, new_bottom = top, bottom
    
    elif transform == 'MY90':
        # 先沿Y轴镜像，再围绕指定点旋转90度
        temp_left = 2 * center_x - right
        temp_right = 2 * center_x - left
        temp_top, temp_bottom = top, bottom
        
        new_left = center_x - (temp_bottom - center_y)
        new_right = center_x - (temp_top - center_y)
        new_top = center_y + (temp_left - center_x)
        new_bottom = center_y + (temp_right - center_x)
    
    elif transform == 'MX':
        # 围绕指定点沿X轴镜像
        new_left, new_right = left, right
        new_top = 2 * center_y - bottom
        new_bottom = 2 * center_y - top
    
    elif transform == 'MXR90':
        # 先沿X轴镜像，再围绕指定点旋转90度
        temp_left, temp_right = left, right
        temp_top = 2 * center_y - bottom
        temp_bottom = 2 * center_y - top
        
        new_left = center_x - (temp_bottom - center_y)
        new_right = center_x - (temp_top - center_y)
        new_top = center_y + (temp_left - center_x)
        new_bottom = center_y + (temp_right - center_x)
    
    else:
        raise ValueError(f"不支持的变换类型: {transform}")
    
    return (round(new_left, 2), round(new_right, 2), 
            round(new_top, 2), round(new_bottom, 2))


def plot_transform(box, transform, center_point, ax=None):
    """绘制单个变换的结果"""
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 6))
    
    # 计算变换后的矩形
    transformed_box = rotate(box, transform, center_point)
    
    # 绘制原始矩形 (蓝色)
    left, right, top, bottom = box
    original_rect = patches.Rectangle(
        (left, top), 
        right - left, 
        bottom - top, 
        linewidth=2, 
        edgecolor='blue', 
        facecolor='blue', 
        alpha=0.3,
        label='原始矩形'
    )
    ax.add_patch(original_rect)
    
    # 绘制变换后的矩形 (红色)
    t_left, t_right, t_top, t_bottom = transformed_box
    transformed_rect = patches.Rectangle(
        (t_left, t_top), 
        t_right - t_left, 
        t_bottom - t_top, 
        linewidth=2, 
        edgecolor='red', 
        facecolor='red', 
        alpha=0.3,
        label='变换后矩形'
    )
    ax.add_patch(transformed_rect)
    
    # 标记中心点
    center_x, center_y = center_point
    ax.plot(center_x, center_y, 'go', markersize=8, label='旋转中心')
    
    # 设置图表属性
    ax.set_title(f'变换: {transform}', fontsize=14)
    ax.set_xlabel('X轴', fontsize=12)
    ax.set_ylabel('Y轴', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.legend()
    
    # 调整坐标轴范围，确保所有元素可见
    all_x = [left, right, t_left, t_right, center_x]
    all_y = [top, bottom, t_top, t_bottom, center_y]
    x_range = max(all_x) - min(all_x)
    y_range = max(all_y) - min(all_y)
    max_range = max(x_range, y_range) * 1.2  # 增加20%的边距
    
    ax.set_xlim(center_x - max_range/2, center_x + max_range/2)
    ax.set_ylim(center_y - max_range/2, center_y + max_range/2)
    ax.set_aspect('equal')
    
    return ax


if __name__ == "__main__":
    # 设置中文字体，确保中文正常显示

# %%
    # 测试用的矩形: left=0, right=2, top=0, bottom=1
# %%
    test_box = (-1, 4, 0, 3)
    # 旋转中心点 (选择矩形外部一点以便更好地观察旋转效果)
    center_point = (1, 1)
    
    # 所有变换类型
    transforms = ['R0', 'R90', 'R180', 'R270', 'MY', 'MY90', 'MX', 'MXR90']
    
    # 创建2x4的子图布局
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle(f'围绕点 {center_point} 的各种矩形变换', fontsize=16)
    
    # 为每个变换创建单独的图表
    for i, transform in enumerate(transforms):
        row = i // 4
        col = i % 4
        plot_transform(test_box, transform, center_point, axes[row, col])
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 调整布局，为标题留出空间
    plt.show()
