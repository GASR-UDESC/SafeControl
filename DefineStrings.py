import copy

import AutomataParser
import AutomataFunctions
import DiagnoserParser
import DiagnoserFunctions


def GetFaultEventsPosition():
    Fault_Events = []
    Fault_Event = AutomataFunctions.GetFaultEvent()

    x = 0
    for each in AutomataParser.Aut_Transition_Event_Table:
        if each == Fault_Event:
            Fault_Events.append(x)
        x = x + 1

    return (Fault_Events)


def GetLastState(state):
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = str(AutomataParser.Aut_Transition_Target_Table[n])
        if state == a:
            positions.append(n)

    for each in positions:
        m = int(each)
        target = AutomataParser.Aut_Transition_Source_Table[m]
        targets.append(target)

    return (targets)


def GetLastEvent(state):
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = str(AutomataParser.Aut_Transition_Target_Table[n])
        if state == a:
            positions.append(n)

    for each in positions:
        m = int(each)
        target = AutomataParser.Aut_Transition_Event_Table[m]
        targets.append(target)

    return (targets)


def GetOneLastEvent(state):
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = str(AutomataParser.Aut_Transition_Target_Table[n])
        if state == a:
            positions.append(n)

    for each in positions:
        m = int(each)
        target = AutomataParser.Aut_Transition_Event_Table[m]
        targets.append(target)

    return (targets[0])


def GetNextStatesInID(state):
    x = len(AutomataParser.Aut_Transition_Source_Table)
    positions = []
    targets = []

    for n in range(0, x):
        a = str(AutomataParser.Aut_Transition_Source_Table[n])
        if state == a:
            positions.append(n)

    for each in positions:
        m = int(each)
        target = AutomataParser.Aut_Transition_Target_Table[m]
        targets.append(target)

    return (targets)


def GetString(position):
    answer = []
    state = AutomataParser.Aut_Transition_Target_Table[position]
    PastStatesIds = GetLastState(state)
    status = False
    while status != True:
        for each in PastStatesIds:
            if each == '1':
                status = True
            else:
                state_id = GetLastState(each)
                event_id = GetLastEvent(each)
                for cada in state_id:
                    if cada == state:
                        break  # ignoring post loop
                    if PastStatesIds.__contains__(cada) == False:
                        PastStatesIds.append(cada)
                for event in event_id:
                    if cada == state:
                        break  # ignoring post loop
                    if answer.__contains__(event) == False:
                        answer.append(event)
    return answer


def GetDiagnoserString(targetID):  # returns all strings between initial state and targetID
    initial_state = DiagnoserParser.Initial_State_ID
    seq = GetDiagnoserStringBtw(initial_state, targetID)
    ret = []

    for each in seq[0]:
        for one in each:
            ret.append(one)
    return ret

    # TODO:
    # this was a test for returning one more string when the same fault has two strings to it
    # it worked, but it is needed to adapt the rest of the code to work with its new way of returning.
    # i = 0
    # while i<len(seq):
    #     hold = []
    #     for each in seq[i]:
    #         for one in each:
    #             hold.append(one)
    #     ret.append(hold)
    #     i += 1
    # return ret


def GetDiagnoserStringBtw(sourceID,targetID):  # returns all strings between sourceID and targetID
    Event_Sequence = []
    # runs only if it is possible to reach it (returns [] if there is no possible string)
    if targetID in GetReachable(sourceID):
        State_Sequence = [[sourceID]]
        state = sourceID
        actual_state = state
        actual_way = 0
        way_num = 1
        status = False
        while not status:
            # get next states from actual state
            NextStatesIds = DiagnoserFunctions.GetNextStatesInID(actual_state)
            NextState = []
            n = 0
            for each in NextStatesIds:
                targets = GetReachable(each)
                # if it is possible to reach target from these next states, save it
                # conditions: ( (state can reach targetID) OR state is targetID) AND state is not already on the way)
                # third condition is to prevent it to stop on a loop
                if ((targetID in targets) or (each == targetID)) and (each not in State_Sequence[actual_way]):
                    NextState.append(each)
                    n += 1
            # if more then one next state was saved, increases the number of ways to get to the target
            way_num += len(NextState) -1

            # and copy actual way how many times it's needed
            i = 1
            while i < len(NextState):
                State_Sequence.insert(i+actual_way,copy.deepcopy(State_Sequence[actual_way]))
                i += 1

            #save the next states on respectives copied ways
            i = actual_way
            for each in NextState:
                State_Sequence[i].append(each)
                i += 1
            x = State_Sequence[actual_way][-1]

            # if ended one string, go to the next one
            if State_Sequence[actual_way][-1] == targetID:
                actual_way += 1
            # if still have strings to test, update actual_state to last one
            if actual_way < len(State_Sequence):
                actual_state = State_Sequence[actual_way][-1]
            # and if there is no more strings to test, end it
            else:
                status = True

        # getting the events for the state sequence
        i = 0
        while i < len(State_Sequence):
            answer = []
            j = 0
            while j < len(State_Sequence[i])-1:
                answer.append(DiagnoserFunctions.GetEventBetween(State_Sequence[i][j], State_Sequence[i][j+1]))
                j += 1
            Event_Sequence.append(answer)
            i += 1

    return (Event_Sequence)


