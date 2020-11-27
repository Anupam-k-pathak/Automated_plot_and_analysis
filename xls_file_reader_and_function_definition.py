import xlrd
import os
import re
import matplotlib.pyplot as plt

data_bank = []
location = 'src_data'


def read_header():
    for r, d, f in os.walk(location):
        for item in f:
            if '.xlsx' in item:
                wb = xlrd.open_workbook(os.path.join(r, item))
                sheet = wb.sheet_by_index(0)
                Dict = {}
                Dict.update({"file_name": str(item)})

                # for header
                for c in range(sheet.ncols):
                    zeroth = sheet.cell_value(0, c)
                    first = sheet.cell_value(1, c)
                    if zeroth:
                        if first:
                            Dict.update({str(zeroth).lower() : str(first).lower()})
                        else:
                            Dict.update({str(zeroth).lower(): str(0)})
                    else:
                        break

                # for other data
                for c in range(sheet.ncols):
                    head = sheet.cell_value(2, c)
                    if True:
                        data = []
                        for rw in range(sheet.nrows - 3):
                            data.append(sheet.cell_value(rw + 3, c))

                        Dict.update({str(head).lower() : data})
                data_bank.append(Dict)


def range_to_list(data):
    rtn_data = []
    for temp in data.split(","):
        if len(re.findall("-", temp)) > 1:
            return 1, rtn_data
        elif len(re.findall("-", temp)) == 1:
            start, end = temp.split("-")
            for i in range(int(start), int(end)+1):
                if int(i) not in rtn_data:
                    rtn_data.append(int(i))
        elif len(data) > 0:
            if int(temp) not in rtn_data:
                rtn_data.append(int(temp))
    return 0, rtn_data


def arg_Display_BW(data_range):
    global data_bank
    truncated_data_buk = []
    for dictionary in data_bank:
        ## print(dictionary)
        ## print(dictionary["num_of_sensors"])
        if int(float(dictionary["Display_BW"])) in data_range:
            truncated_data_buk.append(dictionary)

    data_bank = truncated_data_buk


def arg_qos(data_range):
    global data_bank
    truncated_data_buk = []
    for dictionary in data_bank:
        if int(float(dictionary["qos"])) in data_range:
            truncated_data_buk.append(dictionary)

    data_bank = truncated_data_buk


def arg_ddr(data_range):
    global data_bank
    truncated_data_buk = []
    for dictionary in data_bank:
        if int(float(dictionary["ddr"])) in data_range:
            truncated_data_buk.append(dictionary)

    data_bank = truncated_data_buk

def arg_run_time(r_time):
    global data_bank
    truncated_data_buk = []
    for dictionary in data_bank:
        if r_time == "100us":
            if str(dictionary["time"]) == "100us":
                truncated_data_buk.append(dictionary)
        elif r_time == "1ms":
            if str(dictionary["time"]) == "1ms":
                truncated_data_buk.append(dictionary)
    data_bank = truncated_data_buk


def cam_type_short(cam):
    global data_bank
    truncated_data_buk = []
    for dictionary in data_bank:
        if cam == "dual":
            if int(float(dictionary["num_of_sensors"])) == 2:
                truncated_data_buk.append(dictionary)
        elif cam == "triple":
            if int(float(dictionary["num_of_sensors"])) == 3:
                truncated_data_buk.append(dictionary)

    data_bank = truncated_data_buk


def find_header(dictionary, header):
    data = []
    #print("filename: ", dictionary["file_name"])
    for h in dictionary:
        # print("header:'" + str(header) + "'")
        # print("h:'" + str(h) + "'")
        if re.findall(header, h):
            # print("True")
            # if h == "buff_0_max_volume":
            #     for d in dictionary[h]:
            #         if d and d < 768:
            #             data.append(d)
            #         else:
            #             data.append(0)
            # elif h == "buff_1_max_volume":
            #     for d in dictionary[h]:
            #         if d and d < 520:
            #             data.append(d)
            #         else:
            #             data.append(0)
            # else:
            for d in dictionary[h]:
                if len(str(d)) != 0:
                    data.append(d)
                else:
                    data.append(0)

            break
    return data


def data_plot(x, y, x_min, x_max, y_min, y_max, legend):
    plt.scatter(x, y, label=legend, marker=".", s=30)
    axes = plt.gca()
    axes.set_xlim([float(x_min), float(x_max)])
    axes.set_ylim([float(y_min), float(y_max)])
    axes.legend()


def show_plot(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.show()
