import xlsxwriter


workbook = xlsxwriter.Workbook("dochazka.xlsx")
worksheet = workbook.get_worksheet_by_name("Filip Paul")
worksheet.write('A1', 'Jméno:')
worksheet.write('A2', "Filip Paul")
worksheet.write('A3','Měsíc')
worksheet.write('B3', "unor")
workbook.close()