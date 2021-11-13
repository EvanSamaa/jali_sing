

VOWELS_JALI = set(["Ih_pointer", "Ee_pointer", "Eh_pointer", "Aa_pointer", "U_pointer", "Uh_pointer", "Oo_pointer", "Oh_pointer", "Schwa_pointer", "Eu_pointer", "Ah_pointer"])
CONSONANTS_JALI = set(["MBP_pointer", "JY_pointer", "Th_pointer", "ShChZh_pointer", "SZ_pointer", "GK_pointer", "LNTD_pointer", "R_pointer", "W_pointer", "FV_pointer"])
CONSONANTS_NOJAW_JALI = set(["Ya_pointer", "Ja_pointer", "Ra_pointer", "FVa_pointer", "LNTDa_pointer", "MBPa_pointer", "Wa_pointer", "Tha_pointer", "GKa_pointer"])
LIP_HEAVY_VISEMES_JALI = set(["Oh_pointer", "W_pointer", "U_pointer", "SZ_pointer", "JY_pointer"])
LABIAL_AND_DENTAL_JALI = set(["MBP_pointer", "SZ_pointer", "FV_pointer"])
NASAL_OBSTRUENTS_JALI = set(["LNTD_pointer", "GK_pointer", "FV_pointer", "MBP_pointer", ])
JALI_SLIDERS_SET = set.union(VOWELS_JALI, CONSONANTS_JALI, CONSONANTS_NOJAW_JALI)
CMU_VOCABULARY = ['AA', 'AE', 'AH', 'AO', 'AW', 'AY', 'B', 'CH', 'D', 'DH', 'EH', 'ER', 'EY', 'F', 'G',
                  'HH', 'IH', 'IY', 'JH', 'K', 'L', 'M', 'N', 'NG', 'OW', 'OY', 'P', 'R', 'S', 'SH', 'T', 'TH', 'UH',
                  'UW', 'V', 'W', 'Y', 'Z', 'ZH']
VOWELS_DIPTHONGS_SET = set(["AW", "AY", "EY", "OY"])
CONSONANTS_NO_JAW_SET = ["JY", "R", "FV", "LNTD", "MBP", "W", "Th", "GK"]
CMU2VISEME = {"AA":"Ah",
                    "AO":"Ah",
                    "AY":"Ah",
                    "AW":"Ah",

                    "AE":"Aa",
                    "EY":"Aa",

                    "UH":"Uh",

                    "UW":"U",

                    "IH": "Ih",
                    "IY": "Ih",

                    "EH": "Eh",
                    "HH": "Eh",
                    "UH": "Eh",
                    "AH": "Eh",
                    "ER": "Eh",

                    "OW":"Oh",
                    "OY":"Oh",

                    "R":"R",

                    "D":"LNTD",
                    "T": "LNTD",
                    "L":"LNTD",
                    "N":"LNTD",
                    "NG":"LNTD",

                    "F":"FV",
                    "V":"FV",

                    "B":"MBP",
                    "M":"MBP",
                    "P":"MBP",

                    "CH":"ShChZh",
                    "SH":"ShChZh",
                    "ZH":"ShChZh",

                    "S": "SZ",
                    "Z": "SZ",

                    "DH":"Th",
                    "TH":"Th",

                    "G":"GK",
                    "K":"GK",

                    "Y":"JY",
                    "JH":"JY",

                    "W":"W",
                    }