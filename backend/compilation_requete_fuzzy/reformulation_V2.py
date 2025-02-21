from find_nearby_pitches import find_frequency_bounds, find_nearby_pitches
from find_duration_range import find_duration_range_decimal, find_duration_range_multiplicative_factor_sym
from extract_notes_from_query import extract_notes_from_query, extract_fuzzy_parameters
from utils import calculate_pitch_interval, calculate_intervals
from degree_computation import convert_note_to_sharp

import re

def make_duration_condition(duration_factor, duration, idx, fixed):
    if duration == None:
        return ''

    if duration_factor != 1 and not fixed:
        min_duration, max_duration = find_duration_range_multiplicative_factor_sym(duration, duration_factor)
        res = f"{min_duration} <= e{idx}.duration AND e{idx}.duration <= {max_duration}"
    else:
        duration = find_duration_range_multiplicative_factor_sym(duration, 1.0)[0]
        res = f"e{idx}.duration = {duration}"
    return res

def make_sequencing_condition(duration_gap, idx):
    sequencing_condition = f"e{idx}.end >= e{idx+1}.start - {duration_gap}"
    return sequencing_condition

def make_interval_condition(interval: float, transposition: bool, duration_gap: float, pitch_distance: float, is_fixed: bool, idx: int) -> str:
    '''
    Create the interval condition (for the WHERE clause with transposition or contour).

    - interval       : the interval from the given melody ;
    - transposition  : if true, create condition for query with transposition. Otherwise, create for query with contour ;
    - duration_gap   : the duration gap fuzzy parameter ;
    - pitch_distance : the pitch distance fuzzy parameter ;
    - is_fixed       : a boolean indicating if the note is fixed or not ;
    - idx            : the current index.
    '''

    if transposition:
        if duration_gap > 0:
            if pitch_distance > 0 and not is_fixed:
                interval_condition = f'{interval - pitch_distance} <= totalInterval_{idx} AND totalInterval_{idx} <= {interval + pitch_distance}'
            else:
                interval_condition = f'totalInterval_{idx} = {interval}'

        else:
            # Construct interval conditions for direct connections
            if pitch_distance > 0 and not is_fixed:
                interval_condition = f'{interval - pitch_distance} <= r{idx}.interval AND r{idx}.interval <= {interval + pitch_distance}'
            else:
                interval_condition = f'r{idx}.interval = {interval}'

    else:
        if duration_gap > 0:
            interval_keyword = f'totalInterval_{idx}'
        else:
            interval_keyword = f'r{idx}.interval'

        if interval == 0:
            interval_condition = f'{interval_keyword} = 0'
        elif interval > 0:
            interval_condition = f'{interval_keyword} > 0'
        else:
            interval_condition = f'{interval_keyword} < 0'
    
    return interval_condition

def make_note_condition(note: str, idx: int) -> str:
    '''
    Creates the condition to match the note `note` (only class).
    If there is an accidental (sharp or flat), then it adds two conditions (because the note can be encoded in two ways)

    - note : the class of the note to match, e.g 'c', 'cs', 'c#', 'cf', 'cb'. Its length should be 1 or 2 ;
    - idx  : the current index.
    '''

    note = convert_note_to_sharp(note)

    #---Rest
    if note[0] == 'r':
        return f'f{idx}.type = "rest"'

    #---No accidental
    if len(note) == 1:
        return f'f{idx}.class = "{note[0]}"'

    #---Accidental
    if note[1] in ('#', 's'): # sharp
        note_condition = f'((f{idx}.class = "{note[0]}"'
        note_condition += f' AND (f{idx}.accid = "s" OR f{idx}.accid_ges = "s"))' # f.accid : accidental on the note. f.accid_ges : accidental on the clef.

        notes = 'abcdefg'
        note_flat = notes[(notes.index(note[0]) + 1) % len(notes)]

        note_condition += f' OR (f{idx}.class = "{note_flat}"'
        note_condition += f' AND (f{idx}.accid = "f" OR f{idx}.accid_ges = "f")))'

    # elif note[1] in ('b', 'f'): # flat
    #     note_condition = f'(f{idx}.class = "{note[0]}"'
    #     note_condition += f' AND (f{idx}.accid = "f" OR f{idx}.accid_ges = "f")'

    else:
        raise ValueError(f'reformulation: make_note_condition: `note` not correctly formatted (found "{note}").')

    return note_condition


