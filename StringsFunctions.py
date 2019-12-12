import DefineStrings
import DiagnoserFunctions
import AutomataFunctions
import FU_s
import FC_s
import FB_s
import FP_s

def ConsideredStrings_Publish():

    # get FU (so I know where diagnoser is going to fail)
    FU = FU_s.Get_FU_s()

    # getting the event sequence to the fault
    i = 0
    Fault_Diag_EventStrings_IDs = []
    while i < len(FU):
        fault_state = FU[i]
        fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
        Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
        i += 1


    # getting these events names
    Fault_Aut_Strings_Names = []
    i = 0
    print('\n* Serão consideradas', len(Fault_Diag_EventStrings_IDs), 'cadeias até a falha:\n')
    while i < len(Fault_Diag_EventStrings_IDs):
        state_name = []
        for each in Fault_Diag_EventStrings_IDs[i]:
            state_name.append(DiagnoserFunctions.GetEventName(each))
        state_name.append(AutomataFunctions.GetFaultEventName())
        print('cadeia', i + 1, '=', state_name)
        Fault_Aut_Strings_Names.append(state_name)
        i += 1

def IsDiag():  # returns True if automata is diagnosable, and False if it's not

    # get FU (so I know where diagnoser is going to fail)
    FU = FU_s.Get_FU_s()

    # getting the event sequence to the fault
    i = 0
    Fault_Diag_EventStrings_IDs = []
    while i < len(FU):
        fault_state = FU[i]
        fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
        Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
        i += 1

    # getting these events names
    Fault_Aut_Strings_Names = []
    i = 0
    while i < len(Fault_Diag_EventStrings_IDs):
        state_name = []
        for each in Fault_Diag_EventStrings_IDs[i]:
            state_name.append(DiagnoserFunctions.GetEventName(each))
        state_name.append(AutomataFunctions.GetFaultEventName())
        Fault_Aut_Strings_Names.append(state_name)
        i += 1

    # getting the states to the fail by the ID
    Diag_Fault_StateString_IDs = DefineStrings.GetDiagStates(Fault_Diag_EventStrings_IDs)
    # add next states of the string if they're uncertain
    Diag_Uncertain_StateString_IDs = DefineStrings.IsNextStateUncertain(Diag_Fault_StateString_IDs)

    test = DefineStrings.IsUncertainCycle(Diag_Uncertain_StateString_IDs)
    i = 0
    IsDiagnosable = True
    while i < len(test):
        if True in test[i]:
            IsDiagnosable = False
        i += 1

    return IsDiagnosable


def IsDiag_Publish():  # returns True if automata is diagnosable, and False if it's not
    print('\n\n* DIAGNOSTICABILIDADE\n')

    # # getting the event sequence to the fault
    # Fault_Aut_EventStrings_IDs, Fault_Diag_EventStrings_IDs = DefineStrings.GetStringsToFault()

    # ******* new version
    # get FU (so I know where diagnoser is going to fail)
    FU = FU_s.Get_FU_s()

    # getting the event sequence to the fault
    i = 0
    Fault_Diag_EventStrings_IDs = []
    while i < len(FU):
        fault_state = FU[i]
        fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
        Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
        i += 1

    # getting these events names
    Fault_Aut_Strings_Names = []
    i = 0
    while i < len(Fault_Diag_EventStrings_IDs):
        state_name = []
        for each in Fault_Diag_EventStrings_IDs[i]:
            state_name.append(DiagnoserFunctions.GetEventName(each))
        state_name.append(AutomataFunctions.GetFaultEventName())
        Fault_Aut_Strings_Names.append(state_name)
        i += 1

    # getting the states to the fail by the ID
    Diag_Fault_StateString_IDs = DefineStrings.GetDiagStates(Fault_Diag_EventStrings_IDs)
    # add next states of the string if they're uncertain
    Diag_Uncertain_StateString_IDs = DefineStrings.IsNextStateUncertain(Diag_Fault_StateString_IDs)
    # get the names for the state string
    Diag_Uncertain_StateString_Names = DefineStrings.DiagIDtoName(Diag_Fault_StateString_IDs)

    test = DefineStrings.IsUncertainCycle(Diag_Uncertain_StateString_IDs)
    i = 0
    IsDiagnosable = True
    while i < len(test):
        if True in test[i]:
            IsDiagnosable = False
            index = test[i].index(True)
            print('A cadeia', i + 1, 'possui um ciclo indeterminado em [', Diag_Uncertain_StateString_Names[i][index],
                  '] e, portanto, não é diagnosticável.')
        else:
            print('A cadeia', i + 1, 'não possui ciclo indeterminado e, portanto, é diagnosticável.')
        i += 1

    if IsDiagnosable == True:
        print('\nA linguagem é diagnosticável.')
    else:
        print('\nA linguagem não é diagnosticável.')

    return IsDiagnosable


