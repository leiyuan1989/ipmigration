import networkx as nx













class DependencySolver:
    def __init__(self):
        self.devices = {}
        self.dependency_graph = nx.DiGraph()
        self.all_coordinates = set()
    
    def add_device(self, device_name, coordinates):
        """
        添加器件及其坐标
        coordinates是一个字典: {坐标名: 依赖表达式或None}
        表达式格式示例: "B.b1 + 5" 表示依赖于B器件的b1坐标加5
        """
        self.devices[device_name] = coordinates
        
        # 添加坐标节点
        for coord in coordinates:
            full_coord = f"{device_name}.{coord}"
            self.all_coordinates.add(full_coord)
            self.dependency_graph.add_node(full_coord)
        
        # 解析依赖关系
        for coord, expr in coordinates.items():
            if expr is not None:
                full_coord = f"{device_name}.{coord}"
                # 提取依赖的其他坐标（简单解析，实际可能需要更复杂的表达式解析）
                for dep_device in self.devices:
                    for dep_coord in self.devices[dep_device]:
                        dep_full_coord = f"{dep_device}.{dep_coord}"
                        if dep_full_coord in expr:
                            self.dependency_graph.add_edge(dep_full_coord, full_coord)
    
    
    
    
    
    
    
    
    def check_cycles(self):
        """检查是否存在循环依赖"""
        try:
            cycles = list(nx.simple_cycles(self.dependency_graph))
            if cycles:
                print("发现循环依赖:")
                for cycle in cycles:
                    print(" -> ".join(cycle))
                return True
            return False
        except nx.NetworkXNoCycle:
            return False
    
    def get_build_order(self):
        """获取器件的建立顺序"""
        # 首先获取坐标的拓扑排序
        try:
            coord_order = list(nx.topological_sort(self.dependency_graph))
        except nx.NetworkXUnfeasible:
            print("存在循环依赖，无法确定建立顺序")
            return None
        
        # 根据坐标顺序确定器件建立顺序
        built_coords = set()
        build_order = []
        built_devices = set()
        
        for coord in coord_order:
            device = coord.split('.')[0]
            # 检查该器件是否所有坐标都已可用
            if device not in built_devices:
                all_coords_available = True
                for c in self.devices[device]:
                    if f"{device}.{c}" not in built_coords:
                        all_coords_available = False
                        break
                
                if all_coords_available:
                    build_order.append(device)
                    built_devices.add(device)
            
            built_coords.add(coord)
        
        # 检查是否有未被建立的器件
        for device in self.devices:
            if device not in built_devices:
                print(f"警告: 器件 {device} 无法被建立，存在未解决的依赖")
        
        return build_order
    
    def verify_realizable(self, build_order):
        """使用Z3验证坐标是否可被实数化"""
        if not build_order:
            return False
            
        solver = Solver()
        coord_vars = {}
        
        # 为所有坐标创建实数变量
        for coord in self.all_coordinates:
            coord_vars[coord] = Real(coord)
        
        # 添加约束
        for device in build_order:
            for coord, expr in self.devices[device].items():
                full_coord = f"{device}.{coord}"
                if expr is None:
                    # 没有依赖，可以是任意实数
                    continue
                else:
                    # 替换表达式中的坐标为Z3变量
                    z3_expr = expr
                    for c in coord_vars:
                        z3_expr = z3_expr.replace(c, f"coord_vars['{c}']")
                    
                    # 添加约束: 当前坐标 = 表达式结果
                    constraint = (coord_vars[full_coord] == eval(z3_expr))
                    solver.add(constraint)
        
        # 检查是否有解
        if solver.check() == sat:
            print("所有坐标可以被实数化")
            model = solver.model()
            print("坐标值:")
            for coord in sorted(coord_vars.keys()):
                print(f"{coord}: {model.eval(coord_vars[coord])}")
            return True
        else:
            print("无法将所有坐标实数化，不存在可行解")
            return False


# 使用示例
if __name__ == "__main__":
    solver = DeviceDependencySolver()
    
    # 添加器件及其坐标依赖
    solver.add_device("B", {
        "b1": None,  # 不依赖任何坐标
        "b2": None
    })
    
    solver.add_device("C", {
        "c1": None,
        "c2": "B.b1 * 2"  # 依赖B的b1坐标
    })
    
    solver.add_device("A", {
        "a1": "B.b1 + 5",   # 依赖B的b1坐标
        "a2": "C.c1 - 3"    # 依赖C的c1坐标
    })
    
    solver.add_device("D", {
        "d1": "A.a1 + C.c2",  # 依赖A的a1和C的c2坐标
        "d2": "B.b2 - 10"
    })
    
    # 检查循环依赖
    if not solver.check_cycles():
        # 获取建立顺序
        build_order = solver.get_build_order()
        print("\n器件建立顺序:", build_order)
        
        # 验证是否可实数化
        solver.verify_realizable(build_order)
