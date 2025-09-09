;; 导出Layout中所有图形到TXT文件的SKILL程序
;; 使用方法：在Cadence Virtuoso中加载并运行，指定要导出的层次和输出文件路径

procedure(exportAllShapesToTxt(cellViewName outputFilePath)
    ;; 定义变量
    cv = nil
    shapes = nil
    shapeFile = nil
    layerTable = nil
    layerName = ""
    shapeType = ""
    shapeBounds = nil
    i = 0
    
    ;; 尝试打开指定的cellView
    cv = dbOpenCellViewByType(ddGetObj("libName") cellViewName "layout" "" "r")
    if(cv == nil
        then
        printf("无法打开cellView: %s\n" cellViewName)
        return(nil)
    )
    
    ;; 打开输出文件
    shapeFile = outfile(outputFilePath)
    if(shapeFile == nil
        then
        printf("无法创建输出文件: %s\n" outputFilePath)
        dbCloseCellView(cv)
        return(nil)
    )
    
    ;; 写入文件头信息
    fprintf(shapeFile "Layout Shapes Export - %s\n" cellViewName)
    fprintf(shapeFile "导出时间: %s\n" (formatTime (getCurrentTime) "%Y-%m-%d %H:%M:%S"))
    fprintf(shapeFile "========================================================================\n")
    fprintf(shapeFile "序号\t层次名称\t层次编号\t图形类型\t坐标信息\n")
    fprintf(shapeFile "========================================================================\n")
    
    ;; 获取所有层次表
    layerTable = ddGetLayerTable()
    
    ;; 获取所有图形
    shapes = geGetAllShapes(cv)
    
    ;; 遍历所有图形并写入文件
    when(shapes
        foreach(shape shapes
            i = i + 1
            
            ;; 获取层次信息
            layerName = dbGetAttr(ddGetLayerName(layerTable shape~>layerId) "name")
            
            ;; 确定图形类型
            shapeType = caseq(shape~>type
                dbBoxType       "矩形 (Box)"
                dbPathType      "路径 (Path)"
                dbInstType      "实例 (Instance)"
                dbTextType      "文本 (Text)"
                dbOvalType      "椭圆 (Oval)"
                dbPolygonType   "多边形 (Polygon)"
                dbLabelType     "标签 (Label)"
                t               "未知类型 (Unknown)"
            )
            
            ;; 获取坐标信息
            shapeBounds = dbGetAttr(shape "bBox")
            
            ;; 写入图形信息到文件
            fprintf(shapeFile "%d\t%s\t%d\t%s\t" 
                i 
                layerName 
                shape~>layerId 
                shapeType
            )
            
            ;; 根据不同图形类型输出具体坐标
            caseq(shape~>type
                dbBoxType
                    fprintf(shapeFile "左下:(%d,%d) 右上:(%d,%d)\n" 
                        shapeBounds~>x1 shapeBounds~>y1 
                        shapeBounds~>x2 shapeBounds~>y2
                    )
                
                dbPolygonType
                    fprintf(shapeFile "顶点数:%d 坐标:%L\n" 
                        length(shape~>points) 
                        shape~>points
                    )
                
                dbPathType
                    fprintf(shapeFile "宽度:%d 路径点:%L\n" 
                        shape~>width 
                        shape~>points
                    )
                
                dbTextType
                    fprintf(shapeFile "位置:(%d,%d) 内容:\"%s\" 角度:%d\n" 
                        shape~>x shape~>y 
                        shape~>text 
                        shape~>angle
                    )
                
                dbOvalType
                    fprintf(shapeFile "中心:(%d,%d) 半径X:%d 半径Y:%d\n" 
                        shape~>x shape~>y 
                        shape~>rx shape~>ry
                    )
                
                t
                    fprintf(shapeFile "边界:左下:(%d,%d) 右上:(%d,%d)\n" 
                        shapeBounds~>x1 shapeBounds~>y1 
                        shapeBounds~>x2 shapeBounds~>y2
                    )
            )
        )
    )
    
    ;; 完成处理
    fprintf(shapeFile "========================================================================\n")
    fprintf(shapeFile "总计导出 %d 个图形\n" i)
    close(shapeFile)
    dbCloseCellView(cv)
    
    printf("成功导出 %d 个图形到文件: %s\n" i outputFilePath)
    return(t)
)

;; 使用示例
;; 请替换以下参数为实际的cellView名称和输出文件路径
;; exportAllShapesToTxt("your_cell_name" "/path/to/your/output/shapes.txt")

;; 交互式输入版本
procedure(exportShapesInteractive()
    let( (cellName filePath)
        cellName = getString("请输入要导出的Cell名称: ")
        if(cellName == ""
            then
            printf("未输入Cell名称，操作取消\n")
            return(nil)
        )
        
        filePath = getString("请输入输出文件路径(例如: /tmp/shapes.txt): ")
        if(filePath == ""
            then
            printf("未输入文件路径，操作取消\n")
            return(nil)
        )
        
        exportAllShapesToTxt(cellName filePath)
    )
)

;; 运行交互式版本
exportShapesInteractive()
    