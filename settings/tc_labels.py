TC2IDX = {
    'Appeal_to_Authority': 1,
    'Appeal_to_fear-prejudice': 2,
    'Bandwagon,Reductio_ad_hitlerum': 3,
    'Black-and-White_Fallacy': 4,
    'Causal_Oversimplification': 5,
    'Doubt': 6,
    'Exaggeration,Minimisation': 7,
    'Flag-Waving': 8,
    'Loaded_Language': 9,
    'Name_Calling,Labeling': 10,
    'Whataboutism,Straw_Men,Red_Herring': 11,
    'Thought-terminating_Cliches': 12,
    'Repetition': 13,
    'Slogans': 14
}

TC_BANNED = ['Obfuscation,Intentional_Vagueness,Confusion']

IDX2TCLABEL = {
    0: 'O',
    1: 'AUTH',
    2: 'FEAR',
    3: 'BANDAWAGON',
    4: 'BAWF',
    5: 'CO',
    6: 'DOUBT',
    7: 'EM',
    8: 'FLAG',
    9: 'LOADED',
    10: 'LABEL',
    11: 'RED',
    12: 'REDUCTIO',
    13: 'REPET',
    14: 'SLOGAN',
}

LABELS2CLASS = {
    'AUTH': 'Appeal_to_Authority',
    'FEAR': 'Appeal_to_fear-prejudice',
    'BANDAWAGON': 'Bandwagon,Reductio_ad_hitlerum',
    'BAWF': 'Black-and-White_Fallacy',
    'CO': 'Causal_Oversimplification',
    'DOUBT': 'Doubt',
    'EM': 'Exaggeration,Minimisation',
    'FLAG': 'Flag-Waving',
    'LOADED': 'Loaded_Language',
    'LABEL': 'Name_Calling,Labeling',
    'RED': 'Whataboutism,Straw_Men,Red_Herring',
    'REDUCTIO': 'Thought-terminating_Cliches',
    'REPET': 'Repetition',
    'SLOGAN': 'Slogans',
}