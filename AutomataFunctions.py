import AutomataParser

def GetPosition(id):
    for n in range(0, len(AutomataParser.Aut_State_Id_Table)):
        a = AutomataParser.Aut_State_Id_Table[n]
        if a == id:
            return(int(n))

def GetEventPosition(id):

    for n in range(0, len(AutomataParser.Aut_Event_Id_Table)):
        a = AutomataParser.Aut_Event_Id_Table[n]
        if a == id:
            positions = n

    return (positions)

def GetEventNamePosition(name):

    for n in range(0, len(AutomataParser.Aut_Event_Name_Table)):
        a = AutomataParser.Aut_Event_Name_Table[n]
        if a == name:
            positions = n

    return (positions)


def GetFaultEvent():
    Fault_Event = []
    n = 0
    for each in AutomataParser.Aut_Event_Id_Table:
        if AutomataParser.Aut_ObservableTable[n] == str(0):
            Fault_Event = each
        n = n + 1

    return(Fault_Event)


def GetFaultEventName():
    i = 0
    while i < len(AutomataParser.Aut_Event_Id_Table):
        if AutomataParser.Aut_Event_Id_Table[i] == GetFaultEvent():
            return(AutomataParser.Aut_Event_Name_Table[i])
        i += 1

def IsSelfloopOnly(estado):
   # print(estado)
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = AutomataParser.Aut_Transition_Source_Table[n]
        if a == str(estado):
            positions.append(n)
           # print(a)

    for each in positions:
        m = int(each)
        target = str(AutomataParser.Aut_Transition_Target_Table[m])
        #print(target)
        if target == estado:
            targets.append(0)
        else:
            targets.append(1)

    #print(targets)
    if targets.__contains__(1) == True:
        return(0) #return 0 means that is not only selfloop
    else:
        return(1) #only selfloop