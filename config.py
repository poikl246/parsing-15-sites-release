import csv

def output_csv(parsing_data, input_data, name):
    print(parsing_data)
    data = parsing_data[1]
    liner = [[name, ' ']]
    for in_data in input_data:
        liner[0].append(str(in_data).replace('"', '').replace(']', '').replace('[', '').replace("'", "").replace('\u0131', ''))
    for line in data:
        liner.append([' '] + [line[1]] + line[0])
    print("[CONFIG] ",int(len(data[0][0])))
    caunt_list = [0]* int(len(data[0][0]))

    for dat in data:

        list_loc = []
        for caunt__ in range(len(dat[0])):
            caunt_list[caunt__] = (int(caunt_list[caunt__]) +  int(dat[0][caunt__]))


    out_list = [" ", " "]
    out_list.extend(caunt_list)


    liner.append([])
    liner.append(out_list)

    #
    with open('Data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(liner)

    return caunt_list

def exit_code(caunt_list):
    out_list = [" ", " "]
    out_list.extend(caunt_list)
    liner = []
    liner.append([])
    liner.append([])
    liner.append([])
    liner.append([])
    liner.append(out_list)

    #
    with open('Data.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(liner)

def input_data():
    with open("Input.csv", 'r', encoding='utf-8') as r_file:
        file = r_file.readlines()
    dat = []
    for f in file:
        local = []
        for w in f.replace('\n', '').split(';'):
            if w != '':
                local.append(w)
        dat.append(local)


    return dat

