class toNextMonthHandler:
    def __init__(self,ACCES):
        self.ACCES = ACCES

        query = """SELECT JMENO, PRIJMENI from TAGS"""
                self.ACCES.MultipleWriteQuery(query,[0])
                names = self.ACCES.MultipleResultFromQuery([0])

                months = {"Leden": 0 ,"Únor": 0 ,"Březen": 0 ,"Duben": 0 ,"Květen": 0 ,"Červen": 0 ,"Červenec": 0 ,"Srpen": 0 ,"Září": 0 ,"Říjen": 0 ,"Listopad": 0 ,"Prosinec": 0 }
                data = [{"Jmeno" : names[i][0] , "Prijemni": names[i][1]}| months for i in range(len(names))]
                #print(data)


                ## CREATE COPPY OF MONTHS
                year = datetime.now().year
                if self.tableAlreadyExists(f"toNextMonth{year}",0):
                    self.ACCES.MultipleWriteQuery(f"DROP table toNextMonth{year}",[0])

                self.CreateTableFromListOfDictionaries(data,f"toNextMonth{year}",0)
                self.insertRowsFromListOfDictionaries(data,f"toNextMonth{year}",0)  
                self.ACCES.MultipleUpdateDatabase(cursor_positions=[0]) #upload all changes into database