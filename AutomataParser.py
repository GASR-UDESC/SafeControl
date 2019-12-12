from xml.dom.minidom import parse
doc = parse('G_17.xml')
xml = doc.documentElement

data = xml.getElementsByTagName('data')

for info in data:
    states = info.getElementsByTagName('state')
    events = info.getElementsByTagName('event')
    transitions = info.getElementsByTagName('transition')

Aut_State_Id_Table = []
Aut_State_Name_Table = []
Aut_Event_Id_Table = []
Aut_Event_Name_Table = []
Aut_Transition_Id_Table = []
Aut_Transition_Event_Table = []
Aut_Transition_Target_Table = []
Aut_Transition_Source_Table = []
Aut_ObservableTable = []
Aut_ControllableTable = []

for state_id in states:
    if state_id.hasAttribute('id'):
        Id_State = state_id.getAttribute('id')
        Aut_State_Id_Table.append(Id_State)

for state_name in states:
    name_state = state_name.getElementsByTagName('name')
    state_name = name_state[0].childNodes[0].data
    Aut_State_Name_Table.append(state_name)

for event_id in events:
    if event_id.hasAttribute('id'):
        event_table_id = event_id.getAttribute('id')
        Aut_Event_Id_Table.append(event_table_id)

for event in events:
    try:
        properties = event.getElementsByTagName("properties")[0]
        if(properties.getElementsByTagName("observable")[0]):
            Aut_ObservableTable.append(str(1))
    except:
        Aut_ObservableTable.append(str(0))
        pass

for event in events:
    try:
        properties = event.getElementsByTagName("properties")[0]
        if(properties.getElementsByTagName("controllable")[0]):
            Aut_ControllableTable.append(str(1))
    except:
        Aut_ControllableTable.append(str(0))
        pass

for event_name in events:
    name_event = event_name.getElementsByTagName('name')
    event_table_name = name_event[0].childNodes[0].data
    Aut_Event_Name_Table.append(event_table_name)

for transition_id in transitions:
    if transition_id.hasAttribute('id'):
        transition_table_id = transition_id.getAttribute('id')
        Aut_Transition_Id_Table.append(transition_table_id)

for transition_event in transitions:
    if transition_event.hasAttribute('event'):
        transition_table_event = transition_event.getAttribute('event')
        Aut_Transition_Event_Table.append(transition_table_event)

for transition_target in transitions:
    if transition_target.hasAttribute('target'):
        transition_table_target = transition_target.getAttribute('target')
        Aut_Transition_Target_Table.append(transition_table_target)

for transition_source in transitions:
    if transition_source.hasAttribute('source'):
        transition_table_source = transition_source.getAttribute('source')
        Aut_Transition_Source_Table.append(transition_table_source)
