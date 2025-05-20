#!/bin/csh -f

# Python程序测试脚本
# 用于测试不同工艺规则文件的提取功能

# 设置Python解释器路径
set python_path = "/data/icdesign/ams/ip_migration/tools/anaconda3/bin/python"

# 设置主程序路径
set main_program = "run_rule.py"

# 设置llm host的ip
set llm_host = 'http://10.6.126.115:11434'
set llm_model = 'deepseek-r1:32b'
# 设置保存根目录
set save_dir = "./demo/rule/output/test_results_`date +%Y%m%d_%H%M`"
mkdir -p $save_dir

# 设置测试数据数组根目录
set data_dir = "./demo/rule/decks"

# 测试数据数组
set tbs = ( "c153,c153.rul,c153_ldef.csv"\
            "s40,s40.drc,s40_ldef.csv"\
            "s65,s65.drc,s65_ldef.csv"\
            "s110,s110.drc,s110_ldef.csv"\
            "t40,t40_calibre.drc,t40_ldef.csv"\
            "t65,t65_calibre.drc,t65_ldef.csv" )

#set tbs = ( "c153,c153.rul,c153_ldef.csv")


foreach test_data ($tbs)
    set tech_name = `echo $test_data | awk -F',' '{print $1}'`
    set drc_deck_file = `echo $test_data | awk -F','  '{print $2}'`
    set layer_def_file = `echo $test_data | awk -F','  '{print $3}'`
    set drc_deck = "$data_dir/$drc_deck_file"
    set layer_def = "$data_dir/$layer_def_file"
    echo "------------------------"
    echo "工艺名称: $tech_name"
    echo "规则文件: $drc_deck"
    echo "层定义文件: $layer_def"
    
    set test_output_dir = "$save_dir/${tech_name}"
    mkdir -p $test_output_dir
    
    echo "执行命令: $python_path $main_program --tech-name $tech_name --drc-deck $drc_deck --layer-def $layer_def --output-mode single --debug True --client-host $llm_host --save-dir $test_output_dir"
    
    # 执行Python程序并捕获输出
    set log_file = "$test_output_dir/test.log"
    $python_path $main_program --tech-name $tech_name --drc-deck $drc_deck --layer-def $layer_def --output-mode single --debug True --client-host $llm_host --client-model $llm_model --save-dir $test_output_dir >& $log_file
    
    # 检查执行状态
    if ($status == 0) then
        echo "测试成功，查看日志: $log_file"
    else
        echo "测试失败，查看日志: $log_file"
    endif
    
    echo ""
end

echo "=== 所有测试完成 ==="
echo "测试结果保存在: $save_dir"   