def IsSafeDiag():
    if IsDiag():
        strings = FU_s.GetStringPath()

        # run one time for each string
        FC_s_IDs = []
        string_num = 0
        while string_num < len(strings):
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1

        # getting the bad states
        Bad_State = []
        i = 0
        while i < len(FC_s_Names):
            isbad = []
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each):
                    isbad.append(False)
                else:
                    isbad.append(True)
            Bad_State.append(isbad)
            i += 1

        i = 0
        diag_seg = True
        while i < len(strings):
            if True in Bad_State[i]:
                diag_seg = False
            i += 1

        return diag_seg

    else:
        return False


def IsSafeDiag_Publish():
    print('\n\n* DIAGNOSTICABILIDADE SEGURA\n')

    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath()

        # run one time for each string
        FC_s_IDs = []
        string_num = 0
        while string_num < len(strings):
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1

        # getting the bad states for each string
        Bad_State = []
        i = 0
        while i < len(FC_s_Names):
            isbad = []
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each):
                    isbad.append(False)
                else:
                    isbad.append(True)
            Bad_State.append(isbad)
            i += 1

        print('Para cada cadeia da linguagem, calcula-se o FC(s)\n')
        i = 0
        diag_seg = True
        while i < len(strings):
            print('FC(', i + 1, ') =', FC_s_Names[i])
            if True in Bad_State[i]:
                j = Bad_State[i].index(True)
                print('O estado [', FC_s_Names[i][j], '] é um Bad State.',
                      'Portanto, a cadeia', i + 1, 'não é diagnosticável segura.\n')
                diag_seg = False
            else:
                print('A cadeia', i + 1, 'não possui Bad States no FC, portanto é diagnosticável segura.\n')
            i += 1

        if diag_seg:
            print('A linguagem é diagnosticável segura.')
        else:
            print('A linguagem não é diagnosticável segura.')

        return diag_seg

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é diagnosticável segura, pois não é diagnosticável em primeiro lugar.')
        return False


def IsPred():

    # if it is Language Diagnosable:
    if IsDiag():

        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()
        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetReachable(each_name))

        # test if there is any Normal or Uncertain Cycle
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable)

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # calculating the answers
        i = 0
        IsPredictable = True
        while i < len(test_normal):
            if True in test_normal[i]:
                IsPredictable = False
            elif True in test_uncertain[i]:
                IsPredictable = False
            i += 1

        return IsPredictable

    # if it is not Language Diagnosable:
    else:
        return False


