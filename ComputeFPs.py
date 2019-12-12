import DiagnoserFunctions
import PathManager

def Compute_FPs_Id(conjunto_nomes_id):
    estados_passados = []
    answer = []
    conjunto_nomes = []
    for each in conjunto_nomes_id:
        conjunto_nomes.append(each)

    for cada in conjunto_nomes:
        estados_passados = DiagnoserFunctions.GetBackwardsStatesInID(cada)
        if len(estados_passados) == 0:
            answer.append(cada)
        for everyone in estados_passados:
            if PathManager.ConditionCHolds(everyone):
                if(conjunto_nomes.__contains__(str(everyone)) == False):
                    conjunto_nomes.append(str(everyone))
            else:
                answer.append(cada)

    return(answer)