def create_match_clause(notes, duration_gap, intervals=False):
    '''
    Create the MATCH clause for the compilated query.

    - notes        : the notes (for the format, check the documentation of `extract_notes_from_query`) ;
    - duration_gap : the duration gap ;
    - intervals    : indicate if transposition is allowed or if match contour (to use intervals, i.e to name the links between Events).
    '''

    #---Init
    nb_events = len(notes)

    #---Create the Event path
    if duration_gap > 0:
        # To give a higher bound to the number of intermediate notes, we suppose the shortest possible note has a duration of 0.125
        max_intermediate_nodes = max(int(duration_gap / 0.125), 1)

        if intervals:
            event_path = ',\n '.join([
                f'p{idx} = (e{idx}:Event)-[:NEXT*1..{max_intermediate_nodes + 1}]->(e{idx + 1}:Event)'
                for idx in range(nb_events - 1)
            ]) + ','
        else:
            event_path = f'-[:NEXT*1..{max_intermediate_nodes + 1}]->'.join([f'(e{idx}:Event)' for idx in range(nb_events)]) + ','

    else:
        if intervals:
            event_path = ''.join([f'(e{idx}:Event)-[r{idx}:NEXT]->' for idx in range(nb_events - 1)]) + f'(e{nb_events - 1}:Event)'+ ','
        else:
            event_path = f'-[]->'.join([f'(e{idx}:Event)' for idx in range(nb_events)]) + ','  

    #---Create the path from Events to theirs Facts
    fact_nb = 0
    simplified_connections = ''
    for event_nb, event in enumerate(notes):
        for note in event[:-1]:
            simplified_connections += f'\n (e{event_nb})-[]->(f{fact_nb}:Fact),'
            fact_nb += 1

    simplified_connections = simplified_connections[:-1] # Removing trailing comma.

    #---Create match clause
    match_clause = 'MATCH\n ' + event_path + simplified_connections

    return match_clause

def create_with_clause_interval(nb_events, duration_gap):
    '''
    Create the WITH clause for the compilated query that need intervals (so with `allow_transposition` or `contour`).

    - nb_events    : the number of Events ;
    - duration_gap : the duration gap.
    '''

    with_clause = ""
    if duration_gap > 0:
        # Construct interval conditions for paths with intermediate nodes
        interval_conditions = []

        for idx in range(nb_events - 1): # nb of intervals
            interval_condition = f"reduce(totalInterval = 0, rel IN relationships(p{idx}) | totalInterval + rel.interval) AS totalInterval_{idx}"
            interval_conditions.append(interval_condition)

        # Adding the interval clauses if duration_gap is specified
        variables = ' ' + ', '.join([f"e{idx}" for idx in range(nb_events)]) + ',\n ' + ', '.join([f"f{idx}" for idx in range(nb_events)])
        with_clause = 'WITH\n' + variables + ',\n ' + ',\n '.join(interval_conditions) + ' '

    return with_clause + '\n'