def IsPred_Publish():
    print('\n\n* PROGNOSTICABILIDADE\n')

    # if it is Language Diagnosable:
    if IsDiag():

        # # publishing only
        # Fault_Aut_EventStrings_IDs, Fault_Diag_EventStrings_IDs = DefineStrings.GetStringsToFault()

        # ******* new version
        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s()

        # getting the event sequence to the fault
        i = 0
        Fault_Diag_EventStrings_IDs = []
        while i < len(FU):
            fault_state = FU[i]
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
            i += 1

        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            i += 1

        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()
        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetReachable(each_name))

        # test if there is any Normal or Uncertain Cycle (C condition)
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable)

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # calculating and printing the answers
        i = 0
        IsPredictable = True
        while i < len(test_normal):
            if True in test_normal[i]:
                IsPredictable = False
                index = test_normal[i].index(True)
                print('A cadeia', i + 1, 'possui um ciclo normal em [',
                      Reachable_Names[i][index],
                      '] e, portanto, não é prognosticável.\n')
            elif True in test_uncertain[i]:
                IsPredictable = False
                index = test_uncertain[i].index(True)
                print('A cadeia', i + 1, 'possui um ciclo incerto em [',
                      Reachable_Names[i][index],
                      '] e, portanto, não é prognosticável.\n')
            else:
                print('A cadeia', i + 1, 'não possui ciclo incerto ou normal e, portanto, é prognosticável.\n')
            i += 1

        if IsPredictable == True:
            print('A linguagem é prognosticável.')
        else:
            print('A linguagem não é prognosticável.')

        return IsPredictable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é prognosticável, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiag():

    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath()

        # getting the FC states
        FC_s_IDs = []
        string_num = 0
        while string_num < len(strings):
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1

        # getting the FB states
        i = 0
        FB_s_IDs = []
        while i<len(strings):
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i))
            i += 1

        # getting FB(s) names
        FB_s_Names = []
        i = 0
        while i < len(FB_s_IDs):
            names = []
            for each in FB_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FB_s_Names.append(names)
            i += 1

        # * first condition is: FC can not be a bad state

        # searching for bad states in FC
        Bad_State = []
        i = 0
        while i < len(FC_s_Names):
            isbad = []
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each):
                    isbad.append(False)
                else:
                    isbad.append(True)
            Bad_State.append(isbad)
            i += 1

        # * second condition is: sub-strings must have a controllable state between a FC and a FB

        # getting reachable for each FC
        Sub_Strings_IDs = []
        i = 0
        while i < len(FC_s_IDs):
            reachable = []
            for each in FC_s_IDs[i]:
                reachable.append(DefineStrings.GetReachable(each))
            Sub_Strings_IDs.append(reachable)
            i += 1

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0
        while i < len(Sub_Strings_IDs):
            j = 0
            bad_sub = []
            while j < len(Sub_Strings_IDs[i]):
                bad_subsub = []
                for each in Sub_Strings_IDs[i][j]:
                    if each in FB_s_IDs[i]:
                        bad_subsub.append(each)
                bad_sub.append(bad_subsub)
                j += 1
            the_bads_IDs.append(bad_sub)
            i += 1

        i = 0
        Controllability = []
        while i < len(FC_s_IDs):
            j = 0
            contr = []
            while j < len(FC_s_IDs[i]):
                cont = []
                for each in the_bads_IDs[i][j]:
                    cont.append(DefineStrings.AreAllWaysControllable(FC_s_IDs[i][j],each))
                j += 1
                contr.append(cont)
            i += 1
            Controllability.append(contr)

        # testing both conditions:
        i = 0
        Each_String_Diag_Controllable = []
        while i < len(strings):
            Each_String = True
            if True in Bad_State[i]:
                Each_String = False
            elif False in Controllability[i][0]:
                Each_String = False
            Each_String_Diag_Controllable.append(Each_String)
            i += 1

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        return False