def GetStringsToFault():
    fault_events = GetFaultEventsPosition()

    # gets the sequence of events that lead to fault on automata
    fault_aut_strings = []
    for each in fault_events:
        y = GetString(each)
        fault_aut_strings.append(y)
    i = 0
    rows = len(fault_aut_strings)
    while i < rows:
        fault_aut_strings[i] = list(reversed(fault_aut_strings[i]))
        i += 1

    # gets the same sequence for diagnoser (event IDs may be different)
    fault_diag_strings = []
    i = 0
    while i < (len(fault_aut_strings)):
        diag_string = []
        for each in fault_aut_strings[i]:
            x = DiagnoserFunctions.GetEquivalentDiagEventFromAut(each)
            diag_string.append(x)
        fault_diag_strings.append(diag_string)
        i += 1
    i += 1

    return fault_aut_strings, fault_diag_strings


def GetDiagStates(diag_eventstrings_IDs):  # gets the sequence of diagnoser's states for a given event sequence
    sequence = []
    diag_fault_statestring_IDs = []
    i = 0
    while i < len(diag_eventstrings_IDs):
        seq_row = [DiagnoserParser.Initial_State_ID]
        j = 0
        while j < len(diag_eventstrings_IDs[i]):
            x = DiagnoserFunctions.GetNextState(seq_row[j], diag_eventstrings_IDs[i][j])
            seq_row.append(x)
            j += 1
        sequence.append(seq_row)
        i += 1
        diag_fault_statestring_IDs.append(seq_row)

    return diag_fault_statestring_IDs


def GetStatePosition(state):
    positions = []
    i = 0
    while i < len(DiagnoserParser.Transition_Target_Table):
        if DiagnoserParser.Transition_Target_Table[i] == state:
            positions.append(i)
        i += 1
    return positions



def DiagIDtoName(diag_statestrings_IDs):  # gets the names of diagnoser's states for a given ID sequence
    diag_fault_statestring_names = []
    i = 0
    while i < len(diag_statestrings_IDs):
        seq_row = []
        for each in diag_statestrings_IDs[i]:
            x = DiagnoserFunctions.GetStateName(each)
            seq_row.append(x)
        diag_fault_statestring_names.append(seq_row)
        i += 1
    return diag_fault_statestring_names


def IsNextStateUncertain(diag_fault_statestring_ID):  # evaluate if next state is uncertain and add it to the fault sequence if it is
    last_state = []
    i = 0
    rows = len(diag_fault_statestring_ID)
    while i < rows:
        last_state.append(diag_fault_statestring_ID[i][-1])
        i += 1
    i = 0
    end_loop = [['no'], ['no']]
    while i < rows:
        for ended in end_loop:
            while ended == ['no']:
                a = DiagnoserFunctions.GetNextStatesInID(last_state[i])
                for each in a:
                    b = DiagnoserFunctions.GetStateName(each)
                    if DiagnoserFunctions.IsUncertain(b) and each not in diag_fault_statestring_ID[i]:
                        last_state[i] = each
                        end_loop[i] = ['no']
                        diag_fault_statestring_ID[i].append(each)
                        break  # because of that, this will not work if more then one way is uncertain
                    else:
                        end_loop[i] = ['yes']
                ended = end_loop[i]
        i += 1
    return diag_fault_statestring_ID


