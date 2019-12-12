import AutomataParser
import DiagnoserParser
import AutomataFunctions
import DiagnoserFunctions
import DefineStrings
import FU_s


# metodo para pegar a posição em source em que está o estado 2

def GetSourcePosition(id_estado):
    n = 0
    positions = []
    for each in AutomataParser.Aut_Transition_Source_Table:
        if each == id_estado:
            positions.append(n)
        n = n + 1

    return (positions)


# metodo para pegar os eventos no automato correspondetes ao estado
def GetEventsAfterState(positions):
    events = []
    for each in positions:
        events.append(AutomataParser.Aut_Transition_Event_Table[each])

    return (events)


# metodo para pegar os próximos estados no automato
def GetStatesAfterEstate(positions):
    states = []
    for each in positions:
        states.append(AutomataParser.Aut_Transition_Target_Table[each])

    return (states)


# nethod to define starting state
def GetStartingStates():
    Starting_States = []
    Faul_Events_Position = []
    Faul_Events_Position = DefineStrings.GetFaultEventsPosition()

    for each in Faul_Events_Position:
        Starting_States.append(AutomataParser.Aut_Transition_Target_Table[each])

    return (Starting_States)


# Returns the events sequence after a fault
def GetAutomataPathToAnalyse(FU_s_position):
    states = []
    temp = GetStartingStates()
    state = temp[FU_s_position]
    positions = []
    events = []
    aux = []
    aux_2 = []
    states.append(state)

    for each in states:
        if AutomataFunctions.IsSelfloopOnly(each) == 0:
            positions = GetSourcePosition(each)
            aux = GetEventsAfterState(positions)
            for cada in aux:
                if events.__contains__(cada) == False:
                    events.append(cada)
            aux_2 = GetStatesAfterEstate(positions)
            for cada in aux_2:
                if states.__contains__(cada) == False:
                    states.append(cada)

    return (events)


# define os nomes dos evento no automato
def GetAutomataEventsNames(FU_s_):
    events_names = []
    events = GetAutomataPathToAnalyse(FU_s_)
    for each in events:
        n = 0
        for cada in AutomataParser.Aut_Event_Id_Table:
            if cada == each:
                if events_names.__contains__(AutomataParser.Aut_Event_Name_Table[n]) == False:
                    events_names.append(AutomataParser.Aut_Event_Name_Table[n])
            n = n + 1

    return (events_names)


def GetFC_s_IDs(string):  # gets the FC(s) for a given string number

    FU_s_StateNames = FU_s.Get_FU_s()

    # for this string only, getting the FU(s):
    FU_s_StateIDs = []
    FU_s_StateIDs.append(DiagnoserFunctions.GetStateId(FU_s_StateNames[string]))

    # and getting the reachable states for this string in ID
    string_states_IDs = DefineStrings.GetReachable(FU_s_StateIDs[0])

    # getting the names
    string_states_names = []
    for each in string_states_IDs:
        string_states_names.append(DiagnoserFunctions.GetStateName(each))

    # ignoring the non-certain ones
    the_certain_IDs = []
    i = 0
    while i < len(string_states_names):
        if DiagnoserFunctions.IsCertain(string_states_names[i]):
            the_certain_IDs.append(string_states_IDs[i])
        i += 1

    # and verifying if they lead to each other to ignore the target ones (once they're not the first ones)
    is_first = []
    for each in the_certain_IDs:
        i = 0
        first = True
        while i < len(DiagnoserParser.Transition_Target_Table):
            if (each == DiagnoserParser.Transition_Target_Table[i]
                    and DiagnoserParser.Transition_Source_Table[i] != each
                    and DiagnoserParser.Transition_Source_Table[i] in the_certain_IDs):
                first = False
            i += 1
        is_first.append(first)
    FC_s = []
    i = 0
    while i < len(the_certain_IDs):
        if is_first[i]:
            FC_s.append(the_certain_IDs[i])
        i += 1

    return (FC_s)

