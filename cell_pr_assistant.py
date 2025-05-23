import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QGraphicsView, 
                             QGraphicsRectItem, QGraphicsLineItem, QMenu, QAction, 
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, 
                             QPushButton, QComboBox, QFileDialog,QGraphicsTextItem)
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPointF

class GridPoint(QGraphicsRectItem):
    def __init__(self, x, y, size=30):
        super().__init__(x - size/2, y - size/2, size, size)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        self.setBrush(QBrush(Qt.lightGray))
        self.setPen(QPen(Qt.black, 1))
        self.type = "NA"  # NA, CT-AA, CT-GT, GT-AA
        
        # 添加标签文本项
        self.scene = self.scene()
        self.label = QGraphicsTextItem(self)
        self.label.setPos(x, y - 10)  # 调整标签位置
        self.label.setDefaultTextColor(Qt.black)
        self.label.setPlainText("")
        
    def set_type(self, node_type):
        self.type = node_type
        if node_type == "CT-AA":
            self.setBrush(QBrush(Qt.red))
        elif node_type == "CT-GT":
            self.setBrush(QBrush(Qt.green))
        elif node_type == "GT-AA":
            self.setBrush(QBrush(QColor(128, 0, 128)))  # 紫色
        else:  # NA
            self.setBrush(QBrush(Qt.lightGray))
            
        # 更新标签样式
        if node_type != "NA":
            self.label.setDefaultTextColor(Qt.white)
        else:
            self.label.setDefaultTextColor(Qt.black)
    
    def set_label(self, text):
        """设置网格点的标签文本"""
        self.label.setPlainText(text)

class Connection(QGraphicsLineItem):
    def __init__(self, start_x, start_y, end_x, end_y):
        super().__init__(start_x, start_y, end_x, end_y)
        self.type = "NA"  # NA, M1, GT
        self.setPen(QPen(Qt.lightGray, 5))
        
    def set_type(self, conn_type):
        self.type = conn_type
        if conn_type == "M1":
            self.setPen(QPen(Qt.darkGreen, 10))
        elif conn_type == "GT":
            self.setPen(QPen(Qt.blue, 10))
        else:  # NA
            self.setPen(QPen(Qt.lightGray, 5))

class RouteScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = (5, 5)
        self.cell_size = 150
        self.edge_size = 30
        self.node_size = 40
        
        self.grid_points = {}  # 存储网格点坐标和对象
        self.grid_points_loc = {}
        self.connections = []  # 存储所有网格边
        self.current_node_type = "NA"
        self.current_conn_type = "NA"
        
    def set_grid_size(self, rows, cols):
        self.grid_size = (rows, cols)
        self.clear()
        self.create_grid()
        
    def create_grid(self):
        rows, cols = self.grid_size
        # 创建网格点
        node_pos = {}
        for y in range(rows):
            for x in range(cols):
                pos_x = x * self.cell_size + self.edge_size
                pos_y = y * self.cell_size + self.edge_size
                point = GridPoint(pos_x, pos_y, self.node_size)
                self.addItem(point)
                self.grid_points[(x, y)] = point
                # 设置标签文本（例如坐标）
                point.set_label(f"{x},{y}")  # 使用坐标作为标签
                node_pos[(x,y)]=(pos_x,pos_y)
                
        # 创建水平连线
        for y in range(rows):
            for x in range(cols - 1):
                start_x = node_pos[(x,y)][0] + int(0.5*self.node_size)
                start_y = node_pos[(x,y)][1] 
                end_x =  node_pos[(x+1,y)][0] - int(0.5*self.node_size)
                end_y =  node_pos[(x,y)][1] 
                conn = Connection(start_x, start_y, end_x, end_y)
                self.addItem(conn)
                self.connections.append(conn)
                
        # 创建垂直连线
        for y in range(rows - 1):
            for x in range(cols):
                start_x = node_pos[(x,y)][0] 
                start_y = node_pos[(x,y)][1] + int(0.5*self.node_size)
                end_x   = node_pos[(x,y)][0]
                end_y   = node_pos[(x,y+1)][1] - int(0.5*self.node_size)
                conn = Connection(start_x, start_y, end_x, end_y)
                self.addItem(conn)
                self.connections.append(conn)
    
    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if item:
            if isinstance(item, GridPoint):
                # 设置节点类型
                item.set_type(self.current_node_type)
            elif isinstance(item, Connection):
                # 设置连线类型
                item.set_type(self.current_conn_type)
                
        super().mousePressEvent(event)
    
    def set_node_type(self, node_type):
        self.current_node_type = node_type
        
    def set_conn_type(self, conn_type):
        self.current_conn_type = conn_type
        
    def export_to_dict(self):
        """将当前网格状态导出为字典"""
        data = {
            "grid_size": self.grid_size,
            "nodes": {},
            "connections": []
        }
        
        # 保存节点状态
        for pos, point in self.grid_points.items():
            x, y = pos
            data["nodes"][f"{x},{y}"] = point.type
            
        # 保存连线状态
        for conn in self.connections:
            start_x, start_y = conn.line().p1().x(), conn.line().p1().y()
            end_x, end_y = conn.line().p2().x(), conn.line().p2().y()
            conn_data = {
                "start": (start_x, start_y),
                "end": (end_x, end_y),
                "type": conn.type
            }
            data["connections"].append(conn_data)
            
        return data
        
    def import_from_dict(self, data):
        """从字典导入网格状态"""
        self.clear()
        self.grid_size = data.get("grid_size", (5, 5))
        self.create_grid()
        
        # 恢复节点状态
        for pos_str, node_type in data.get("nodes", {}).items():
            x, y = map(int, pos_str.split(","))
            if (x, y) in self.grid_points:
                self.grid_points[(x, y)].set_type(node_type)
                
        # 恢复连线状态
        for conn_data in data.get("connections", []):
            start_x, start_y = conn_data["start"]
            end_x, end_y = conn_data["end"]
            conn_type = conn_data["type"]
            
            # 查找匹配的连线对象
            for conn in self.connections:
                line = conn.line()
                if (abs(line.p1().x() - start_x) < 1 and 
                    abs(line.p1().y() - start_y) < 1 and 
                    abs(line.p2().x() - end_x) < 1 and 
                    abs(line.p2().y() - end_y) < 1):
                    conn.set_type(conn_type)
                    # break

class GridSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置网格大小")
        layout = QVBoxLayout()
        
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel("行数:"))
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(2, 20)
        self.rows_spin.setValue(5)
        row_layout.addWidget(self.rows_spin)
        layout.addLayout(row_layout)
        
        col_layout = QHBoxLayout()
        col_layout.addWidget(QLabel("列数:"))
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(2, 20)
        self.cols_spin.setValue(5)
        col_layout.addWidget(self.cols_spin)
        layout.addLayout(col_layout)
        
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)

    def get_grid_size(self):
        return self.rows_spin.value(), self.cols_spin.value()

class RouteEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.scene = RouteScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.setWindowTitle("网格编辑器")
        self.resize(800, 600)
        self.create_menu()
        self.create_toolbar()
        self.scene.create_grid()
        
    def create_menu(self):
        file_menu = self.menuBar().addMenu("文件")
        
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_grid)
        file_menu.addAction(save_action)
        
        load_action = QAction("打开", self)
        load_action.triggered.connect(self.load_grid)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        grid_menu = self.menuBar().addMenu("网格")
        grid_size_action = QAction("设置网格大小", self)
        grid_size_action.triggered.connect(self.set_grid_size)
        grid_menu.addAction(grid_size_action)
        
    def create_toolbar(self):
        toolbar = self.addToolBar("工具栏")
        
        # 节点类型选择
        node_type_label = QLabel("节点类型:")
        toolbar.addWidget(node_type_label)
        
        node_type_combo = QComboBox()
        node_type_combo.addItems(["NA", "CT-AA", "CT-GT", "GT-AA"])
        node_type_combo.currentTextChanged.connect(self.scene.set_node_type)
        toolbar.addWidget(node_type_combo)
        
        toolbar.addSeparator()
        
        # 连线类型选择
        conn_type_label = QLabel("连线类型:")
        toolbar.addWidget(conn_type_label)
        
        conn_type_combo = QComboBox()
        conn_type_combo.addItems(["NA", "M1", "GT"])
        conn_type_combo.currentTextChanged.connect(self.scene.set_conn_type)
        toolbar.addWidget(conn_type_combo)
        
    def set_grid_size(self):
        dialog = GridSizeDialog(self)
        if dialog.exec_():
            rows, cols = dialog.get_grid_size()
            self.scene.set_grid_size(rows, cols)
            
    def save_grid(self):
        """保存网格到JSON文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存网格", "", "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            try:
                data = self.scene.export_to_dict()
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2)
                print(f"网格已保存到: {file_path}")
            except Exception as e:
                print(f"保存失败: {e}")
                
    def load_grid(self):
        """从JSON文件加载网格"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开网格", "", "JSON文件 (*.json);;所有文件 (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                self.scene.import_from_dict(data)
                print(f"已从 {file_path} 加载网格")
            except Exception as e:
                print(f"加载失败: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = RouteEditor()
    editor.show()
    sys.exit(app.exec_())