def IsNormalCycle(diag_statestring_IDs):  # find uncertain loop in a given string
    # mark all uncertain states on each string
    Normal_Diag_States = []
    i = 0
    while i < len(diag_statestring_IDs):
        normalstates = []
        for each in diag_statestring_IDs[i]:
            b = DiagnoserFunctions.GetStateName(each)
            if DiagnoserFunctions.IsNormal(b):
                normalstates.append(1)
            else:
                normalstates.append(0)
        Normal_Diag_States.append(normalstates)
        i += 1

    # for each uncertain state, check for a loop to other uncertain state that is also on the given string
    # loops are searched only backwards
    Normal_Diag_Loop = []
    ret = False
    i = 0
    while i < len(Normal_Diag_States):
        j = 0
        NormalLoop = []
        while j < len(Normal_Diag_States[i]):
            if Normal_Diag_States[i][j] == 1:
                state_id = diag_statestring_IDs[i][j]
                the_targets = GetDiagStateTarget(state_id)
                targets = []
                for each in the_targets:
                    if each in diag_statestring_IDs[i]:
                        targets.append(each)
                normalloop = False
                for each_target in targets:
                    for each_state in diag_statestring_IDs[i]:
                        if each_state == each_target:
                            normalloop = True
                            ret = True
                        elif each_state == state_id:
                            break
                NormalLoop.append(normalloop)
            else:
                NormalLoop.append(False)
            j += 1
        Normal_Diag_Loop.append(NormalLoop)
        i += 1
    return Normal_Diag_Loop


def IsUncertainCycle(diag_statestring_IDs):  # find uncertain loop in a given string
    # mark all uncertain states on each string
    Uncertain_Diag_States = []
    i = 0
    while i < len(diag_statestring_IDs):
        uncertainstates = []
        for each in diag_statestring_IDs[i]:
            b = DiagnoserFunctions.GetStateName(each)
            if DiagnoserFunctions.IsUncertain(b):
                uncertainstates.append(1)
            else:
                uncertainstates.append(0)
        Uncertain_Diag_States.append(uncertainstates)
        i += 1

    # for each uncertain state, check for a loop to other uncertain state that is also on the given string
    # loops are searched only backwards
    Uncertain_Diag_Loop = []
    ret = False
    i = 0
    while i < len(Uncertain_Diag_States):
        j = 0
        UncertainLoop = []
        while j < len(Uncertain_Diag_States[i]):
            if Uncertain_Diag_States[i][j] == 1:
                state_id = diag_statestring_IDs[i][j]
                the_targets = GetDiagStateTarget(state_id)
                targets = []
                for each in the_targets:
                    if each in diag_statestring_IDs[i]:
                        targets.append(each)
                uncertainloop = False
                for each_target in targets:
                    for each_state in diag_statestring_IDs[i]:
                        if each_state == each_target:
                            uncertainloop = True
                            ret = True
                        elif each_state == state_id:
                            break
                UncertainLoop.append(uncertainloop)
            else:
                UncertainLoop.append(False)
            j += 1
        Uncertain_Diag_Loop.append(UncertainLoop)
        i += 1
    return Uncertain_Diag_Loop


def GetDiagStateTarget(state):  # get all targets of a given state
    source_table = DiagnoserParser.Transition_Source_Table
    target_table = DiagnoserParser.Transition_Target_Table

    size = len(source_table)
    i = 0
    target = []

    while i < size:
        if source_table[i] == state:
            target.append(target_table[i])
        i += 1

    return (target)


def GetReachable(state_ID):
    string_states_IDs = []
    verified_states = []
    actual_state_ID = [state_ID]
    ended = False
    while not ended:
        for each in actual_state_ID:
            if each not in verified_states:
                verified_states.append(each)
                next_state_IDs = DiagnoserFunctions.GetNextStatesInID(each)
            for each in next_state_IDs:
                if each not in string_states_IDs:
                    string_states_IDs.append(each)
                    actual_state_ID.append(each)
        ended = True
    return string_states_IDs


def AreAllWaysControllable(stateID1,stateID2):
    # returns True if all substrings between the states has a controllable event

    event_string = GetDiagnoserStringBtw(stateID1,stateID2)

    #finding if any event between the states is controllable
    i = 0
    retval = True
    while i < len(event_string):
        test = False
        for each in event_string[i]:
            if DiagnoserFunctions.EventIsControllable(each[0]):
                test = True
        if not test:
            retval = False
        i += 1

    return retval

