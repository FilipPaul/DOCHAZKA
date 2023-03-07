from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem,QApplication,QHeaderView
from PyQt5.QtGui import QColor, QFont
#from PyQt5 import *
import datetime
list_of_employees = [{'Jméno:': 'Lukas', 'Příjmenní': 'Bartosek', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Milan', 'Příjmenní': 'Brzy', 'Normální doba': datetime.timedelta(0), 'Dovolená': 
datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Pavel', 'Příjmenní': 'Ceresnik', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Radomil', 'Příjmenní': 'Havlin', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Josef', 'Příjmenní': 'Hladky', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Ludek', 'Příjmenní': 'Hladky', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Ondrej', 'Příjmenní': 'Hutter', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Filip', 'Příjmenní': 'Paul', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Ludek', 'Příjmenní': 'Janderka', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Robert', 'Příjmenní': 'Kazda', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Josef', 'Příjmenní': 'Kopriva', 'Normální \
doba': datetime.timedelta(seconds=77669), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(seconds=48869), 'Celkový čas': datetime.timedelta(seconds=77669), 'Počet Chyb': 0}, {'Jméno:': 'Josef', 'Příjmenní': 'Malousek', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), \
'Počet Chyb': 0}, {'Jméno:': 'Martin', 'Příjmenní': 'Petr', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Lubomir', 'Příjmenní': 'Petrik', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Petra', 'Příjmenní': 'Spacilova', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Ondrej', 'Příjmenní': 'Vainlich', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), \
'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}, {'Jméno:': 'Petr', 'Příjmenní': 'Zouhar', 'Normální doba': datetime.timedelta(0), 'Dovolená': datetime.timedelta(0), 'Lékař': datetime.timedelta(0), 'Nemocenská': datetime.timedelta(0), 'Pracovní Cesty': datetime.timedelta(0), 'Pochůzky': datetime.timedelta(0), 'Přesčasy': datetime.timedelta(0), 'Celkový čas': datetime.timedelta(0), 'Počet Chyb': 0}]


def makeOverview(table_widget:QTableWidget, list_of_employees:list):
    header = []
    for keys in list_of_employees[0]:
        header.append(keys)

    columns = len(header)
    rows = len(list_of_employees)
    table_widget.clear()
    table_widget.setColumnCount(columns)
    table_widget.setHorizontalHeaderLabels(header)#Fill Headers with predefined values
    table_widget.setRowCount(rows)
    table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    for i in range(columns):
        table_widget.horizontalHeaderItem(i).setFont(QFont("Segoe UI", pointSize=12))
    

    col = 0

    for col_name in header:
        row = 0
        for row_in_list in list_of_employees:
            #print(row_in_list)
            if type(row_in_list[col_name]) == datetime.timedelta:
                item = QTableWidgetItem(f"{row_in_list[col_name].total_seconds()/3600 :.2f} h")
            else:
                item = QTableWidgetItem(str(row_in_list[col_name]))
            print(f" row: {row}   column: {col}  ITEM: {row_in_list[col_name]}")

            if row_in_list["Počet Chyb"] > 0:
                item.setBackground(QColor(220,120,120,20)) #print it bright red
                item.setForeground(QColor(141, 204, 169))
            else:
                item.setBackground(QColor(120,220,120,180)) #print it green
                item.setForeground(QColor(55,55,55))

            table_widget.setItem(row,col,item)
            row += 1
        col += 1



QApp = QApplication([])
table = QTableWidget()
    #for col in range(columns):
    #    for row in range(rows):
    #        item = QTableWidgetItem("ASFFSA")
    #        table_widget.setItem(col, row, item)
            


    #header.append(f"{employees['Prijmeni']} {employees['Jmeno']}")
    #print(list_of_employees)
    #print(tableWidget)

makeOverview(table, list_of_employees)
