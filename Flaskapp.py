import sqlite3
from flask import Flask, request, jsonify
app = Flask(__name__)
app.config["DEBUG"] = True
possible_args = [["date","str"],["time","str"],["temperature","float"],["humidity","float"],["air_pressure","float"],["illuminance","float"],["location","str"]]


def does_list_contain(clist,datapoint):
    for item in clist:
        if item == datapoint:
            return True
    return False

def get_data_from_table(db_name : str,table_name : str,Date : bool = False,Time : bool = False,temperature : bool = False,humidity : bool = False,air_pressure: bool = False,illuminance: bool = False, Location : bool = False):
    data_to_pull = []
    if Date == True:
        data_to_pull.append("Date")
    if Time == True:
        data_to_pull.append("Time")
    if temperature == True:
        data_to_pull.append("Temperature")
    if humidity == True:
        data_to_pull.append("Humidity")
    if air_pressure == True:
        data_to_pull.append("AirPressure")
    if illuminance == True:
        data_to_pull.append("Illuminance")
    if Location == True:
        data_to_pull.append("Location")
    complete_string = ""
    for i in data_to_pull:
        if i != data_to_pull[len(data_to_pull)-1]:
            complete_string += i+","
        else:
            complete_string += i
    print(data_to_pull)
    con = sqlite3.connect(db_name+".db")
    cur = con.cursor()
    print(complete_string)
    table = cur.execute(f"SELECT {complete_string} FROM {table_name}")
    for record in table:
        print(record)
    con.close()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Blank page</p>"
@app.route("/pull_all")
def pull_data():
    con = sqlite3.connect("basicDB.db")
    cur = con.cursor()
    table = cur.execute("SELECT * FROM BeeData")
    Array = []
    for record in table:
        Array.append(record)
    con.close()
    return jsonify(Array)

#example url http://127.0.0.1:5000/pull_data?Location=London&Time=19:20
@app.route("/pull_data", methods=['GET'])
def pull_datas():
    con = sqlite3.connect("basicDB.db")
    cur = con.cursor()
    print(str(request.args))
    con.close()
    possible_args = [["date","str"],["time","str"],["temperature","float"],["humidity","float"],["air_pressure","float"],["illuminance","float"],["location","str"]]
    for i in possible_args:
        if request.args.get(i):
            return request.args.get(i)
    return "query contains invalid arguments"

@app.route("/bee_data/api/v1/data_base", methods=['GET'])
def get_data_from_table():
    wanted_args = []
    con = sqlite3.connect("basicDB.db")
    cur = con.cursor()
    for i in possible_args:
        if request.args.get(i[0]): 
            wanted_args.append([i[0],request.args.get(i[0]),i[1]])
    args = ""
    for i in wanted_args:
        if i[0] != wanted_args[len(wanted_args)-1][0]:
            if i[2] == "str":
                args += str(i[0])+"="+"'"+str(i[1])+"'"+" AND "
            else:
                args += str(i[0])+"="+str(i[1])+" AND "
        else:
            if i[2] == "str":
                args += str(i[0])+"="+"'"+str(i[1])+"'"
            else:
                args += str(i[0])+"="+str(i[1])
    print(args)
    data = cur.execute(f"SELECT * FROM BeeData WHERE {args}")
    data2 = []
    for row in data:
        data2.append(row)
    return str(data2)


posible_args = [["date","str"],["time","str"],["temperature","float"],["humidity","float"],["air_pressure","float"],["illuminance","float"],["location","str"]]

