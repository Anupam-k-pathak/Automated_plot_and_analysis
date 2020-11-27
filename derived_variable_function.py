def add_cols(col1, col2):
    print("from col add ",len(col1), len(col2))
    col = [col1[i]+col2[i] for i in range(len(col1))]
    return col


def sub_cols(col1, col2):
    col = [col1[i]-col2[i] for i in min(range(len(col1)),range(len(col2)))]
    return col


def mul_cols(col1, col2):
    col = [col1[i]*col2[i] for i in min(range(len(col1)),range(len(col2)))]
    return col


def div_cols(col1, col2):
    print("from col div ", len(col1), len(col2))
    col = []
    for i in range(len(col1)):
        if type(col1[i]) != str and type(col2[i]) != str and col2[i] != 0:
            col.append(float(col1[i]) / (float(col2[i])))
        else:
            col.append(0)
    return col


def add_col_constant(col1, cons):
    col = [col1[i]+cons for i in range(len(col1))]
    return col


def sub_col_constant(col1, cons):
    col = [col1[i]-cons for i in range(len(col1))]
    return col


def mul_col_constant(col1, cons):
    col = [col1[i]*cons for i in range(len(col1))]
    return col


def div_col_constant(col1, cons):
    col = [col1[i]/cons for i in range(len(col1))]
    return col