def IsSafeControlByDiag_Publish():
    print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE\n')

    # if it is Language Diagnosable:
    if IsDiag():
        strings = FU_s.GetStringPath()

        # # publishing only
        # Fault_Aut_EventStrings_IDs, Fault_Diag_EventStrings_IDs = DefineStrings.GetStringsToFault()

        # ******* new version
        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s()

        # getting the event sequence to the fault
        i = 0
        Fault_Diag_EventStrings_IDs = []
        while i < len(FU):
            fault_state = FU[i]
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
            i += 1


        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            i += 1

        # getting the FC states
        FC_s_IDs = []
        string_num = 0
        while string_num < len(strings):
            FC_s_IDs.append(FC_s.GetFC_s_IDs(string_num))
            string_num += 1

        # getting FC(s) names
        FC_s_Names = []
        i = 0
        while i < len(FC_s_IDs):
            names = []
            for each in FC_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FC_s_Names.append(names)
            i += 1

        # getting the FB states
        i = 0
        FB_s_IDs = []
        while i<len(strings):
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i))
            i += 1

        # getting FB(s) names
        FB_s_Names = []
        i = 0
        while i < len(FB_s_IDs):
            names = []
            for each in FB_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FB_s_Names.append(names)
            i += 1

        # * first condition is: FC can not be a bad state

        # searching for bad states in FC
        Bad_State = []
        i = 0
        while i < len(FC_s_Names):
            isbad = []
            for each in FC_s_Names[i]:
                if DiagnoserFunctions.IsNotBad(each):
                    isbad.append(False)
                else:
                    isbad.append(True)
            Bad_State.append(isbad)
            i += 1

        # * second condition is: sub-strings must have a controllable state between a FC and a FB

        # getting reachable for each FC
        Sub_Strings_IDs = []
        i = 0
        while i < len(FC_s_IDs):
            reachable = []
            for each in FC_s_IDs[i]:
                reachable.append(DefineStrings.GetReachable(each))
            Sub_Strings_IDs.append(reachable)
            i += 1

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0
        while i < len(Sub_Strings_IDs):
            j = 0
            bad_sub = []
            while j < len(Sub_Strings_IDs[i]):
                bad_subsub = []
                for each in Sub_Strings_IDs[i][j]:
                    if each in FB_s_IDs[i]:
                        bad_subsub.append(each)
                bad_sub.append(bad_subsub)
                j += 1
            the_bads_IDs.append(bad_sub)
            i += 1

        i = 0
        Controllability = []
        while i < len(FC_s_IDs):
            j = 0
            contr = []
            while j < len(FC_s_IDs[i]):
                cont = []
                for each in the_bads_IDs[i][j]:
                    cont.append(DefineStrings.AreAllWaysControllable(FC_s_IDs[i][j],each))
                j += 1
                contr.append(cont)
            i += 1
            Controllability.append(contr)

        # testing and publishing both conditions:
        i = 0
        Is_Controllable_By_Diagnosis = True
        Each_String_Diag_Controllable = []
        while i < len(strings):
            Each_String = True
            print('Para a cadeia', i + 1, 'calcula-se o FC(s) e o FB(s)')
            print('FC(', i + 1, ') =', FC_s_Names[i])
            print('FB(', i + 1, ') =', FB_s_Names[i],'\n')
            if True in Bad_State[i]:
                j = Bad_State[i].index(True)
                print('O estado', FC_s_Names[i][j], 'é um Bad State.',
                      '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela diagnose.\n')
                Is_Controllable_By_Diagnosis = False
                Each_String = False
            elif False in Controllability[i][0]:
                j = Controllability[i][0].index(False)
                print('No conjunto de eventos que ocorre entre o estado FC(', i + 1, ') = [', FC_s_Names[i][j], ']',
                      'e o estado FB(', i + 1, ') = [', FB_s_Names[i][j],'] não há um evento controlável',
                      '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela diagnose.\n')
                Is_Controllable_By_Diagnosis = False
                Each_String = False
            else:
                print('A cadeia', i + 1, 'não possui Bad States no FC. Além disso, sempre há um evento controlável',
                      'entre um estado FC(', i + 1, ') e um estado FB(', i + 1, ').',
                      '\nPortanto, a cadeia', i + 1, 'é controlável segura pela diagnose.\n')
            Each_String_Diag_Controllable.append(Each_String)
            i += 1

        if Is_Controllable_By_Diagnosis:
            print('A linguagem é controlável segura pela diagnose.')
        else:
            print('A linguagem não é controlável segura pela diagnose.')

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é controlável segura pela diagnose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByProg():

    # if it is Language Diagnosable:
    if IsDiag():

        # * first condition is C condition

        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()
        FU_states_ID = []
        for each in FU_states:
            FU_states_ID.append(DiagnoserFunctions.GetStateId(each))
        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetReachable(each_name))

        # test if there is any Normal or Uncertain Cycle (C condition)
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable)

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # * second condition is: sub-strings must have a controllable state between a FP and a FB

        # getting FP(s) names
        FP_s_Names = []
        for each in FU_states_ID:
            FP_s_Names.append(FP_s.GetFP_s(each))

        # getting FB(s) IDs
        FP_s_IDs = []
        i = 0
        while i < len(FP_s_Names):
            names = []
            for each in FP_s_Names[i]:
                names.append(DiagnoserFunctions.GetStateId(each))
            FP_s_IDs.append(names)
            i += 1

        # getting the FB states
        i = 0
        FB_s_IDs = []
        while i < len(FU_states):
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i))
            i += 1

        # getting FB(s) names
        FB_s_Names = []
        i = 0
        while i < len(FB_s_IDs):
            names = []
            for each in FB_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FB_s_Names.append(names)
            i += 1

        # getting reachable for each FP
        Sub_Strings_IDs = []
        i = 0
        while i < len(FP_s_IDs):
            reachable = []
            for each in FP_s_IDs[i]:
                reachable.append(DefineStrings.GetReachable(each))
            Sub_Strings_IDs.append(reachable)
            i += 1

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0
        while i < len(Sub_Strings_IDs):
            j = 0
            bad_sub = []
            while j < len(Sub_Strings_IDs[i]):
                bad_subsub = []
                for each in Sub_Strings_IDs[i][j]:
                    if each in FB_s_IDs[i]:
                        bad_subsub.append(each)
                bad_sub.append(bad_subsub)
                j += 1
            the_bads_IDs.append(bad_sub)
            i += 1

        i = 0
        control_FP_FB = []
        while i < len(FP_s_IDs):
            j = 0
            contr = []
            while j < len(FP_s_IDs[i]):
                cont = []
                for each in the_bads_IDs[i][j]:
                    cont.append(DefineStrings.AreAllWaysControllable(FP_s_IDs[i][j], each))
                j += 1
                contr.append(cont)
            i += 1
            control_FP_FB.append(contr)

        # * testing both conditions:

        # calculating and printing the answers
        i = 0
        Each_String_Diag_Controllable = []

        while i < len(FU_states):
            Each_String = True

            if True in test_normal[i]:
                Each_String = False
            elif len(FP_s_Names) == 0:
                Each_String = False
            elif True in test_uncertain[i]:
                Each_String = False
            elif False in control_FP_FB[i][0]:
                Each_String = False
            Each_String_Diag_Controllable.append(Each_String)
            i += 1

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        return False


