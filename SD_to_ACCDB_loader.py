"""This module takes data from SD card (fetched in fetch_data.py and parsed in correct_file.py)
order them in suitable form (all data from one day in one row) and store them in MS Acces database.
This module also takes care of synchorization of data in database and SD card.

In onther words, this Trasports data from attendance system to database.
"""

from datetime import datetime
import yaml 
from AutomateSuperPackage.AutomateSuperModule import SuperClass
from fetch_data import FetchData
from correct_file import FileCorrector

        

class Synchro():
    def __init__(self,ACCES:SuperClass().database.AccesDatabase,YAML) -> None:
        #LOAD CONFIG FILE WITH STORED PATHS
        self.YAML = YAML
        self.ACCES = ACCES
        #INIT DATABASE
        self.ACCES.multipleCursors([ self.YAML["ACCDB"] ])
        self.cursor_index = 0 #ALL changes are made at index 0
        self.FatchData = FetchData(link=self.YAML["URL"],logs=self.YAML["PATHS"][0]["path"] + self.YAML["PATHS"][0]["file"])
        self.FileCorrector = FileCorrector(file_path=self.YAML["PATHS"][0]["path"] + self.YAML["PATHS"][0]["file"], new_file_path=self.YAML["PATHS"][1]["path"] + self.YAML["PATHS"][1]["file"])
        self.last_ID_in_database = 0
        self.last_ID_in_SD = 0

    def tableAlreadyExists(self,table,cursor_index):
        for rows in self.ACCES.cursors[cursor_index].tables():
            if rows[2] == table:
                return 1 #table already exists
        return 0 #Table doesnt exists

    def getTableContent(self,table,cursor_index):
        """retunr dictionary, where key corresponds to the name of column and value coresponds to the datatype"""
        #GET INFO ABOUT TABLE
        column_name_types_dict= {}
        for row in self.ACCES.cursors[cursor_index].columns(table = table):
            if row.type_name == "VARCHAR":
                column_name_types_dict[row.column_name] =  str(row.type_name) + "(" +str( row.column_size) + ")"
            if row.type_name == "CHAR":
                column_name_types_dict[row.column_name] =  str(row.type_name) + "(" +str( row.column_size) + ")"
            else:
                column_name_types_dict[row.column_name] =  row.type_name
        return column_name_types_dict

    def parseSDfileToListOfDictionaries(self,file_name):
        """output is in form:
        [{column_1_key: data, column_2_key:data, column_3_key: data....}, #row1
        {column_1_key: data, column_2_key:data, column_3_key: data....}, #row2
        {column_1_key: data, column_2_key:data, column_3_key: data....}, #row3
        ]"""
        for files in self.YAML["PATHS"]:
            if files["file"] == file_name:
                with open(files["path"] + files["file"], "r") as f:
                    lines = f.readlines()
        list_of_lines = []
        dict_from_SD_line = {}
        for line in lines:
            line = line.split(";")
            dict_from_SD_line.clear()
            if len(line) > 1:
                for i in range(0,int(len(line))-1):
                    if i%2 == 0:
                        dict_from_SD_line[line[i]] = line[line.index(line[i])+1]
                list_of_lines.append(dict_from_SD_line.copy())
        return list_of_lines
            
    def insertRowsFromListOfDictionaries(self,list_of_dictionaries,table_name,cursor_index):
        """UPDATE MS ACCES TABLE ACCORDINGLY TO LIST_OF_DICTIONARIES,
        which can be obtained from parseSDfileToListOfDictionaries function"""
        SQL_string = f"INSERT INTO {table_name} ("
        for lines_in_dictionary_form in list_of_dictionaries:
            for keys in lines_in_dictionary_form:#loop for column names
                SQL_string += str(keys) + ","
            SQL_string = SQL_string[:-1] + ") VALUES(" #SQL_string[:-1] removes last comma 
            
            for keys in lines_in_dictionary_form: #loop again to get column values (all values are CHARS)
                if (keys == "SAVED_DATE"):
                    date_time_object = datetime.strptime(str(lines_in_dictionary_form[keys]),"%d.%m.%Y")
                    replace_dots = date_time_object.strftime("#%Y/%m/%d %H:%M:%S#")
        
                    SQL_string += replace_dots + ","

                elif (keys == "SAVED_TIME"):
                    date_time_object = datetime.strptime(str(lines_in_dictionary_form[keys]),"%H:%M:%S")
                    replace_dots = date_time_object.strftime("#%Y/%m/%d %H:%M:%S#")
        
                    SQL_string += replace_dots + ","
                else:
                    SQL_string += "'" + str(lines_in_dictionary_form[keys]) + "',"
            SQL_string = SQL_string[:-1] + ")" #SQL_string[:-1] removes last comma 
            SQL_string = SQL_string.replace(".","")
            print(SQL_string)
            self.ACCES.MultipleWriteQuery(SQL_string,[cursor_index])
            SQL_string = f"INSERT INTO {table_name} ("
        self.ACCES.MultipleUpdateDatabase([cursor_index])

    def CreateTableFromListOfDictionaries(self,list_of_dictionaries,table_name,cursor_index):
        """take list of dictionaries, and for each key in dictionary, create column of table
        with custom formating"""
        SQL_string = f"CREATE TABLE {table_name} (ID AUTOINCREMENT,"
        for keys in list_of_dictionaries[0]:#loop for column names in first row
            if (keys == "SAVED_DATE" or keys == "SAVED_TIME"):
                SQL_string += str(keys) + " DATETIME,"

            elif (keys == "LOG_ID"):
                    SQL_string += str(keys) + " VARCHAR UNIQUE,"
            else:
                SQL_string += str(keys) + " VARCHAR,"
        SQL_string = SQL_string[:-1] + ")" #SQL_string[:-1] removes last comma 
        SQL_string = SQL_string.replace(".","")
        print(SQL_string)
        self.ACCES.MultipleWriteQuery(SQL_string,[cursor_index])
        SQL_string = f"CREATE TABLE {table_name} (ID AUTOINCREMENT,"
        self.ACCES.MultipleUpdateDatabase([cursor_index])

    def storeDataIntoDatabase(self):
        self.FatchData.fetch_data() #Download data from attendance
        self.FatchData.fetch_tags()
        self.FileCorrector.correct() #Correct files

        list_of_lines_tags = self.parseSDfileToListOfDictionaries("tags_new.txt")
        list_of_lines_logs = self.parseSDfileToListOfDictionaries("logs_new.txt")
        last_LOG_ID_in_SD_card = int(list_of_lines_logs[-1]["LOG_ID"])

        ## CREATE COPPY OF SD CARD TAGS
        if self.tableAlreadyExists("OriginaTAGS",0):
            self.ACCES.MultipleWriteQuery("DROP table OriginaTAGS",[0])

        print(list_of_lines_tags)
        self.CreateTableFromListOfDictionaries(list_of_lines_tags,"OriginaTAGS",0)
        self.insertRowsFromListOfDictionaries(list_of_lines_tags,"OriginaTAGS",0)  

        ## CREATE COPPY OF SD CARD LOGS
        if self.tableAlreadyExists("OriginalSDcontent",0):
            self.ACCES.MultipleWriteQuery("DROP table OriginalSDcontent",[0])

        self.CreateTableFromListOfDictionaries(list_of_lines_logs,"OriginalSDcontent",0)
        self.insertRowsFromListOfDictionaries(list_of_lines_logs,"OriginalSDcontent",0)  

        ##UPDATE TAGS IN DB ONLY
        if 0 == self.tableAlreadyExists("tags",0): #table does NOT exist
            self.CreateTableFromListOfDictionaries(list_of_lines_tags,"tags",0)
            self.insertRowsFromListOfDictionaries(list_of_lines_tags,"tags",0) 


        ##UPDATE LOGS IN DB ONLY
        if self.tableAlreadyExists("logs",0):
            #query = """SELECT TOP 1 LOG_ID from logs WHERE EDIT = 'NONE' ORDER BY VAL(LOG_ID) DESC"""
            query = """SELECT TOP 1 LOG_ID from logs where LOG_ID not like '%E%' ORDER BY VAL(LOG_ID) DESC"""
            self.ACCES.MultipleWriteQuery(query,[0])
            last_LOG_ID_in_ACCES_DB = int(self.ACCES.MultipleResultFromQuery([0])[0][0])

            if last_LOG_ID_in_ACCES_DB <  last_LOG_ID_in_SD_card:
                print("UPDATING TABLE:")
                #to show = (MAX LOG_ID FROM UNEDITED DATABASE LOGS) - (NUMBER OF CORRECTED LINES IN SD) - (MIN LOG_ID FROM SD CARD) -> min log can start from non zero...
                to_show = last_LOG_ID_in_ACCES_DB #- len(list_of_lines_logs) - int(list_of_lines_logs[0]['LOG_ID']) + 1
                print(f"to show: {to_show} , len: {len(list_of_lines_logs)}, last: {last_LOG_ID_in_ACCES_DB}, first in SD: {list_of_lines_logs[0]['LOG_ID']}")

                #print(list_of_lines_logs[to_show])
                self.insertRowsFromListOfDictionaries(list_of_lines_logs[to_show:],"logs",0)
        else:
            self.CreateTableFromListOfDictionaries(list_of_lines_logs,"logs",0)
            self.insertRowsFromListOfDictionaries(list_of_lines_logs,"logs",0)
            last_LOG_ID_in_ACCES_DB = int(list_of_lines_logs[-1]['LOG_ID'])

        self.last_ID_in_database = last_LOG_ID_in_ACCES_DB
        self.last_ID_in_SD = int(list_of_lines_logs[-1]['LOG_ID'])

        query = """SELECT JMENO, PRIJMENI from TAGS"""
        self.ACCES.MultipleWriteQuery(query,[0])
        names = self.ACCES.MultipleResultFromQuery([0])

        months = {"Leden": 0 ,"Únor": 0 ,"Březen": 0 ,"Duben": 0 ,"Květen": 0 ,"Červen": 0 ,"Červenec": 0 ,"Srpen": 0 ,"Září": 0 ,"Říjen": 0 ,"Listopad": 0 ,"Prosinec": 0 }
        data = [{"Jmeno" : names[i][0] , "Prijmeni": names[i][1]}| months for i in range(len(names))]
        #print(data)


        ## CREATE COPPY OF MONTHS
        year = datetime.now().year
        if False == self.tableAlreadyExists(f"toNextMonth{year}",0):
            self.CreateTableFromListOfDictionaries(data,f"toNextMonth{year}",0)
            self.insertRowsFromListOfDictionaries(data,f"toNextMonth{year}",0)  
        self.ACCES.MultipleUpdateDatabase(cursor_positions=[0]) #upload all changes into database

    def createNewToNextMonthTable(self,year):
        query = """SELECT JMENO, PRIJMENI from TAGS"""
        self.ACCES.MultipleWriteQuery(query,[0])
        names = self.ACCES.MultipleResultFromQuery([0])

        months = {"Leden": 0 ,"Únor": 0 ,"Březen": 0 ,"Duben": 0 ,"Květen": 0 ,"Červen": 0 ,"Červenec": 0 ,"Srpen": 0 ,"Září": 0 ,"Říjen": 0 ,"Listopad": 0 ,"Prosinec": 0 }
        data = [{"Jmeno" : names[i][0] , "Prijmeni": names[i][1]}| months for i in range(len(names))]
        #print(data)

        if self.tableAlreadyExists(f"toNextMonth{year}",0):
            return

        self.CreateTableFromListOfDictionaries(data,f"toNextMonth{year}",0)
        self.insertRowsFromListOfDictionaries(data,f"toNextMonth{year}",0)  
        self.ACCES.MultipleUpdateDatabase(cursor_positions=[0]) #upload all changes into database

    
    def createNewVyplatitTable(self,year):
        query = """SELECT JMENO, PRIJMENI from TAGS"""
        self.ACCES.MultipleWriteQuery(query,[0])
        names = self.ACCES.MultipleResultFromQuery([0])

        months = {"Leden": 0 ,"Únor": 0 ,"Březen": 0 ,"Duben": 0 ,"Květen": 0 ,"Červen": 0 ,"Červenec": 0 ,"Srpen": 0 ,"Září": 0 ,"Říjen": 0 ,"Listopad": 0 ,"Prosinec": 0 }
        data = [{"Jmeno" : names[i][0] , "Prijmeni": names[i][1]}| months for i in range(len(names))]
        #print(data)

        if self.tableAlreadyExists(f"Vyplatit{year}",0):
            return

        self.CreateTableFromListOfDictionaries(data,f"Vyplatit{year}",0)
        self.insertRowsFromListOfDictionaries(data,f"Vyplatit{year}",0)  
        self.ACCES.MultipleUpdateDatabase(cursor_positions=[0]) #upload all changes into database







#LOAD ACCES DATABASE DRIVER

if __name__ == "__main__":
    SC = SuperClass()
    with open('config.yaml', "r") as f:
        YAML = yaml.safe_load(f)

    ACCES = SC.database.AccesDatabase
    ACCES.SimplyConnectByPath(YAML["ACCDB"])

    SynchroClass = Synchro(ACCES=ACCES,YAML=YAML)
    SynchroClass.storeDataIntoDatabase()