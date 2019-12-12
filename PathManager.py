import DiagnoserFunctions
import DefineStrings

def AnalyseStatePath(state): #str(id)
    answer = []
    NextStateIds = DiagnoserFunctions.GetNextStatesInID(state)
    status = False

    while status != True:
        for each in NextStateIds:
            NextStateNames = str(DiagnoserFunctions.GetNextStatesInNames(str(each)))

            if DiagnoserFunctions.IsCertain(NextStateNames) == True:
                status = True
                answer.append(1)
            else:
                if DiagnoserFunctions.IsOnlySelfloop(each) == 1:
                    status = True
                    answer.append(0)
                else:
                    state_id = DiagnoserFunctions.GetNextStatesInID(each)
                    for cada in state_id:
                        if NextStateIds.__contains__(cada) == False:
                            NextStateIds.append(cada)

            if answer.__contains__(0) == True:
                resposta_final = 0
            else:
                resposta_final = 1

    return(resposta_final)


def ConditionCHolds(state_ID):  # returns True if C condition holds
    Reachable = []
    for each in state_ID:
        Reachable.append(DefineStrings.GetReachable(each))

    # test if there is any Normal or Uncertain Cycle
    test_normal = DefineStrings.IsNormalCycle(Reachable)
    test_uncertain = DefineStrings.IsUncertainCycle(Reachable)

    # calculating the answers
    i = 0
    C_Condition = True
    while i < len(test_normal):
        if True in test_normal[i] or True in test_uncertain[i]:
            C_Condition = False
        i += 1

    return C_Condition
