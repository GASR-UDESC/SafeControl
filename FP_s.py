import FU_s
import ComputeFPs
import ComputeE
import PathManager
import DiagnoserFunctions
UP = []

def GetFP_s(FU_s_Id):
    FPs = []
    FP = []
    UPs = []
    UP = []

    if PathManager.ConditionCHolds(FU_s_Id):
        FPs = ComputeFPs.Compute_FPs_Id(FU_s_Id)
        for each in FPs:
        #print(each)
            X = ComputeE.iuashdusai(each)
            fi = ['9', '10']
            for cada in fi:
                if X.__contains__(str(cada)) == True:
                    if(UPs.__contains__(str(each)) == False):
                        UPs.append(each)

            if len(UPs) > 0:
                for each in UPs:
                    if FPs.__contains__(str(each)):
                        FPs.remove(str(each))

    for each in FPs:
        x = DiagnoserFunctions.GetNextStatesInNames(each)
        if FP.__contains__(x) == False:
            FP.append(x)

    for each in UPs:
        x = DiagnoserFunctions.GetNextStatesInNames(each)
        if UP.__contains__(x) == False:
            UP.append(x)

    return(FP)

def GetUP(FU_Pos):
    GetFP_s(FU_Pos)
    return(UP)