def IsSafeControlByProg_Publish():
    print('\n\n* CONTROLABILIDADE SEGURA PELA PROGNOSE\n')

    # if it is Language Diagnosable:
    if IsDiag():

        # * first condition is C condition

        # get reachable states from FU
        FU_states = FU_s.Get_FU_s()
        FU_states_ID = []
        for each in FU_states:
            FU_states_ID.append(DiagnoserFunctions.GetStateId(each))
        Reachable = []
        for each in FU_states:
            each_name = DiagnoserFunctions.GetStateId(each)
            Reachable.append(DefineStrings.GetReachable(each_name))

        # test if there is any Normal or Uncertain Cycle (C condition)
        test_normal = DefineStrings.IsNormalCycle(Reachable)
        test_uncertain = DefineStrings.IsUncertainCycle(Reachable)

        # getting the names
        i = 0
        Reachable_Names = []
        while i < len(Reachable):
            names = []
            for each in Reachable[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            Reachable_Names.append(names)
            i += 1

        # * second condition is: sub-strings must have a controllable state between a FP and a FB

        # getting FP(s) names
        FP_s_Names = []
        for each in FU_states_ID:
            FP_s_Names.append(FP_s.GetFP_s(each))

        # getting FP(s) IDs
        FP_s_IDs = []
        i = 0
        while i < len(FP_s_Names):
            names = []
            for each in FP_s_Names[i]:
                names.append(DiagnoserFunctions.GetStateId(each))
            FP_s_IDs.append(names)
            i += 1

        # getting the FB states
        i = 0
        FB_s_IDs = []
        while i < len(FU_states):
            FB_s_IDs.append(FB_s.GetFB_s_IDs(i))
            i += 1

        # getting FB(s) names
        FB_s_Names = []
        i = 0
        while i < len(FB_s_IDs):
            names = []
            for each in FB_s_IDs[i]:
                names.append(DiagnoserFunctions.GetStateName(each))
            FB_s_Names.append(names)
            i += 1

        # getting reachable for each FP
        Sub_Strings_IDs = []
        i = 0
        while i < len(FP_s_IDs):
            reachable = []
            for each in FP_s_IDs[i]:
                reachable.append(DefineStrings.GetReachable(each))
            Sub_Strings_IDs.append(reachable)
            i += 1

        # ignoring the not-FB ones for each sub string
        the_bads_IDs = []
        i = 0
        while i < len(Sub_Strings_IDs):
            j = 0
            bad_sub = []
            while j < len(Sub_Strings_IDs[i]):
                bad_subsub = []
                for each in Sub_Strings_IDs[i][j]:
                    if each in FB_s_IDs[i]:
                        bad_subsub.append(each)
                bad_sub.append(bad_subsub)
                j += 1
            the_bads_IDs.append(bad_sub)
            i += 1

        i = 0
        control_FP_FB = []
        while i < len(FP_s_IDs):
            j = 0
            contr = []
            while j < len(FP_s_IDs[i]):
                cont = []
                for each in the_bads_IDs[i][j]:
                    cont.append(DefineStrings.AreAllWaysControllable(FP_s_IDs[i][j], each))
                j += 1
                contr.append(cont)
            i += 1
            control_FP_FB.append(contr)

        # * testing both conditions:

        # calculating and printing the answers

        i = 0
        Is_Controllable_By_Prognosis = True
        Each_String_Diag_Controllable = []

        while i < len(FU_states):
            Each_String = True
            print('Para a cadeia', i + 1, 'calcula-se o FP(s) e o FB(s)')
            print('FP(', i + 1, ') =', FP_s_Names[i])
            print('FB(', i + 1, ') =', FB_s_Names[i], '\n')

            if True in test_normal[i]:
                index = test_normal[i].index(True)
                print('A cadeia', i + 1, 'possui um ciclo normal em [',
                      Reachable_Names[i][index],
                      '] e, portanto, não é prognosticável.\n')
                Is_Controllable_By_Prognosis = False
                Each_String = False
            elif len(FP_s_Names) == 0:
                print('A cadeia', i + 1, 'não garante prognose e, portanto, não é prognosticável.\n')
                Is_Controllable_By_Prognosis = False
                Each_String = False
            elif True in test_uncertain[i]:
                index = test_uncertain[i].index(True)
                print('A cadeia', i + 1, 'possui um ciclo incerto em [',
                      Reachable_Names[i][index],
                      '] e, portanto, não é prognosticável.\n')
                Is_Controllable_By_Prognosis = False
                Each_String = False
            elif False in control_FP_FB[i][0]:
                index = control_FP_FB[i][0].index(False)
                print('No conjunto de eventos que ocorre entre', FP_s_Names[i], 'e [', FB_s_Names[i][index],
                      '] não há um evento controlável.'
                      '\nPortanto, a cadeia', i + 1, 'não é controlável segura pela prognose.\n')
                Is_Controllable_By_Prognosis = False
                Each_String = False
            else:
                print('Na cadeia', i + 1, 'não há ciclos incertos ou normais. Além disso, sempre há um',
                      'evento controlável entre um estado FP(', i + 1, ') e um estado FB(', i + 1, ').',
                      '\nPortanto, a cadeia', i + 1, 'é controlável segura pela prognose.\n')
            Each_String_Diag_Controllable.append(Each_String)
            i += 1

        if Is_Controllable_By_Prognosis == True:
            print('A linguagem é controlável segura pela prognose.')
        else:
            print('A linguagem não é controlável segura pela prognose.')

        return Each_String_Diag_Controllable

    # if it is not Language Diagnosable:
    else:
        print('\nA linguagem não é controlável segura pela prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg_Publish():

    # if it is Language Diagnosable:
    if IsDiag():

        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s()

        # getting the event sequence to the fault
        i = 0
        Fault_Diag_EventStrings_IDs = []
        while i < len(FU):
            fault_state = FU[i]
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
            i += 1


        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            i += 1

        print('\n\nPara cada cadeia, calcula-se a controlabilidade segura tanto pela diagnose quanto pela prognose:')

        by_diag = IsSafeControlByDiag_Publish()
        by_prog = IsSafeControlByProg_Publish()

        print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE E PROGNOSE\n')

        Is_Controllable = True
        string = 0
        while string < len(by_diag):
            if by_diag[string] and by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura tanto pela diagnose quanto pela prognose.')
            elif by_diag[string]:
                print('A cadeia', string+1, 'é controlável segura pela diagnose.')
            elif by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura pela prognose.')
            else:
                print('A cadeia', string+1, 'não é controlável segura pela diagnose ou pela prognose.')
                Is_Controllable = False
            string += 1

        if Is_Controllable:
            print('\nPortanto, a linguagem é controlável segura pela diagnose e pela prognose')
        else:
            print('\nPortanto, a linguagem não é controlável segura pela diagnose e pela prognose')

        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é controlável segura pela diagnose e prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg_SelfPublish():

    # if it is Language Diagnosable:
    if IsDiag():

        # get FU (so I know where diagnoser is going to fail)
        FU = FU_s.Get_FU_s()

        # getting the event sequence to the fault
        i = 0
        Fault_Diag_EventStrings_IDs = []
        while i < len(FU):
            fault_state = FU[i]
            fault_state_ID = DiagnoserFunctions.GetStateId(fault_state)
            Fault_Diag_EventStrings_IDs.append(DefineStrings.GetDiagnoserString(fault_state_ID))
            i += 1


        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            i += 1

        by_diag = IsSafeControlByDiag()
        by_prog = IsSafeControlByProg()

        print('\n\n* CONTROLABILIDADE SEGURA PELA DIAGNOSE E PROGNOSE\n')

        # getting these events names
        Fault_Aut_Strings_Names = []
        i = 0
        while i < len(Fault_Diag_EventStrings_IDs):
            state_name = []
            for each in Fault_Diag_EventStrings_IDs[i]:
                state_name.append(DiagnoserFunctions.GetEventName(each))
            state_name.append(AutomataFunctions.GetFaultEventName())
            Fault_Aut_Strings_Names.append(state_name)
            i += 1

        Is_Controllable = True
        string = 0
        while string < len(by_diag):
            if by_diag[string] and by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura tanto pela diagnose quanto pela prognose.')
            elif by_diag[string]:
                print('A cadeia', string+1, 'é controlável segura pela diagnose.')
            elif by_prog[string]:
                print('A cadeia', string+1, 'é controlável segura pela prognose.')
            else:
                print('A cadeia', string+1, 'não é controlável segura pela diagnose ou pela prognose.')
                Is_Controllable = False
            string += 1

        if Is_Controllable:
            print('\nPortanto, a linguagem é controlável segura pela diagnose e pela prognose')
        else:
            print('\nPortanto, a linguagem não é controlável segura pela diagnose e pela prognose')

        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        print('A linguagem não é controlável segura pela diagnose e prognose, pois não é diagnosticável em primeiro lugar.')
        return False


def IsSafeControlByDiagAndProg():

    # if it is Language Diagnosable:
    if IsDiag():

        by_diag = IsSafeControlByDiag()
        by_prog = IsSafeControlByProg()

        Is_Controllable = True
        string = 0
        while string < len(by_diag):
            if not (by_diag[string] or by_prog[string]):
                Is_Controllable = False
            string += 1

        return Is_Controllable

    # if it is not Language Diagnosable:
    else:
        return False
