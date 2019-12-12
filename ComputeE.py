import DiagnoserFunctions
import DiagnoserParser



def ComputeEgdeg(estado_inicial):
    estados = []
    aux = []
    estados.append(estado_inicial)

    for estado in estados:
        positions = DiagnoserFunctions.GetPositionSource(estado)
        for each in positions:
            #print(each)
            event_id = DiagnoserParser.Transition_Event_Table[int(each)]
            if (DiagnoserFunctions.EventIsControllable(event_id) == False):
                aux = DiagnoserParser.Transition_Target_Table[int(each)]
                if estados.__contains__(str(aux)) == False:
                    estados.append(str(aux))

    return (estados)

def iuashdusai(estado_inicial):
    events = []
    estado = []
    aux = []
    estados = []
    estados.append(estado_inicial)

    for estado in estados:
        positions = DiagnoserFunctions.GetPositionSource(estado)
        for each in positions:
            event_id = DiagnoserParser.Transition_Event_Table[int(each)]
            if (DiagnoserFunctions.EventIsControllable(event_id) == False):
                if(events.__contains__(str(event_id)) == False):
                    events.append(event_id)
                aux = DiagnoserParser.Transition_Target_Table[int(each)]
                if estados.__contains__(str(aux)) == False:
                    estados.append(str(aux))

    return(events)