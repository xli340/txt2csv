import re
import csv

def extract_data(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    data_list = re.split(r'08RK', data)[1:]
    csv_data = []
    count = 1

    for item in data_list:
        if item.strip():
            number = f"LT{count}"
            count += 1

            # extact N
            n_start = item.find(number) + len(number)
            n_end = item.find(' ', n_start)
            n = float(item[n_start:n_end])
            n = f"{n:.3f}"

            # extact E
            e_start = n_end + 1
            e_end = item.find(' ', e_start)
            e = float(item[e_start:e_end])
            e = f"{e:.3f}"

            # extact H
            h_start = e_end + 1
            h_end = item.find(' ', h_start)
            h = float(item[h_start:h_end])
            h = f"{h:.2f}"

            # extact Code
            code_start = h_end + 1
            code_end = item.find('\n', code_start)
            code = item[code_start:code_end]

            # extact HSIG
            hsig_match = re.search(r'13NMHSIG:([\d\.]+)', item)
            hsig = hsig_match.group(1) if hsig_match else ''

            # extact VSIG
            vsig_match = re.search(r'VSIG:([\d\.]+)', item)
            vsig = vsig_match.group(1) if vsig_match else ''

            # extact SATS
            sats_match = re.search(r'SATS:(\d+)', item)
            sats = sats_match.group(1) if sats_match else ''

            # extact PDOP
            pdop_match = re.search(r'PDOP:([\d\.]+)', item)
            pdop = pdop_match.group(1) if pdop_match else ''

            # extact HDOP
            hdop_match = re.search(r'HDOP:([\d\.]+)', item)
            hdop = hdop_match.group(1) if hdop_match else ''

            # extact VDOP
            vdop_match = re.search(r'VDOP:([\d\.]+)', item)
            vdop = vdop_match.group(1) if vdop_match else ''

            # extact MSIG
            msig_match = re.search(r'13NMSIG:([\d\.]+)', item)
            msig = msig_match.group(1) if msig_match else ''

            csv_data.append([number, n, e, h, code, hsig, vsig, sats, pdop, hdop, vdop, msig])

    return csv_data

def save_to_csv(data, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Number', 'N', 'E', 'H', 'Code', 'HSIG', 'VSIG', 'SATS', 'PDOP', 'HDOP', 'VDOP', 'MSIG'])
        writer.writerows(data)

if __name__ == "__main__":
    input_file_path = 'input.txt'
    output_file_path = 'output.csv'

    data = extract_data(input_file_path)
    save_to_csv(data, output_file_path)
    print("Generated: output.csv")