def create_where_clause_simple(notes, fixed_notes, pitch_distance, duration_factor, duration_gap):
    '''
    Create the WHERE clause to match `notes`.
    Does not allow transposition.

    - notes           : the array of notes triples (pitch, octave, duration) ;
    - fixed_notes     : the array indicating if notes are fixed ;
    - pitch_distance  : the pitch distance ;
    - duration_factor : the duration factor ;
    - duration_gap    : the duration gap.
    '''

    where_clauses = []
    sequencing_conditions = []
    fact_nb = 0 # the current fact number

    for event_nb, event in enumerate(notes):
        duration = event[-1]

        #---Making the duration condition
        duration_condition = make_duration_condition(duration_factor, duration, event_nb, fixed_notes[event_nb])

        if duration_condition != '':
            where_clauses.append(' ' + duration_condition)

        #---Adding sequencing conditions
        if event_nb < len(notes) - 1 and duration_gap > 0:
            sequencing_condition = make_sequencing_condition(duration_gap, event_nb)
            sequencing_conditions.append(sequencing_condition)

        #---Making the class + octave conditions for each note in the event (multiple if there is a chord)
        for (note, octave) in event[:-1]:
            if note == None:
                if octave == None:
                    note_condition = ''
                else:
                    note_condition = f'f{fact_nb}.octave = {octave}'

            else:
                if fixed_notes[event_nb] or pitch_distance == 0 or note[0] == 'r':
                    note_condition = make_note_condition(note, fact_nb)

                    if octave != None and note[0] != 'r':
                        note_condition += f' AND f{fact_nb}.octave = {octave}'

                else:
                    o = 4 if octave is None else octave # If octave is None, use 4 to get near notes classes
                    near_notes = find_nearby_pitches(note, o, pitch_distance)

                    # note_condition = '('
                    # for n, o_ in near_notes:
                    #     base_condition = make_note_condition(n, fact_nb)

                    #     if octave == None:
                    #         note_condition += f'\n  ({base_condition}) OR '
                    #     else:
                    #         note_condition += f'\n  ({base_condition} AND f{fact_nb}.octave = {o_}) OR '

                    # note_condition = note_condition[:-len(' OR ')] + '\n )' # Remove trailing ' AND '

                    low_freq_bound, high_freq_bound = find_frequency_bounds(note, o, pitch_distance)
                    note_condition = f"{low_freq_bound} <= f{fact_nb}.frequency AND f{fact_nb}.frequency <= {high_freq_bound}"


            if note_condition != '':
                where_clauses.append(' ' + note_condition)

            fact_nb += 1
    
    #---Assemble frequency, duration and sequencing conditions
    where_clause = 'WHERE\n' + ' AND\n'.join(where_clauses)
    if sequencing_conditions:
        sequencing_conditions = ' AND '.join(sequencing_conditions)
        where_clause = where_clause + ' AND \n ' + sequencing_conditions

    return where_clause

def create_where_clause_intervals(notes, allow_transposition, fixed_notes, pitch_distance, duration_factor, duration_gap):
    '''
    Create the WHERE clause to match `notes`.
    Allows transposition (by using intervals).

    Example: for the notes c5 b4 b4 g4 b4 a4, the intervals (in tones) are -0.5, 0, -2, 2, -1.

    - notes               : the array of notes triples (pitch, octave, duration) ;
    - allow_transposition : indicate if make query for transposition (True) or for contour (False) ;
    - fixed_notes         : the array indicating if notes are fixed ;
    - pitch_distance      : the pitch distance ;
    - duration_factor     : the duration factor ;
    - duration_gap        : the duration gap.
    '''

    intervals = calculate_intervals(notes)
    where_clauses = []

    for idx, event in enumerate(notes):
        duration = event[-1]
        duration_condition = make_duration_condition(duration_factor, duration, idx, fixed_notes[idx])

        if idx == len(notes) - 1 or intervals[idx] == None: # only duration condition for the last step or if no interval given
            if duration_condition != '':
                where_clauses.append(' ' + duration_condition)

        else: # duration condition + interval condition
            interval_condition = make_interval_condition(intervals[idx], allow_transposition, duration_gap, pitch_distance, fixed_notes[idx], idx)

            if duration_condition != '':
                where_clauses.append(' ' + duration_condition + ' AND ' + interval_condition)
            elif interval_condition != '':
                where_clauses.append(' ' + interval_condition)

    where_clause = 'WHERE\n' + ' AND\n'.join(where_clauses)

    # Adding the sequencing constraints to the WHERE clause
    if duration_gap > 0:
        sequencing_conditions = []
        for idx in range(len(notes) - 1):
            sequencing_condition = make_sequencing_condition(duration_gap, idx)
            if sequencing_condition:
                sequencing_conditions.append(sequencing_condition)
        sequencing_conditions = ' AND '.join(sequencing_conditions)
        where_clause = where_clause + ' AND \n ' + sequencing_conditions

    return where_clause

