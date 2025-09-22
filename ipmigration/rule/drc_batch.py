import os


def generate_drc_shell_script(drc_files, script_path="run_drc.sh"):
    """
    生成执行所有DRC检查的shell脚本
    
    参数:
        drc_files: DRC文件路径列表
        script_path: 生成的shell脚本路径，默认是"run_drc.sh"
        
    返回:
        str: 生成的shell脚本路径
    """
    # 构建脚本内容
    script_content = "#!/bin/bash\n\n"

    script_content += "#for \\r error : sed -i 's/\\r//' run_drc.sh\n\n "
    
    for drc_file in drc_files:
        log_file ="drc_bath_log.txt"
        
        # 添加命令：执行calibre并将输出重定向到日志文件
        script_content += f"calibre -drc {drc_file} &> {log_file}\n"
        
        # 添加检查命令执行结果的逻辑
        script_content += "if [ $? -eq 0 ]; then\n"
        script_content += f"    echo \"DRC check completed successfully for {drc_file}\"\n"
        script_content += "else\n"
        script_content += f"    echo \"Error occurred during DRC check for {drc_file}\"\n"
        script_content += "fi\n\n"
    
    # 添加完成提示
    script_content += "echo \"All DRC checks have been processed\"\n"
    
    # 写入脚本文件
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # 赋予脚本可执行权限
    os.chmod(script_path, 0o755)
    
    return script_path

def generate_drc_rule_file(template_path, output_path, layout_path, layout_primary, 
                          drc_result_database, drc_summary_report):
    """
    生成修改关键参数后的DRC规则文档
    
    参数说明：
    - template_path: 原始Calibre模板
    - output_path: 新生成文档的保存路径
    - layout_path: 替换 LAYOUT PATH 后的GDS文件路径（需包含文件名，如"new_cell.gds"）
    - layout_primary: 替换 LAYOUT PRIMARY 后的主单元名（如"TOP_CELL"）
    - drc_result_database: 替换 DRC RESULTS DATABASE 后的数据库路径（需包含文件名，如"new_db.db"）
    - drc_summary_report: 替换 DRC SUMMARY REPORT 后的报告路径（需包含文件名，如"new_summary.txt"）
    """
    # 读取模板文件内容
    try:
        with open(template_path, 'r', encoding='utf-8') as template_file:
            template_content = template_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"模板文件未找到：{template_path}")
    except Exception as e:
        raise Exception(f"读取模板文件失败：{str(e)}")
    
    # 定义需要修改的行标识及对应替换规则
    modify_rules = [
        # 匹配 LAYOUT PATH 行，替换引号内内容
        {
            "flag": "LAYOUT PATH ",
            "replace_func": lambda line: f'LAYOUT PATH "{layout_path}"\n'
        },
        # 匹配 LAYOUT PRIMARY 行，替换引号内内容
        {
            "flag": "LAYOUT PRIMARY ",
            "replace_func": lambda line: f'LAYOUT PRIMARY "{layout_primary}"\n'
        },
        # 匹配 DRC RESULTS DATABASE 行，替换引号内内容（保留ASCII关键字）
        {
            "flag": "DRC RESULTS DATABASE ",
            "replace_func": lambda line: f'DRC RESULTS DATABASE "{drc_result_database}" ASCII\n'
        },
        # 匹配 DRC SUMMARY REPORT 行，替换引号内内容（保留REPLACE HIER关键字）
        {
            "flag": "DRC SUMMARY REPORT ",
            "replace_func": lambda line: f'DRC SUMMARY REPORT "{drc_summary_report}" REPLACE HIER\n'
        }
    ]
    
    # 逐行处理模板内容，修改目标行
    new_content = []
    for line in template_content:
        # 标记是否已匹配并修改当前行
        modified = False
        for rule in modify_rules:
            # 检查当前行是否包含目标标识（忽略行首空格，确保匹配）
            stripped_line = line.strip()
            if stripped_line.startswith(rule["flag"]):
                # 应用替换规则
                new_line = rule["replace_func"](line)
                new_content.append(new_line)
                modified = True
                break
        # 未匹配到修改规则的行，保持原样
        if not modified:
            new_content.append(line)
    
    # 将修改后的内容写入新文件
    try:
        with open(output_path, 'w', encoding='utf-8') as output_file:
            output_file.writelines(new_content)
        print(f"DRC files generated：{output_path}")
    except Exception as e:
        raise Exception(f"写入新文件失败：{str(e)}")