@app.route("/bee_data/api/v2/data_base", methods=['GET'])
def get_data_v2():
    con = sqlite3.connect("basicDB.db")
    cur = con.cursor()
    wanted_sargs = []
    wanted_cargs = []
    for args in posible_args:
        if request.args.get("s"+args[0]):
            wanted_sargs.append(args[0])
        elif request.args.get("c"+args[0]):
            wanted_cargs.append([args[0],request.args.get("c"+args[0]),args[1]])
            
    select_args = ""
    if len(wanted_sargs) > 0:
        for args in wanted_sargs:
            if args == wanted_sargs[len(wanted_sargs)-1]:
                select_args += args 
            else:
                select_args += args + "AND"
    else:
        select_args = "*"
    #only includes equal to currently
    condition_args = ""
    for args in wanted_cargs:
        if args == wanted_cargs[len(wanted_cargs)-1]:
            if args[2] == "str":
                condition_args += str(args[0])+"="+"'"+str(args[1])+"'"
            else:
                condition_args += str(args[0])+"="+str(args[1])
        else:
            if args[2] == "str":
                condition_args += str(args[0])+"="+"'"+str(args[1])+"'"+" AND "
            else:
                condition_args += str(args[0])+"="+str(args[1])+" AND "
    table_return = cur.execute(f"SELECT {select_args} FROM BeeData WHERE {condition_args}")
    table_data = []
    for row in table_return:
        table_data.append(row)
    con.close()   
    return jsonify(table_data)
@app.route("/bee_data/api/v3/data_base", methods=['GET'])
def get_data_v3():
    #will be the same the only difference will be the select singel query seperated with :
    con = sqlite3.connect("Bee_Data_Base.db")
    cur = con.cursor()
    select_args = ""
    wanted_cargs = []
    if request.args.get("select"):
        possible_args = request.args.get("select").split(":")
        for arg in possible_args:
            if arg == possible_args[len(possible_args)-1]:
                select_args += arg
            else:
                select_args += arg +","


    for args in posible_args:
        if request.args.get(args[0]):
            wanted_cargs.append([args[0],request.args.get(args[0]),args[1]])
       
    #only includes equal to currently
    condition_args = ""
    for args in wanted_cargs:
        if args == wanted_cargs[len(wanted_cargs)-1]:
            if args[2] == "str":
                condition_args += str(args[0])+"="+"'"+str(args[1])+"'"
            else:
                condition_args += str(args[0])+"="+str(args[1])
        else:
            if args[2] == "str":
                condition_args += str(args[0])+"="+"'"+str(args[1])+"'"+" AND "
            else:
                condition_args += str(args[0])+"="+str(args[1])+" AND "
    #table_return = cur.execute(f"SELECT {select_args} FROM BeeData WHERE {condition_args}")
    table_return = cur.execute(f"SELECT {select_args} FROM BeeData WHERE {condition_args}")
    table_data = []
    for row in table_return:
        table_data.append(row)
    con.close()   
    #return jsonify(table_data)
    return condition_args
    #return select_args

#same as previous only condition query changes
possible_args = ["date","time","temperature","humidity","air_pressure","illuminance","location"]
@app.route("/bee_data/api/v4/data_base", methods=['GET'])
def get_data_v4():
    #will be the same the only difference will be the conditions will be speretated with ;
    #example ?condition=time<19:20;temperature=20
    #change date to format  YYYY/MM/DD
    #select example ?select=time:date:location
    con = sqlite3.connect("Bee_Data_Base.db")
    cur = con.cursor()
    SQL_command = ""
    
    select_args = ""
    config = []
    if request.args.get("select"):
        possible_select_args = request.args.get("select").split(":")
        for arg in possible_select_args:
            if does_list_contain(possible_args,arg):
                config.append(arg)
        
        for arg in config:
            if arg == config[len(config)-1]:
                select_args += arg
            else:
                select_args += arg +","
    else:
        select_args = "*"
    SQL_command += f"SELECT {select_args} FROM BeeData" 
    condition_args = ""
    config = []
    if request.args.get("condition"):
        possible_condition_args = request.args.get("condition").split(";")
        for arg in possible_condition_args:
            if does_list_contain(possible_args,arg):
                config.append(arg)

        for arg in possible_condition_args:
            if arg == possible_condition_args[len(possible_condition_args)-1]:
                condition_args += arg
            else:
                condition_args += arg + " AND "
        SQL_command += f" WHERE {condition_args}"
    table_return = cur.execute(SQL_command)
    #table_return = cur.execute(f"SELECT {select_args} FROM BeeData")
    #table_return = cur.execute(f"SELECT * FROM BeeData WHERE {condition_args}")
    
    table_data = []
    for row in table_return:
        table_data.append(row)
    con.close()   
    #return condition_args
    return jsonify(table_data)
app.run()

