from unidecode import unidecode
import pandas as pd
import numpy as np
from ast import literal_eval

def trim(x):
    x = x.split()
    x = ' '.join(x)
    return x   


def clean_punctuation(df):
    for i in df.columns:
        df[i] = df[i].astype(str) 
    df = df.map(lambda x: x.lower())
    for i in df.columns:
        df[i] = df[i].str.replace('[^\w\s\.\-\(\)\,\:\/\\\\]','')
    df = df.map(lambda x: trim(x))
    df = df.map(lambda x: unidecode(x))
    for i in df.columns:
        df[i] = df[i].replace({'nan': None, 'none': None, 'nat': None})
    return df

def select_fields(fields, field_properties):
    for i in field_properties:
        if type(i)==str:
            fields.concat({'field': i, 'type': 'String'})
        elif len(i)==2:
            fields.concat({'field': i[0], 'type': i[1]})
        elif len(i)==3:
            if i[2] == 'has missing':
                fields.concat({'field': i[0], 'type': i[1], 'has missing': True})
            elif i[2] == 'crf':
                fields.concat({'field': i[0], 'type': i[1], 'crf': True})
            else:
                raise Exception(i[2] + " is not a valid field property")
                
    
def latlong_datatype(x):
    if x is None:
        return None
    else:
        try:
            x = literal_eval(x)
            k,v = x
            k = float(k)
            v = float(v)
            return k, v
        except:
            raise Exception("Make sure that LatLong columns are tuples arranged like ('lat', 'lon')")
            
            
def specify_type(df, field_properties):
    for i in field_properties:
        if i[1] == 'LatLong':
            df[i[0]] = df[i[0]].apply(lambda x: latlong_datatype(x))
        elif i[1] == 'Price':
            try:
                df[i[0]] = df[i[0]].str.replace(",","")
                df[i[0]] = df[i[0]].replace({None: np.nan})
                df[i[0]] = df[i[0]].astype(float)
                df[i[0]] = df[i[0]].replace({np.nan: None})
            except:
                raise Exception('Make sure that Price columns can be converted to float.')
 
