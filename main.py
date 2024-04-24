import re
import csv

def extract_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        current_data = {}
        for line in lines:
            line = line.strip()
            if line.startswith('GPS'):
                if current_data:
                    data.append(current_data)
                    current_data = {}
                parts = line.split(',')
                current_data['Name'] = parts[1]
                la_part = parts[2].split('LA-')
                if len(la_part) > 1:
                    current_data['LA'] = float('-' + la_part[1])
                else:
                    current_data['LA'] = float(la_part[0].split('-')[1])
                ln_part = parts[3].split('LN')
                if len(ln_part) > 1:
                    if ln_part[0].endswith('-'):
                        current_data['LN'] = float('-' + ln_part[1])
                    else:
                        current_data['LN'] = float(ln_part[1])
                el_part = parts[4].split('EL')
                if len(el_part) > 1:
                    current_data['EL'] = float(el_part[1])
                stk_code_part = parts[-1].split('--')
                if len(stk_code_part) > 1:
                    stk_code = stk_code_part[1].split()
                    current_data['STK'] = stk_code[0]
                    current_data['CODE'] = ' '.join(stk_code[1:])
            elif line.startswith('--GS'):
                gs_pattern = r'--GS,\w+,N\s*(\d+\.\d+),E\s*(\d+\.\d+),EL(\d+\.\d+)'
                match = re.search(gs_pattern, line)
                if match:
                    current_data['GS_N'] = float(match.group(1))
                    current_data['GS_E'] = float(match.group(2))
                    current_data['GS_EL'] = float(match.group(3))
            elif line.startswith('--HSIG'):
                pdop_value = line.split('PDOP:')[1].split(',')[0]
                current_data['HSIG_PDOP'] = float(pdop_value)
        if current_data:
            data.append(current_data)
    return data

# input file
file_path = 'x.txt'
data = extract_data(file_path)

# output file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['Name', 'LA', 'LN', 'EL', 'STK', 'CODE', 'GS_N', 'GS_E', 'GS_EL', 'HSIG_PDOP']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for item in data:
        writer.writerow(item)

print("Generated: output.csv")