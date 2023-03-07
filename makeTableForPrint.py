
from PyQt5.QtWidgets import QTableWidget,QApplication

def makeTableForPrint(table_widget:QTableWidget):
    list_of_dates = []
    header  = []
    list_of_hours = []
    list_of_dict_stavs =  [{} for i in range(table_widget.rowCount())]
    for cols in range(table_widget.columnCount()):
        header.append(table_widget.horizontalHeaderItem(cols).text())

    
    col = 0
    for column_name in header:
        if column_name in "GEN_DATE":
            for rows in range(table_widget.rowCount()):
                list_of_dates.append(table_widget.item(rows,col).text())

        if column_name in "CELKEM HODIN":
            for rows in range(table_widget.rowCount()):
                list_of_hours.append(table_widget.item(rows,col).text())

        if "STAV" in column_name :
            for rows in range(table_widget.rowCount()):
                list_of_dict_stavs[rows][column_name] = f"{table_widget.item(rows,col).text()} {table_widget.item(rows,col+1).text()}"

        col += 1


    l = "{"
    r = "}"
    bck = "\\"


    table_string = ""
    for i in range(len(list_of_dates)):
        pruchod_string = ""
        for keys in list_of_dict_stavs[i]:
            if list_of_dict_stavs[i][keys] != " ":
                pruchod_string += f" {list_of_dict_stavs[i][keys]} |"

        table_string += f"{list_of_dates[i].replace('svátek','sv')} & {pruchod_string[:-1]} & {list_of_hours[i]}  {bck}{bck} {bck}hline\n"

    return table_string

QApp = QApplication([])
table = QTableWidget()
    #for col in range(columns):
    #    for row in range(rows):
    #        item = QTableWidgetItem("ASFFSA")
    #        table_widget.setItem(col, row, item)
            


    #header.append(f"{employees['Prijmeni']} {employees['Jmeno']}")
    #print(list_of_employees)
    #print(tableWidget)

makeTableForPrint(table)
