import sys
sys.path.append(['../utils/'])

from utils.StormFormat import extract_storm_ids

def test_extracting_storm_ids_uppercase():
    example = 'B07_048+050+055+057+B08_001+007+008+009'
    expected_result = ['B07_048',
                    'B07_050',
                    'B07_055',
                    'B07_057',
                    'B08_001',
                    'B08_007',
                    'B08_008',
                    'B08_009']
    assert extract_storm_ids(example) == expected_result

def test_extracting_storm_ids_lowercase():
    example = 'e06_005+006+007+014+015+016+017+e07_001+002'
    expected_result = ['e06_005',
                    'e06_006',
                    'e06_007',
                    'e06_014',
                    'e06_015',
                    'e06_016',
                    'e06_017',
                    'e07_001',
                    'e07_002']
    assert extract_storm_ids(example) == expected_result

