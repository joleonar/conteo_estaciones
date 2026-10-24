import re
import pandas as pd

def cuenta_estaciones(fname: str, nombre_columna: str = None) -> pd.DataFrame:
    try:
        with open(fname, 'r', encoding='utf-8', errors='ignore') as fhand:
            lines = fhand.readlines()
    except Exception as e:
        raise FileNotFoundError(f"No se pudo abrir el archivo {fname}: {e}")
        
    parsing = False
    estaciones = []
    
    # Extrae códigos de estaciones entre ' STAT ' y la línea en blanco
    for line in lines:
        line = line.rstrip()
        if re.match(r'^ STAT ', line):
            parsing = True
            continue
        elif line == '':
            parsing = False
       
        if parsing:
            # Arribos de fase P
            if re.search(r'\bP\s+', line) or 'P ' in line:
                sta = line.split()
                if sta:
                    estaciones.append(sta[0])
    
    # Conteo por estación
    cuenta_dict = {}
    for st in estaciones:
        cuenta_dict[st] = cuenta_dict.get(st, 0) + 1
    
    col_name = nombre_columna if nombre_columna else "conteo"
    
    df_est = (pd.DataFrame(list(cuenta_dict.items()), columns=['Estacion', col_name])
              .set_index('Estacion')
              .sort_index())
    
    return df_est