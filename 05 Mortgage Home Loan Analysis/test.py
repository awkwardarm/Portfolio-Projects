filename = "2021Q3.csv"

def quarter_string_to_num(filename):

    filename_str = filename[:4] + "." + filename[-5]

    filename_num = ''

    if filename_str[-1] == '1':
        filename_num += filename_str[:-1] + '00'
    elif filename_str[-1] == '2':
        filename_num += filename_str[:-1] + '25'
    elif filename_str[-1] == '3':
        filename_num += filename_str[:-1] + '5'
    elif filename_str[-1] == '4':
        filename_num += filename_str[:-1] + '75'
    
    return float(filename_num)

print(quarter_string_to_num(filename))