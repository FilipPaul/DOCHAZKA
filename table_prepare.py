import datetime
import holidays

def generateDatesOfMonth(month_inp:int,year_inp:int) -> tuple[list, list]:
    """Generate list of days in month, with updated Names of day into CZECH language,
    also take account public holidays"""
    public_holiday_list = []
    for public_hollydays in holidays.Czechia(years= int(year_inp)).items():
        public_holiday_list.append(public_hollydays)

    month, year = int(month_inp), int(year_inp)

    day = datetime.timedelta(days=1)
    date = datetime.date(year, month, 1)
    dates = []

    while date.month == month:
        final_date  = ""
        final_date += date.strftime("%A")
        final_date += f" { date.strftime('%d.%m.%Y') }"  
        for holiday in public_holiday_list: #check if day is public hollyday
            if holiday[0] == date:
                final_date += f" svátek"    
        #Translate days
        final_date = final_date.replace("Monday", "Po")
        final_date = final_date.replace("Tuesday","Út")
        final_date = final_date.replace("Wednesday","St")
        final_date = final_date.replace("Thursday","Čt")
        final_date = final_date.replace("Friday","Pá")
        final_date = final_date.replace("Saturday","So")
        final_date = final_date.replace("Sunday","Ne")

        dates.append(final_date)
        date += day

        only_dates = []
        for strings in dates:
            if len(strings) == 13:
                only_dates.append(strings[3:])
            else:
                only_dates.append(strings[3:13])
        
    return dates,only_dates

def create_list_of_dictionaries_rows(full_dates: list, only_dates:list,query_dictionary, month:int, year:int):
    """PROBLEM: result from query is in form like this:
    query_dictionary =
    {
    'EDIT':["'NONE'","'NONE'","'NONE'"], #members in list represents individual rows
    'ID':['38', '47', '57'],
    'Jmeno': ["'Filip '","'Filip'","'Filip'"],
    'LOG_ID': ["'38'", "'47'", "'57'"],
    'Prijmeni': ["'Paul'","'Paul'","'Paul'"],
    'SAVED_DATE': ['#2022-02-09 00:00:00#','#2022-02-10 00:00:00#','#2022-02-10 00:00:00#'],
    'SAVED_TIME': ['#1900-01-01 17:01:33#','#1900-01-01 07:40:51#','#1900-01-01 15:50:43#'],
    'STAV': ["'Odchod'","'Prichod'","'Odchod'",],
    'TAG': ["'1A 30 66 62'","'1A 30 66 62'","'1A 30 66 62'"]
    }

    GOAL is create rows, where all rows with the same TAG and SAVED_DATE will be merged together
    and the merged rows will add only not redundant info about STAV and SAVED_TIME like this:

    for easier implementation first create dict in form like this:
    in this I can easily check if in ROW_X key X exists... and it has more tranparent code...
    
    dict_representing_row =
    }
     ROW_1:{ EDIT: ..., ID:...,Jmeno:...,Prijmeni:...,TAG:..., SAVED_DATE: 01.02.2022, STAV: Prichod, SAVED_TIME:...STAV_1:Odchod,SAVED_TIME_1:...},
     ROW_2:{ EDIT: ..., ID:...,Jmeno:...,Prijmeni:...,TAG:..., SAVED_DATE: 02.02.2020, STAV: Prichod, SAVED_TIME:...STAV_1:Odchod,SAVED_TIME_1:...}
    }

    and then convert it into final ouptut list_of_rows.
    list_of_rows=
    [
     { EDIT: ..., ID:...,Jmeno:...,Prijmeni:...,TAG:..., SAVED_DATE: 01.02.2022, STAV: Prichod, SAVED_TIME:...STAV_1:Odchod,SAVED_TIME_1:...},
     { EDIT: ..., ID:...,Jmeno:...,Prijmeni:...,TAG:..., SAVED_DATE: 02.02.2020, STAV: Prichod, SAVED_TIME:...STAV_1:Odchod,SAVED_TIME_1:...}
    ]



    Note that STAV_X and SAVED_TIME_X will be generated acordingly to the maximal multiplicities in SAVED_DATE.
    This function returns dictionary exactly like described above
    """
    full_dates,only_dates = generateDatesOfMonth(month,year)
    i = 0 #help itterable, iterates with each row of original dictionary (query_dictionary)
    dict_representing_row = {} 
    for log_dates in query_dictionary["SAVED_DATE"]: #for each date
        #format savedDate into form of dd.mm.yy
        date_object = datetime.datetime.strptime(log_dates,"#%Y-%m-%d %H:%M:%S#")
        log_dates_formated = date_object.strftime("%d.%m.%Y")   
        for dates in only_dates: #check if current row from query match generated dates
            if dates == log_dates_formated: # IF match
                row_key = f"ROW_{only_dates.index(dates)}" #set key of dict_representing_row to row of matched generated date
                
                for global_keys in query_dictionary: #global keys are keys like EDIT,ID,STAV,SAVED_DATE,etc
                    if (row_key in dict_representing_row): #if ROW_X already exists
                        item_key_iterable = 0 #help iterable
                        item_key = f"{global_keys}" #set current KEY of ROW_X --> {ROW_X:{item_key:...}}, where item KEY is fEX: SAVED_TIME
                        while item_key in dict_representing_row[row_key]:
                            #while item key already exists iterate it like STAV -> STAV_1 -> STAV_2.
                            if global_keys not in ("SAVED_TIME", "STAV") : #only in SAVED_TIME or STAV matters
                                break
                            else:
                                item_key_iterable += 1
                                item_key = f"{global_keys}_{item_key_iterable}"
                    else:#if ROW_X doesnt exist -> create it
                        item_key = f"{global_keys}"
                        dict_representing_row[f"ROW_{only_dates.index(dates)}"] = {}
                        dict_representing_row[f"ROW_{only_dates.index(dates)}"][item_key] = log_dates
                    dict_representing_row[row_key][item_key] = query_dictionary[global_keys][i]
                    #p.pprint(dict_representing_row)

        i+=1 # iterates with each row of original dictionary (query_dictionary)

    #Now we created dict_representing_row, lets convert it into list_of_rows
    list_of_rows = [None for members in only_dates] #create None buffer for list_of_rows output (fill all unused rows with None)
    for row_keys in dict_representing_row:
        row_num = int(row_keys[4:]) #dictionary is unordered, but we have keys in form like ROW_X -> take X
        list_of_rows[row_num] = dict_representing_row[row_keys] # {ROW_X:{ID:...,SAVED_TIME,.. etc}} -> PUT {ID:...,SAVED_TIME,.. etc} into list
   

    #NOW fill all remaining None rows with default values
    x = 0 #help itterable which represents list index (row)
    for members in list_of_rows:
        if members == None:
            list_of_rows[x] = {"GEN_DATE": full_dates[x]}#just in case, that query is empty genereate atleast dates
            for keys in dict_representing_row:#rows in dict_representing_row
                for nested_keys in dict_representing_row[keys]:#item_keys == nested_keys (SAVED_TIME,etc..)
                    list_of_rows[x][nested_keys] = None #fill all item keys in final list with None Value
                    list_of_rows[x]["GEN_DATE"] = full_dates[x] #DEFAULT value of generated date
        else: #if row exists, append GEN_DATE key, which will be always displayed
            list_of_rows[x]["GEN_DATE"] = full_dates[x] 
        x+= 1
    return list_of_rows

