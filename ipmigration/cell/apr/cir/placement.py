import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

class Placement:
    def __init__(self, place_data):
        self.place_data = place_data
        self.parsed_data = self._parse_place_data()
    
    def _parse_place_data(self):
        parsed = []
        for idx, devices in enumerate(self.place_data):
            layer = {}
            # 处理PMOS器件
            if 'P' in devices and devices['P'] is not None:
                p_info, p_name = devices['P']
                p_source, p_gate, p_drain = p_info
                layer['P'] = {
                    'name': p_name,
                    'source': p_source,
                    'gate': p_gate,
                    'drain': p_drain
                }
            
            # 处理NMOS器件
            if 'N' in devices and devices['N'] is not None:
                n_info, n_name = devices['N']
                n_source, n_gate, n_drain = n_info
                layer['N'] = {
                    'name': n_name,
                    'source': n_source,
                    'gate': n_gate,
                    'drain': n_drain
                }
            
            parsed.append(layer)
        return parsed
    
    def detect_abutment(self):
        """检测当前Placement内部所有相邻器件是否都满足连接要求"""
        for i in range(len(self.parsed_data) - 1):
            current_layer = self.parsed_data[i]
            next_layer = self.parsed_data[i + 1]
            
            # 跳过空层
            if not current_layer or not next_layer:
                continue
            
            # 检查PMOS之间的连接
            if 'P' in current_layer and 'P' in next_layer:
                if current_layer['P']['drain'] != next_layer['P']['source']:
                    return False
            
            # 检查NMOS之间的连接
            if 'N' in current_layer and 'N' in next_layer:
                if current_layer['N']['drain'] != next_layer['N']['source']:
                    return False
        
        return True
    
    def print_abutment_result(self):
        """打印当前Placement内部的连接检测结果"""
        result = self.detect_abutment()
        if result:
            print("所有器件都满足相邻连接要求")
        else:
            print("存在不满足相邻连接要求的器件")
    
    @staticmethod
    def check_placement_abutment(placement1, placement2):
        """
        检查两个Placement是否可以连接
        
        参数:
            placement1: 第一个Placement实例
            placement2: 第二个Placement实例
            
        返回:
            如果不能连接，返回(False, None)
            如果只能placement1在前，返回(True, 0)
            如果只能placement2在前，返回(True, 1)
            如果两者都可以，返回(True, 2)
        """
        # 检查两种可能的连接方向
        can_p1_first = False
        can_p2_first = False
        
        # 检查placement1在前，placement2在后的情况
        if placement1.parsed_data and placement2.parsed_data:
            last_layer_p1 = placement1.parsed_data[-1]
            first_layer_p2 = placement2.parsed_data[0]
            
            match = True
            
            # 检查PMOS匹配
            if 'P' in last_layer_p1 and 'P' in first_layer_p2:
                if last_layer_p1['P']['drain'] != first_layer_p2['P']['source']:
                    match = False
            
            # 检查NMOS匹配
            if 'N' in last_layer_p1 and 'N' in first_layer_p2:
                if last_layer_p1['N']['drain'] != first_layer_p2['N']['source']:
                    match = False
            
            can_p1_first = match
        
        # 检查placement2在前，placement1在后的情况
        if placement1.parsed_data and placement2.parsed_data:
            last_layer_p2 = placement2.parsed_data[-1]
            first_layer_p1 = placement1.parsed_data[0]
            
            match = True
            
            # 检查PMOS匹配
            if 'P' in last_layer_p2 and 'P' in first_layer_p1:
                if last_layer_p2['P']['drain'] != first_layer_p1['P']['source']:
                    match = False
            
            # 检查NMOS匹配
            if 'N' in last_layer_p2 and 'N' in first_layer_p1:
                if last_layer_p2['N']['drain'] != first_layer_p1['N']['source']:
                    match = False
            
            can_p2_first = match
        
        # 确定返回结果
        if can_p1_first and can_p2_first:
            return (True, 2)  # 两者都可以
        elif can_p1_first:
            return (True, 0)  # 只能placement1在前
        elif can_p2_first:
            return (True, 1)  # 只能placement2在前
        else:
            return (False, None)  # 不能连接
    
    @staticmethod
    def merge_two_placements(placement1, placement2, preferred_order=None):
        """合并两个Placement实例"""
        # 检查是否可以连接
        can_abut, order = Placement.check_placement_abutment(placement1, placement2)
        
        # 处理双向都能连接的情况
        if can_abut and order == 2 and preferred_order is not None:
            order = preferred_order
        
        # 确定合并顺序
        if can_abut:
            if order == 1 or (order == 2 and preferred_order == 1):
                # placement2在前，placement1在后
                merged_data = placement2.place_data + placement1.place_data
            else:
                # placement1在前，placement2在后（默认情况）
                merged_data = placement1.place_data + placement2.place_data
        else:
            # 不能连接，添加一行分隔
            merged_data = placement1.place_data + [{'P': None, 'N': None}] + placement2.place_data
        
        return Placement(merged_data)
    
    @staticmethod
    def merge_placement_list(placement_list, preferred_orders=None):
        """
        合并一个Placement实例的列表
        
        参数:
            placement_list: Placement实例的列表
            preferred_orders: 可选，处理双向连接时的优先顺序列表
            
        返回:
            合并后的Placement实例
        """
        if not placement_list:
            return Placement([])
        
        # 从第一个元素开始逐步合并
        merged = placement_list[0]
        
        # 合并剩余的所有Placement
        for i in range(1, len(placement_list)):
            preferred_order = None
            if preferred_orders and i-1 < len(preferred_orders):
                preferred_order = preferred_orders[i-1]
            
            merged = Placement.merge_two_placements(merged, placement_list[i], preferred_order)
        
        return merged
    
    def print_structure(self):
        """打印布局结构，可以限制显示的层数"""
        print("Placement:")
        layers_to_print = self.parsed_data
        
        for i, layer in enumerate(layers_to_print):
            p_info = f"P:{layer['P']['name']}({layer['P']['source']}→{layer['P']['drain']})" if 'P' in layer else "P:None"
            n_info = f"N:{layer['N']['name']}({layer['N']['source']}→{layer['N']['drain']})" if 'N' in layer else "N:None"
            print(f"Column {i}: {p_info}, {n_info}")
    
    def get_layer_count(self):
        """返回布局的层数"""
        return len(self.parsed_data)


    def plot(self, figsize=(18, 10), title="Placement MOS Layout Visualization"):
        """
        绘制MOS器件布局：
        - 横向：按 Column 从左到右排列
        - 纵向：PMOS在上（y=1~2.2），NMOS在下（y=-2.2~-1）
        - 器件结构：source(左,红) → gate(中,蓝,稍长) → drain(右,红)
        - 标签：含器件名、source/gate/drain 的 Net 名
        """
        # 1. 初始化画布
        fig, ax = plt.subplots(figsize=figsize)
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)  
        
        # 2. 固定绘图参数（确保器件尺寸统一）
        col_total_width = 5.2    # 单个Column总宽度（source+gate+drain+间隙）
        col_spacing = 1.0        # Column之间的间距
        part_width = 2.0         # source/gate/drain 的基础宽度
        p_y_top = 2.2            # PMOS区域顶部y坐标
        p_y_bottom = 1.0         # PMOS区域底部y坐标
        n_y_top = -1.0           # NMOS区域顶部y坐标
        n_y_bottom = -2.2        # NMOS区域底部y坐标
        normal_height = 0.8      # source/drain 的高度
        gate_height = 1.2        # gate 的高度（比source/drain长0.4单位）
        
        # 3. 遍历每个Column绘制器件
        for col_idx, col in enumerate(self.parsed_data):
            # 计算当前Column的起始x坐标（左对齐）
            col_start_x = col_idx * (col_total_width + col_spacing)
            
            # ---------------------- 绘制PMOS（上区域） ----------------------
            if 'P' in col:
                p = col['P']
                # 计算PMOS各部分的x坐标（居中分布在Column内）
                p_source_x = col_start_x + 0.2
                p_gate_x = p_source_x + part_width + 0.1
                p_drain_x = p_gate_x + part_width + 0.1
                
                # 1. source（左，红色）
                p_source = FancyBboxPatch(
                    (p_source_x, p_y_bottom),  # 左下角坐标（垂直居中）
                    part_width, normal_height,
                    boxstyle="round,pad=0.05",  # 圆角优化视觉效果
                    facecolor='#ff4444', alpha=0.8,  # 浅红色（半透明）
                    edgecolor='black', linewidth=1.5
                )
                
                # 2. gate（中，蓝色，稍长）
                p_gate = FancyBboxPatch(
                    (p_gate_x, p_y_bottom - 0.2),  # 上下延伸0.2单位
                    part_width, gate_height,
                    boxstyle="round,pad=0.05",
                    facecolor='#2288ff', alpha=0.9,  # 亮蓝色
                    edgecolor='black', linewidth=1.5
                )
                
                # 3. drain（右，红色）
                p_drain = FancyBboxPatch(
                    (p_drain_x, p_y_bottom),
                    part_width, normal_height,
                    boxstyle="round,pad=0.05",
                    facecolor='#ff4444', alpha=0.8,
                    edgecolor='black', linewidth=1.5
                )
                
                # 添加PMOS器件到画布
                ax.add_patch(p_source)
                ax.add_patch(p_gate)
                ax.add_patch(p_drain)
                
                # 添加PMOS标签（白色文字，突出显示）
                # 器件名（gate上方）
                ax.text(
                    p_gate_x + part_width/2, p_y_top + 0.1,
                    f"PMOS: {p['name']}",
                    ha='center', va='bottom', fontsize=11, fontweight='bold'
                )
                # source Net名（source中心）
                ax.text(
                    p_source_x + part_width/2, p_y_bottom + normal_height/2 -0.2,
                    p['source'],
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold'
                )
                # gate Net名（gate中心）
                ax.text(
                    p_gate_x + part_width/2, p_y_bottom + gate_height/2,
                    p['gate'],
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold'
                )
                # drain Net名（drain中心）
                ax.text(
                    p_drain_x + part_width/2, p_y_bottom + normal_height/2 - 0.2,
                    p['drain'],
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold'
                )
            
            # ---------------------- 绘制NMOS（下区域） ----------------------
            if 'N' in col:
                n = col['N']
                # 计算NMOS各部分的x坐标（与PMOS对齐）
                n_source_x = col_start_x + 0.2
                n_gate_x = n_source_x + part_width + 0.1
                n_drain_x = n_gate_x + part_width + 0.1
                
                # 1. source（左，红色）
                n_source = FancyBboxPatch(
                    (n_source_x, n_y_top - normal_height),  # 垂直居中（NMOS区域）
                    part_width, normal_height,
                    boxstyle="round,pad=0.05",
                    facecolor='#ff4444', alpha=0.8,
                    edgecolor='black', linewidth=1.5
                )
                
                # 2. gate（中，蓝色，稍长）
                n_gate = FancyBboxPatch(
                    (n_gate_x, n_y_top - gate_height + 0.2),  # 上下延伸0.2单位
                    part_width, gate_height,
                    boxstyle="round,pad=0.05",
                    facecolor='#2288ff', alpha=0.9,
                    edgecolor='black', linewidth=1.5
                )
                
                # 3. drain（右，红色）
                n_drain = FancyBboxPatch(
                    (n_drain_x, n_y_top - normal_height),
                    part_width, normal_height,
                    boxstyle="round,pad=0.05",
                    facecolor='#ff4444', alpha=0.8,
                    edgecolor='black', linewidth=1.5
                )
                
                # 添加NMOS器件到画布
                ax.add_patch(n_source)
                ax.add_patch(n_gate)
                ax.add_patch(n_drain)
                
                # 添加NMOS标签（白色文字）
                # 器件名（gate下方）
                ax.text(
                    n_gate_x + part_width/2, n_y_bottom - 0.1,
                    f"NMOS: {n['name']}",
                    ha='center', va='top', fontsize=11, fontweight='bold'
                )
                # source Net名（source中心）
                ax.text(
                    n_source_x + part_width/2, n_y_top - normal_height/2 + 0.2,
                    n['source'],
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold'
                )
                # gate Net名（gate中心）
                ax.text(
                    n_gate_x + part_width/2, n_y_top - gate_height/2,
                    n['gate'],
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold'
                )
                # drain Net名（drain中心）
                ax.text(
                    n_drain_x + part_width/2, n_y_top - normal_height/2 + 0.2,
                    n['drain'],
                    ha='center', va='center', fontsize=10, color='white', fontweight='bold'
                )
            

        
        # 4. 优化画布样式
        # 设置坐标轴范围（留出边距）
        total_x_range = len(self.parsed_data) * (col_total_width + col_spacing) - col_spacing + 2
        ax.set_xlim(-0.5, total_x_range)
        ax.set_ylim(-3.0, 3.0)
        
        # 添加水平分隔线（区分PMOS和NMOS区域）
        ax.axhline(y=0, color='black', linestyle='--', linewidth=1.5, alpha=0.7, label='上下区域分隔线')
        
        # 添加图例
        legend_elements = [
            patches.Patch(color='#ff4444', alpha=0.8, label='Source / Drain'),
            patches.Patch(color='#2288ff', alpha=0.9, label='Gate'),
        ]
        ax.legend(handles=legend_elements, fontsize=12, loc='upper right')
        
        # 添加网格（便于对齐查看）
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        
        # 调整布局（避免标签被截断）
        plt.tight_layout()
        # 显示图像
        plt.show()


