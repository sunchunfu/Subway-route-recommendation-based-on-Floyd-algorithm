import pandas as pd
import json
from pprint import pprint



with open('../data/stdata1.json','r',encoding='utf-8') as f:
    stdata = json.load(f)

    sts = list(stdata.keys())
    for i in range(len(sts)):
        stn = sts[i]
        id = i
        stdata[stn]['id'] = id

    with open('../data/stdata2.json', 'w', encoding='utf-8') as fin:
        json.dump(stdata,fin,indent=4,ensure_ascii=False)