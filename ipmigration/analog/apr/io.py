import re
import csv

# basic_info = ['ART368_demo_tsmc018','OTA','schematic']
para_attr = {'mos':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                    'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                    'm':{'cdf_name':'m','cdf_unit':'','cdf_type':'string'}},
             'mimcap':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                       'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                       'm':{'cdf_name':'m','cdf_unit':'','cdf_type':'string'}},
             'respoly':{'w':{'cdf_name':'w','cdf_unit':'u','cdf_type':'string'},
                        'l':{'cdf_name':'l','cdf_unit':'u','cdf_type':'string'},
                        'm':{'cdf_name':'segments','cdf_unit':'','cdf_type':'string'}}
             }

def csv_to_skill(csv_path, output_skill_path,para_attr):
    lines = []
    # lines.append("cv=dbOpenCellViewByType(\"%s\" \"%s\" \"%s\" \"\" \"r\")\n"%(basic_info[0],basic_info[1],basic_info[2]))
    lines.append("insts=cv->instances\n")
    
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        # 创建 CSV 读取器
        csv_reader = csv.reader(file)
        
        # 读取所有行（返回列表的列表）
        rows = list(csv_reader)
        col_names = rows[0]
        for row in rows[1:]:
            name = row[0]
            if name.startswith('M') or name.startswith('m'):
                attrs = para_attr['mos']
            if name.startswith('C') or name.startswith('c'):
                attrs = para_attr['mimcap']
            if name.startswith('R') or name.startswith('r'):
                attrs = para_attr['respoly']
            
            for idx,para in enumerate(row[1:]):
                para_name =col_names[idx+1] 
                attr = attrs[para_name]
                lines.append("inst=car(setof(a insts a->name==\"%s\"))\n"%(name))
                lines.append("instCdf=cdfGetInstCDF(inst)\n")
                if attr['cdf_type'] == 'string':
                    value = para+attr['cdf_unit']
                    lines.append("cdfFindParamByName(instCdf \"%s\")~>value=\"%s\"\n"%(attr['cdf_name'],value))
                else:
                    value = para
                    lines.append("cdfFindParamByName(instCdf \"%s\")~>value=%s\n"%(attr['cdf_name'],value))

    
    with open(output_skill_path, 'w') as f:
        for line in lines:
            f.write(line)












def netlist_to_csv(netlist_path, output_csv_path):
    """
    Convert Spectre netlist to CSV, retaining device names and l/w/m parameters.
    :param netlist_path: Path to input netlist file
    :param output_csv_path: Path to save output CSV file
    """
    # Regex patterns: match device names and l/w/m parameters (order-agnostic)
    # Device name: Starts with M/C/R, followed by letters/numbers/underscores (e.g., M14, C1, R3_1__dmy0)
    device_pattern = re.compile(r'^(M\w+|C\w+|R\w+)')
    # Parameter patterns: Match l=xx, w=xx, m=xx (supports values with units like 1u, 28.0u)
    param_patterns = {
        'l': re.compile(r'l=([\d\.]+[a-zA-Z]?)'),  # Length parameter
        'w': re.compile(r'w=([\d\.]+[a-zA-Z]?)'),  # Width parameter
        'm': re.compile(r'm=([\d\.]+[a-zA-Z]?)')   # Multiplier parameter
    }

    # Store CSV data (header + rows)
    csv_data = [['Device_Name', 'Length(l)', 'Width(w)', 'Multiplier(m)']]

    # Read and parse netlist line by line
    with open(netlist_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line_stripped = line.strip()
            # Skip comments, empty lines, and non-device lines (e.g., simulator config, includes)
            if not line_stripped or line_stripped.startswith('//') or \
               any(keyword in line_stripped for keyword in ['simulator', 'global', 'include', 'simulatorOptions', 'modelParameter', 'element', 'outputParameter', 'designParamVals', 'primitives', 'subckts', 'saveOptions']):
                continue

            # Extract device name
            device_match = device_pattern.match(line_stripped)
            if not device_match:
                continue  # Skip non-target device lines
            device_name = device_match.group(1)

            # Extract l/w/m parameters (empty string if not found)
            param_l = param_patterns['l'].search(line_stripped).group(1) if param_patterns['l'].search(line_stripped) else ''
            param_w = param_patterns['w'].search(line_stripped).group(1) if param_patterns['w'].search(line_stripped) else ''
            param_m = param_patterns['m'].search(line_stripped).group(1) if param_patterns['m'].search(line_stripped) else ''

            # Add to CSV data
            csv_data.append([device_name, param_l, param_w, param_m])

    # Write to CSV file
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csv_f:
        csv_writer = csv.writer(csv_f)
        csv_writer.writerows(csv_data)

    print(f"CSV file generated: {output_csv_path}")
    print(f"Extracted {len(csv_data)-1} devices (header excluded)")


# ------------------- Configuration -------------------
NETLIST_PATH = "data/schematic_data.scs"  # Replace with your netlist path (absolute path allowed)
OUTPUT_CSV_PATH = "data/device_parameters.csv"  # Output CSV path
OUTPUT_SKILL_PATH = "ipm_skill/sized_schematic_data.il"  # Output CSV path
# -----------------------------------------------------

# Execute conversion
if __name__ == "__main__":
    # netlist_to_csv(NETLIST_PATH, OUTPUT_CSV_PATH) 
    csv_to_skill(OUTPUT_CSV_PATH, OUTPUT_SKILL_PATH,para_attr)