# 示例用法
if __name__ == "__main__":
    # 准备测试数据 - 修复元组格式，添加引号
    data1 = [
        {'P': (('N_4', 'CKN', 'VDD'), 'M19'), 'N': (('N_4', 'CKN', 'VSS'), 'M1')},
        {'P': (('VDD', 'N_4', 'N_5'), 'M20'), 'N': (('VSS', 'N_4', 'N_5'), 'M2')}
    ]
    
    data2 = [
        {'P': (('N_10', 'RN', 'VDD'), 'M33'), 'N': (('N_10', 'RN', 'VSS'), 'M15')}
    ]
    
    data3 = [
        {'P': (('VDD', 'N_9', 'QN'), 'M36'), 'N': (('VSS', 'N_9', 'QN'), 'M18')}
    ]
    
    data4 = [
        {'P': (('Q', 'N_11', 'VDD'), 'M35'), 'N': (('Q', 'N_11', 'VSS'), 'M17')}
    ]
    
    data5 = [
        {'P': (('VDD', 'N_9', 'N_11'), 'M34'), 'N': (('VSS', 'N_9', 'N_11'), 'M16')}
    ]
    
    data6 = [
        {'P': (('VDD', 'D', 'N_21'), 'M21'), 'N': (('VSS', 'D', 'N_14'), 'M3')},
        {'P': (('N_21', 'N_4', 'N_6'), 'M23'), 'N': (('N_14', 'N_5', 'N_6'), 'M4')},
        {'P': (('N_6', 'N_5', 'N_22'), 'M22'), 'N': (('N_6', 'N_4', 'N_15'), 'M5')},
        {'P': (('N_22', 'N_7', 'VDD'), 'M24'), 'N': (('N_15', 'N_7', 'VSS'), 'M6')}
    ]
    
    data7 = [
        {'P': (('VDD', 'N_6', 'N_23'), 'M25'), 'N': (('VSS', 'N_6', 'N_7'), 'M7')},
        {'P': (('N_23', 'N_10', 'N_7'), 'M26'), 'N': (('N_7', 'N_10', 'VSS'), 'M8')}
    ]
    
    data8 = [
        {'P': (('VDD', 'N_7', 'N_24'), 'M27'), 'N': (('VSS', 'N_7', 'N_16'), 'M9')},
        {'P': (('N_24', 'N_5', 'N_8'), 'M28'), 'N': (('N_16', 'N_4', 'N_8'), 'M10')},
        {'P': (('N_8', 'N_4', 'N_25'), 'M29'), 'N': (('N_8', 'N_5', 'N_17'), 'M11')},
        {'P': (('N_25', 'N_9', 'VDD'), 'M30'), 'N': (('N_17', 'N_9', 'VSS'), 'M12')}
    ]
    
    data9 = [
        {'P': (('VDD', 'N_8', 'N_26'), 'M31'), 'N': (('VSS', 'N_8', 'N_9'), 'M13')},
        {'P': (('N_26', 'N_10', 'N_9'), 'M32'), 'N': (('N_9', 'N_10', 'VSS'), 'M14')}
    ]
    
    # 创建Placement实例列表
    placements = [
        Placement(data1),
        Placement(data2),
        Placement(data3),
        Placement(data4),
        Placement(data5),
        Placement(data6),
        Placement(data7),
        Placement(data8),
        Placement(data9)
    ]
    
    # 打印每个Placement的信息
    print("=== 原始Placement列表 ===")
    for i, placement in enumerate(placements):
        print(f"\nPlacement {i+1}: {placement.get_layer_count()} 层")
        placement.print_structure() 
    
    # 合并所有Placement
    print("\n=== 开始合并所有Placement ===")
    merged = Placement.merge_placement_list(placements)
    
    # 显示合并结果
    print("\n=== 合并结果 ===")
    print(f"总层数: {merged.get_layer_count()}")
    merged.print_structure()  # 显示前10层
    
    # 检查合并后的连接情况
    print("\n=== 合并后的连接检查 ===")
    merged.print_abutment_result()
    # 6. 可视化合并后的布局（核心功能）
    print("\n=== 正在生成可视化图像... ===")
    merged.plot(
        figsize=(20, 10),
        title="Placement"
    )