def batch_drc_check(template_path, output_dir, layout_path, cell_names):
    """
    批量处理DRC检查
    
    参数:
        template_path: DRC规则模板文件路径
        output_dir: 输出文件存放目录
        layout_path: GDS布局文件路径
        cell_names: 要处理的cell名称列表
        
    返回:
        list: 所有生成的DRC总结报告文件路径集合
    """
    # 确保输出目录以斜杠结尾，处理不同操作系统路径格式
    if not output_dir.endswith(('/')):
        output_dir += '/'
    
    
    drc_files = []
    summary_reports = []
    
    # 循环处理每个cell
    for cell_name in cell_names:
        # 生成各个输出文件的路径
        drc_output_path = f"{output_dir}{cell_name}.drc"
        drc_database = f"{output_dir}drc_result.db"
        drc_summary = f"{output_dir}{cell_name}.summary"
        
        # 调用DRC规则文件生成函数
        generate_drc_rule_file(
            template_path=template_path,
            output_path=drc_output_path,
            layout_path=layout_path,
            layout_primary=cell_name,
            drc_result_database=drc_database,
            drc_summary_report=drc_summary
        )
        
        drc_files.append(drc_output_path)
        summary_reports.append(drc_summary)
    
    return drc_files,summary_reports




def extract_drc_info(log_file_path):
    """
    从DRC检查日志文件中提取关键信息（含非零结果规则的数量）
    
    参数:
        log_file_path: DRC日志文件的完整路径（如./drc_bath_log.txt）
        
    返回:
        dict: 包含三类关键信息的字典，格式如下：
            {
                "total_rule_checks_executed": int,  # TOTAL DRC RuleChecks Executed的数量
                "total_drc_results_generated": int, # TOTAL DRC Results Generated的数量
                "non_zero_result_rules": list      # 所有TOTAL Result Count≠0的规则（含数量），元素为元组(规则名, 结果数)
            }
    
    异常:
        FileNotFoundError: 若输入的日志文件路径不存在，会抛出此异常
    """
    # 初始化返回数据
    drc_info = {
        "total_rule_checks_executed": 0,
        "total_drc_results_generated": 0,
        "non_zero_result_rules": []  # 元素格式：(rule_name, result_count)
    }
    
    # 打开并读取日志文件（支持UTF-8编码，兼容Linux生成的日志）
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()  # 去除每行首尾的空格、换行符
            
            # 1. 提取TOTAL DRC RuleChecks Executed
            if line.startswith("TOTAL DRC RuleChecks Executed:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    drc_info["total_rule_checks_executed"] = int(parts[1].strip())
            
            # 2. 提取TOTAL DRC Results Generated
            elif line.startswith("TOTAL DRC Results Generated:"):
                parts = line.split(":")
                if len(parts) >= 2:
                    drc_info["total_drc_results_generated"] = int(parts[1].strip())
            
            # 3. 提取TOTAL Result Count≠0的规则名和对应数量
            elif line.startswith("RULECHECK") and "TOTAL Result Count = " in line:
                # 分割行内容，示例行：RULECHECK Convention_FLT_NW ....... TOTAL Result Count = 1
                line_parts = line.split()
                # 规则名："RULECHECK"后的第一个元素（如Convention_FLT_NW）
                rule_name = line_parts[1]
                # 找到"= "后的数字（结果数）：先定位"TOTAL Result Count = "的位置，再取后续数字
                count_index = line_parts.index("=") + 1  # "="的下一个元素就是数字
                try:
                    result_count = int(line_parts[count_index])
                    # 仅保留结果数非零的规则
                    if result_count != 0:
                        drc_info["non_zero_result_rules"].append((rule_name, result_count))
                except (ValueError, IndexError):
                    # 若数字解析失败或索引异常，跳过该行
                    continue
    
    return drc_info


# ------------------- 使用示例 -------------------



# 使用示例
if __name__ == "__main__":
    # 配置输入参数
    template_file_path = "c153_template.txt"  # 模板文件路径
    output_directory = "./"       # 输出目录
    layout_file_path = "../c153/7T/gds/csmc0153.gds"  # GDS文件路径
    cells_to_process = ["dfcfb1", "dfcfb2", "dfcfb3", "dfcfb4"]  # 要处理的cell列表
    
    # 执行批量DRC检查
    drc_files,summary_reports = batch_drc_check(
        template_path=template_file_path,
        output_dir=output_directory,
        layout_path=layout_file_path,
        cell_names=cells_to_process
    )
    
    script = generate_drc_shell_script(drc_files)
    print(f"DRC执行脚本已生成: {script}")
    print(f"可通过命令执行: ./{script}")

    # 替换为你的DRC日志文件路径
    log_path = "dfcfb1.summary"
    drc_result = extract_drc_info(log_path)
   