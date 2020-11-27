import json
import modified_code_for_plot as imp
import derived_variable_function as dv
current_variable_json_file = "current_variables.json"
default_variable_json_file = "default_value.json"
derived_variable_json_file = "derived_variable.json"
post_filter_json_file = "post_filter.json"

def read_json(json_file):
    with open(json_file, 'r') as file:
        data = file.read()

    json_obj = json.loads(data)
    return json_obj


def derived_x(dictionary):
    temp = []
    ############################ change the function here for X-axis ######################
    #  ****-----------------------This is for (Display_BW + Video_front_eng_BW) ----------------****  #
    # temp = dv.add_cols(imp.find_header(dictionary, "Display_BW_BW"), imp.find_header(dictionary,"Video_front_eng_BW_BW"))
    #  ****-----------------------This is for (Display_BW + Video_front_eng_BW) ----------------****  #

    #  ****-----------------------This is for RT % ----------------****  #
    add = dv.add_cols(imp.find_header(dictionary, "Display_BW"), imp.find_header(dictionary, "Video_front_eng_BW"))
    mul = dv.mul_col_constant(imp.find_header(dictionary, "ddr_utilization"), int(float(dictionary["ddr"]))*8)   #### int(float(dictionary["ddr"]))*8 is similar to 2103*8
    temp = dv.div_cols(add, mul)
    #  ****-----------------------This is for RT % ----------------****  #
    ############################ change up to this #################################
    return temp


def derived_y(dictionary):
    temp = []
    ############################ change the function here for Y-axis ######################
    # -------------------------------------
    temp = imp.find_header(dictionary, post_filter["VARIABLE"][1])        ## post_filter["VARIABLE"][1] means y-axis from post_filter.json file
    # -------------------------------------
    ############################ change up to this #################################

    return temp


if __name__ == "__main__":
    current_obj = read_json(current_variable_json_file)
    default_obj = read_json(default_variable_json_file)
    derived_variable = read_json(derived_variable_json_file)
    post_filter = read_json(post_filter_json_file)

    derived_x_formula = derived_variable["X_axis"]

    variable = current_obj["VARIABLE"]
    imp.read_header()

    if "Display_BW" in variable:
        error, data_range = imp.range_to_list(current_obj["Display_BW"]["Current_val"])
        #print("Display_BW:", error, data_range)
        if len(data_range) == 0:
            print("Display_BW taking default values")
            error, data_range = imp.range_to_list(default_obj["Display_BW"]["Default_val"])
        print("Display_BW:", error, data_range)
        imp.arg_mdp(data_range)

    if "QOS" in variable:
        error, data_range = imp.range_to_list(current_obj["QOS"]["Current_val"])
        if len(data_range) == 0:
            print("QOS taking default values")
            error, data_range = imp.range_to_list(default_obj["QOS"]["Default_val"])
        imp.arg_qos(data_range)

    if "DDR" in variable:
        error, data_range = imp.range_to_list(current_obj["DDR"]["Current_val"])
        if len(data_range) == 0:
            print("DDR taking default values")
            error, data_range = imp.range_to_list(default_obj["DDR"]["Default_val"])
        imp.arg_ddr(data_range)

    if "CAM_TYPE" in variable:
        cam = current_obj["CAM_TYPE"]["Current_val"]
        if len(cam) == 0:
            print("CAM TYPE taking default values")
            cam = default_obj["CAM_TYPE"]["Default_val"]
        imp.cam_type_short(cam)

    if "TIME" in variable:
        r_time = current_obj["TIME"]["Current_val"]
        if len(r_time) == 0:
            print("TIME taking default values")
            r_time = default_obj["TIME"]["Default_val"]
        imp.arg_run_time(r_time)

    for dictionary in imp.data_bank:      ##### for all xlxs sheets present in data bank, plot graphs #####
        x = derived_x(dictionary)
        y = derived_y(dictionary)
        count = 0
        y1 = []
        x1 = []
        for i in y:
            if i < 768:                 ####### To remove 768 value from y and remove corresponding x ######
                y1.append(y[count])
                x1.append(x[count])
            count = count + 1
        legend = ""
        for var in variable:
            if var != "CAM_TYPE":
                legend += var + " : " + str(dictionary[var.lower()]) + ", "
            elif str(current_obj["CAM_TYPE"]["Current_val"]) != "":
                legend += var + " : " + str(current_obj["CAM_TYPE"]["Current_val"]) + ", "
            else:
                legend += var + " : " + str(default_obj["CAM_TYPE"]["Default_val"]) + ", "
        legend = legend[:-2]
        x_axis = post_filter["VARIABLE"][0]
        y_axis = post_filter["VARIABLE"][1]

        x_limit = post_filter[x_axis]["Current_val"].split("-")
        y_limit = post_filter[y_axis]["Current_val"].split("-")

        imp.data_plot(x1, y1, x_limit[0], x_limit[1], y_limit[0], y_limit[1], legend)
    imp.show_plot(post_filter["VARIABLE"][0], post_filter["VARIABLE"][1], str(post_filter["VARIABLE"][1]) + " Vs " + str(post_filter["VARIABLE"][0]))
