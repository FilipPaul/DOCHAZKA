import pandas as pd
import datetime
import pickle
import calendar
from PyQt5.QtWidgets import QTableWidget



class ToExcellFromSingleDays:
    def __init__(self, data :dict, month:int, save_path:str = "dochazka.xlsx"):
        self.data = data
        self.path = save_path
        self.month = month
        self.table_data = None
        self.employee_Summary = None

    def translateMonths(self,month):
        month = month.replace("January","Leden")
        month = month.replace("February","Únor")
        month = month.replace("March","Březen")
        month = month.replace("April","Duben")
        month = month.replace("May","Květen")
        month = month.replace("June","Červen")
        month = month.replace("July","Červenec")
        month = month.replace("August","Srpen")
        month = month.replace("September","Září")
        month = month.replace("October","Říjen")
        month = month.replace("November","Listopad")
        month = month.replace("December","Prosinec")
        return month
    
    def timeDeltaToHoursOnly(self,td :datetime.timedelta):
            if td == "CHYBA":
                return "CHYBA"
            seconds = td.total_seconds()
            sign = ""
            if seconds < 0:
                sign = "-"
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return '{:02}:{:02}'.format(int(hours), int(minutes))


    def printTableToExcell(self):
        employee_list = []
        list_of_panda_frames = []
        for employee in self.table_data:
            employee_list.append(employee)
            pandaFrameForEmployee = pd.DataFrame(self.table_data[employee])
            list_of_panda_frames.append(pandaFrameForEmployee)
        
        with pd.ExcelWriter(self.path) as writer:
            i = 0
            for pandaFrame in list_of_panda_frames:
                dataFrame : pd.DataFrame = pandaFrame

                dataFrame.to_excel( writer, sheet_name=employee_list[i], float_format= "%.2f", startrow = 5,)
                infoFrame = pd.DataFrame([["Jméno:",employee_list[i]],["Měsíc:", self.translateMonths(calendar.month_name[self.month])]],columns = ["",""])
                infoFrame.to_excel(writer, sheet_name=employee_list[i], startrow = 0, index = False)
                i += 1

            

    def printToExcell(self):

        load_header = []
        for employees in self.data:
            for keys in self.data[employees]["1"]:
                load_header.append(keys)
            break

        list_of_panda_frames =[]
        employee_list = []
        for employees in self.data:
            list_of_doctor = []
            list_of_odchod = []
            list_of_holliday = []
            list_of_sick_days = []
            list_of_short_work_rides = []
            list_of_work_rides = []
            list_of_days = []
            list_of_celkem_with_meals = []
            list_of_celkem_without_meals = []
            list_of_meals = []
            list_of_jine = []
            list_of_omluv_absence = []
            employee_list.append(employees)
            for days in self.data[employees]:
                if "p" in days or "P" in days: #all strings like celkový přesčas has P in itsname.. others are just days
                    continue

                list_of_days.append(f"{str(days).zfill(2)}.{str(self.month).zfill(2)}")
                for keys in self.data[employees][days]:
                    if keys == "Doktor":
                        list_of_doctor.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == "Dovolena":
                        list_of_holliday.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == "Nemoc":
                        list_of_sick_days.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == "Normalni Doba":
                        list_of_odchod.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == "Pochuzka":
                        list_of_short_work_rides.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == 'Prac Cesta':
                        list_of_work_rides.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == 'Celkem s obědy':
                        list_of_celkem_with_meals.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == 'Celkem bez obědů':
                        list_of_celkem_without_meals.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
                    elif keys == 'Oběd':
                        list_of_meals.append(self.data[employees][days][keys])
                    elif keys == 'Oml Abs':
                        list_of_omluv_absence.append(self.data[employees][days][keys])
                    elif keys == 'Jine':
                        list_of_jine.append(self.timeDeltaToHoursOnly(self.data[employees][days][keys]))
            
            
            print(f"\n\nEmployee: {employees}")
            #print(f"Doktor: {len(list_of_doctor)}\nDovolena: {len(list_of_holliday)}\nNemoc: {len(list_of_sick_days)}\nOdchod: {len(list_of_odchod)}\nPochuzka: {len(list_of_short_work_rides)}\nPrac Cesta: {len(list_of_work_rides)}")
            #print(f"Days: {len(list_of_days)}")

            print(f"Header: {len(load_header)}:: {load_header}")
            pandaFrameForEmployee = pd.DataFrame([list_of_doctor,list_of_holliday,list_of_sick_days,\
                                                  list_of_odchod,list_of_short_work_rides,list_of_work_rides,\
                                                  list_of_jine,  list_of_omluv_absence,\
                                                 list_of_celkem_with_meals,list_of_meals, list_of_celkem_without_meals ],columns = list_of_days , index= load_header)
            list_of_panda_frames.append(pandaFrameForEmployee.T)
            #print(pandaFrameForEmployee.T)


        with pd.ExcelWriter(self.path) as writer:
            i = 0
            for pandaFrame in list_of_panda_frames:
                dataFrame : pd.DataFrame = pandaFrame

                dataFrame.to_excel( writer, sheet_name=employee_list[i], float_format= "%.2f", startrow = 5,)
                infoFrame = pd.DataFrame([["Jméno:",employee_list[i]],["Měsíc:", self.translateMonths(calendar.month_name[self.month])]],columns = ["",""])
                infoFrame.to_excel(writer, sheet_name=employee_list[i], startrow = 0, index = False)
                i += 1

            for employees in self.employee_Summary:
                print(employees)
                print(self.employee_Summary[employees])
                summaryFrame = pd.DataFrame(self.employee_Summary[employees], index= [""])
                summaryFrame.to_excel(writer, sheet_name=employees, startrow = 37, startcol = 0, index = True)


if __name__ == "__main__":
    with open("DochazkaÚnor.pkl", "rb") as f:
        data = pickle.load(f)


    with open("Dochazka_table_Únor.pkl", "rb") as f:
        data2 = pickle.load(f)

    with open("employee_summary_dict_Únor.pkl", "rb") as f:
        data3 = pickle.load(f)

    EXCELL = ToExcellFromSingleDays(data, 11)
    EXCELL.employee_Summary = data3
    #EXCELL.table_data = data2
    #EXCELL.printToExcell()
    #EXCELL.printTableToExcell()
    EXCELL.data = data
    #print(EXCELL.data["Filip Paul"])
    EXCELL.printToExcell()