from AutomateSuperPackage.AutomateSuperModule import SuperClass

query = "SELECT Leden FROM toNextMonth2023 WHERE JMENO = 'Lukas' AND Prijmeni = 'Bartosek'"
SC = SuperClass()
ACCES = SC.database.AccesDatabase
ACCES.SimplyConnectByPath("database.accdb")

ACCES.WriteQuery(query)
print(ACCES.ResultFromQuery())


def getLastLogID():
    query = "SELECT LOG_ID from logs WHERE EDIT <> 'NONE'"
    ACCES.WriteQuery(query)
    result = ACCES.ResultFromQuery()
    max_log_id = 0
    for LOG_IDs in result:
        ID = int(LOG_IDs[0].replace("E", ""))
        if max_log_id < ID:
            max_log_id = ID

        
    return max_log_id

#print(getLastLogID())