def create_dictionary_for_table_widget(query_dictionary,month,year):
    """Creates dictionary in suitable form for function, which is used for filling table widget:
    this form is: {COLUMN_NAME_1:[row_1_data,row_2_data], COLUMN_NAME_2:[row_1_data,row_2_data]}
    also merge columns with the same date and TAG ID (more info in description of create_list_of_dictionaries_rows function"""
    full_dates,only_dates = generateDatesOfMonth(month,year)

    #list of merged rows:
    list_of_rows = create_list_of_dictionaries_rows(full_dates,only_dates,query_dictionary,month,year)
    
    #CONVERTING into table update form:
    final_dict_of_lists_collumns = {} 
    ## CREATE HEADERS (need to scan all rows, because the length of row is not static)
    for rows in list_of_rows:
        for collumns in rows:
            final_dict_of_lists_collumns[collumns] = []
    
    
    for keys in final_dict_of_lists_collumns: #for each column HEADER (key)
        for i in range(len(list_of_rows)): #for each row
            if keys in list_of_rows[i]: #if current row has column HEADER (key)
                final_dict_of_lists_collumns[keys].append(list_of_rows[i][keys]) #asign value
            else: #if row does not have key from HEADER
                final_dict_of_lists_collumns[keys].append(None) #asign None


    #final_dict_of_lists_collumns["Jmeno"] = [query_dictionary["Jmeno"][-1] for members in final_dict_of_lists_collumns["GEN_DATE"] if query_dictionary["Jmeno"] != [] ]
    #final_dict_of_lists_collumns["Prijmeni"] = [query_dictionary["Prijmeni"][-1] for members in final_dict_of_lists_collumns["GEN_DATE"] if query_dictionary["Jmeno"] != []]
    final_dict_of_lists_collumns["CELKEM HODIN"] = [None for members in final_dict_of_lists_collumns["GEN_DATE"] ]


    return final_dict_of_lists_collumns