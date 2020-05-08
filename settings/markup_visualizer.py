CLASSES_HIGHLIGHTS_SI_HTML = {
    0: lambda x: "<mark style='background-color: white'>" + x + "</mark>",
    1: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>"
}

CLASSES_NAMES_SI = {
    0: "None",
    1: "Span",
}

CLASSES_NAMES_SI2IDX = {
    "O": 0,
    "I": 1,
}

CLASSES_HIGHLIGHTS_SI_BILUO_HTML = {
    0: lambda x: "<mark style='background-color: white'>" + x + "</mark>",
    1: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>",
    2: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>",
    3: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>",
    4: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>"
}

CLASSES_NAMES_SI_BILUO = {
    0: "None",
    1: "B-Span",
    2: "I-Span",
    3: "L-Span",
    4: "U-Span",
}

CLASSES_NAMES_SI_BILUO2IDX = {
    "O": 0,
    "-": 0,
    "B-SPAN": 1,
    "I-SPAN": 1,
    "L-SPAN": 1,
    "U-SPAN": 1,
    "S-B": 1,
    "S-I": 1
}

CLASSES_HIGHLIGHTS_TC_HTML = {
    0: lambda x: "<mark style='background-color: white'>" + x + "</mark>",
    1: lambda x: "<mark style='background-color: red'>" + x + "</mark>",
    2: lambda x: "<mark style='background-color: magenta'>" + x + "</mark>",
    3: lambda x: "<mark style='background-color: yellow'>" + x + "</mark>",
    4: lambda x: "<mark style='background-color: green'>" + x + "</mark>",
    5: lambda x: "<mark style='background-color: lime'>" + x + "</mark>",
    6: lambda x: "<mark style='background-color: blue'>" + x + "</mark>",
    7: lambda x: "<mark style='background-color: cyan'>" + x + "</mark>",
    8: lambda x: "<mark style='background-color: LightSalmon'>" + x + "</mark>",
    9: lambda x: "<mark style='background-color: DeepPink'>" + x + "</mark>",
    10: lambda x: "<mark style='background-color: PaleVioletRed'>" + x + "</mark>",
    11: lambda x: "<mark style='background-color: OrangeRed'>" + x + "</mark>",
    12: lambda x: "<mark style='background-color: RebeccaPurple'>" + x + "</mark>",
    13: lambda x: "<mark style='background-color: Moccasin'>" + x + "</mark>",
    14: lambda x: "<mark style='background-color: YellowGreen'>" + x + "</mark>",
    15: lambda x: "<mark style='background-color: DarkCyan'>" + x + "</mark>",
    16: lambda x: "<mark style='background-color: DarkGray'>" + x + "</mark>",
    17: lambda x: "<mark style='background-color: MidnightBlue'>" + x + "</mark>",
    18: lambda x: "<mark style='background-color: Chocolate'>" + x + "</mark>"
}

CLASSES_NAMES_TC = {
    0: "None",
    1: "Presenting Irrelevant Data",
    2: "Misrepresentation of Someone's Position",
    3: "Whataboutism",
    4: "Causal Oversimplification",
    5: "Obfuscation, Intentional vagueness, Confusion",
    6: "Appeal to authority",
    7: "Black-and-white Fallacy, Dictatorship",
    8: "Name calling or labeling",
    9: "Loaded Language",
    10: "Exaggeration or Minimisation",
    11: "Flag-waving",
    12: "Doubt",
    13: "Appeal to fear/prejudice",
    14: "Slogans",
    15: "Thought-terminating cliché",
    16: "Bandwagon",
    17: "Reductio_ad_hitlerum",
    18: "Repetition"
}

CLASSES_NAMES_TC2IDX = {
    "None": 0,
    "Presenting_Irrelevant_Data": 1,
    "Misrepresentation_of_Someone's_Position": 2,
    "Whataboutism,Straw_Men,Red_Herring": 3,
    "Causal_Oversimplification": 4,
    "Obfuscation, Intentional vagueness, Confusion": 5,
    "Appeal_to_Authority": 6,
    "Black-and-white_Fallacy": 7,
    "Name_Calling,Labeling": 8,
    "Loaded_Language": 9,
    "Exaggeration,Minimisation": 10,
    "Flag-waving": 11,
    "Doubt": 12,
    "Appeal_to_fear-prejudice": 13,
    "Slogans": 14,
    "Thought-terminating_cliché": 15,
    "Bandwagon": 16,
    "Reductio_ad_hitlerum": 17,
    "Repetition": 18,
}