def create_collection_clause(collections, nb_events, nb_facts, duration_gap=0.0, intervals=False):
    '''
    Create the clause that will filter the given collections.

    - collections  : the array of collection strings ;
    - nb_events    : the number of Events ;
    - nb_facts     : the number of Facts ;
    - duration_gap : the duration gap fuzzy parameter (used to know if adding `r{idx} as r{idx}`) ;
    - intervals    : indicate if the clause will allow transpositions or match contour (and so use intervals). In this case, adding `r{idx} as r{idx}`.
    '''

    if collections == None or len(collections) == 0:
        col_clause = ''

    else:
        col_clause = '\nWITH'

        as_col_clause = ''
        for k in range(nb_events):
            as_col_clause += f'e{k} as e{k}, '

            if intervals and k < nb_events - 1:
                if duration_gap > 0:
                    as_col_clause += f'totalInterval_{k} as totalInterval_{k}, '
                else:
                    as_col_clause += f'r{k} as r{k}, '

        for k in range(nb_facts):
            as_col_clause += f'f{k} as f{k}, '

        as_col_clause = as_col_clause[:-2] # Remove trailing ', '

        col_clause += '\n ' + as_col_clause
        col_clause += '\nCALL {\n WITH e0\n MATCH (e0)<-[:timeSeries|VOICE|NEXT*]-(s:Score)\n RETURN s\n LIMIT 1\n}'
        col_clause += '\nWITH\n s as s, ' + as_col_clause

        col_clause += '\nWHERE'
        for col in collections:
            col_clause += f'\n s.collection CONTAINS "{col}" OR'

        col_clause = col_clause[:-3] # Remove trailing ' OR'.

    return col_clause

def create_return_clause(notes, duration_gap=0., intervals=False):
    '''
    Create the return clause.

    - notes        : the notes in the search melody ;
    - duration_gap : the duration gap. Used only when `intervals` is True ;
    - intervals    : indicate if the return clause is for a query that allows transposition, or contour match, or not. If so, it will also add `interval_{idx}` to the clause.
    '''

    fact_nb = 0 # will correspond to the index of the first fact corresponding to the current event
    return_clauses = []
    for event_nb, event in enumerate(notes):
        # Prepare return clauses with specified names
        return_clauses.extend([ #TODO: for a chord, only one note will be returned (the first one)
            f"\n f{fact_nb}.class AS pitch_{fact_nb}",
            f"f{fact_nb}.octave AS octave_{fact_nb}",
            f"e{event_nb}.duration AS duration_{event_nb}",
            f"e{event_nb}.start AS start_{event_nb}",
            f"e{event_nb}.end AS end_{event_nb}",
            f"e{event_nb}.id AS id_{event_nb}"
        ])

        if intervals and event_nb < len(notes) - 1:
            if duration_gap > 0:
                return_clauses.append(f"totalInterval_{event_nb} AS interval_{event_nb}")
            else:
                return_clauses.append(f"r{event_nb}.interval AS interval_{event_nb}")
        
        fact_nb += len(event) - 1 # -1 because event[-1] is duration and not a note

    return_clause = 'RETURN' + ', '.join(return_clauses) + f', \n e0.source AS source, e0.start AS start, e{len(notes) - 1}.end AS end'

    return return_clause


def reformulate_fuzzy_query(query):
    '''
    Converts a fuzzy query to a cypher one.

    - query : the fuzzy query.
    '''

    #------Init
    #---Extract the parameters from the augmented query
    pitch_distance, duration_factor, duration_gap, alpha, allow_transposition, contour_match, fixed_notes, collections = extract_fuzzy_parameters(query)

    #---Extract notes using the new function
    notes = extract_notes_from_query(query)

    nb_events = len(notes)
    nb_facts = sum(len(event) - 1 for event in notes)
    
    #------Construct the MATCH clause
    match_clause = create_match_clause(notes, duration_gap, allow_transposition or contour_match)

    #------Construct WITH clause
    if allow_transposition or contour_match:
        with_clause = create_with_clause_interval(nb_events, duration_gap)
    else:
        with_clause = ''

    #------Construct the WHERE clause
    if allow_transposition or contour_match:
        where_clause = create_where_clause_intervals(notes, allow_transposition, fixed_notes, pitch_distance, duration_factor, duration_gap)
    else:
        where_clause = create_where_clause_simple(notes, fixed_notes, pitch_distance, duration_factor, duration_gap)

    #------Construct the collection filter
    col_clause = create_collection_clause(collections, nb_events, nb_facts, duration_gap, allow_transposition or contour_match)

    #------Construct the return clause
    return_clause = create_return_clause(notes, duration_gap, allow_transposition or contour_match)
    
    #------Construct the final query
    new_query = match_clause + '\n' + with_clause + where_clause + col_clause + '\n' + return_clause
    return new_query.strip('\n')


if __name__ == '__main__':
    with open('query.cypher', 'r') as file:
        augmented_query = file.read()
    print(reformulate_fuzzy_query(augmented_query))
