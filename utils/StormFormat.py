"""
Prep function to get storms into groups with merges and unmerges.
"""

import pandas as pd
import re

def read_data(loc:str):
    data = pd.read_csv(loc)
    return data

def extract_storm_ids(row):
    # gather the sub missions from the first parts of each storm combination 
    found_sub_missions = re.findall(r'[A-Z][0-9]{2}', row, flags=re.IGNORECASE) 
    # gather the storm ids from each grounp of submissions
    storm_ids = re.split(r'[A-Z][0-9]{2}_', row, flags=re.IGNORECASE) 
    storm_ids = [x for x in storm_ids if x != '']

    for idx, mission_add in enumerate(storm_ids):
        temp = mission_add.split('+')
        temp = [x for x in temp if x != '']
        storm_ids[idx] = temp

    # bring the submission and storm ids together and into a single list
    # instead of list of lists
    storm_ids_final = []
    for sub_mission, storm_id in zip(found_sub_missions, storm_ids):
        for idx, storm in enumerate(storm_id):
            storm_ids_final.append(sub_mission + '_' + storm)

    return storm_ids_final

def drop_not_useful_columns(d,
    drop_cols:list=[
        'Mars Year',
        'Mission subphase',
        'Sol',
        'Sequence ID', 
        'storm_ids', 
        'Member ID',
        'variable'
        ]
    ):
    # get rid of columns that are not required
    return d.drop(drop_cols, axis=1, inplace=True)
    

# build a process to break down the sequence ID into the individual storms
def break_down_storm_history(data, column:str='Sequence ID') -> pd.DataFrame:
    seq_id_combo = data.copy()[[column]].dropna()
    seq_id_combo['combined_storm'] = data.copy()[column].apply(lambda x: '+' in str(x))
    seq_id_combo['storm_ids'] = seq_id_combo[column].apply(extract_storm_ids)

    # put into columns of dataframe
    storms_as_col = pd.DataFrame(seq_id_combo['storm_ids'].to_list())
    storms_as_col = storms_as_col.add_prefix('storm_id_list_')
    variable_cols = storms_as_col.columns.to_list()
    
    seq_id_combo = pd.concat([data, seq_id_combo, storms_as_col], axis=1)
    seq_id_combo = seq_id_combo.loc[:,~seq_id_combo.columns.duplicated()].copy()

    # pivot dataframe to flat dataframe with storm IDS
    seq_id_combo = seq_id_combo.melt(
    id_vars=seq_id_combo.drop(variable_cols, axis=1).columns.to_list(), 
    value_name='storm_id_breakout'
    )
    
    # get rid of the column entries with 'none' with the storm ids
    seq_id_combo.dropna(subset=['storm_id_breakout'], inplace=True)

    # get rid of extra columns no required for machine learning 
    #drop_not_useful_columns(seq_id_combo)
    
    
    return seq_id_combo