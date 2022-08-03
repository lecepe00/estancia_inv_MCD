import pandas as pd
import numpy as np
import re


def limpieza_texto(text,tesis):
    
    tesis_borrar = ''.join(tesis)
    text_aux = text.strip()
    text_aux = text_aux.replace('\n\n','###')
    text_aux = text_aux.replace('\n',' ')
    text_aux = text_aux.replace('Ley de Amparo','ley_de_amparo')
    text_aux = text_aux.replace('Competencia Económica','competencia_económica')
    text_aux = text_aux.replace(r"1o.","01")
    text_aux = text_aux.replace('Pág. 1 de 1 ','')
    text_aux = text_aux.replace('Pág. 1 de 2 ','')
    text_aux = text_aux.replace('Pág. 2 de 2 ','')
    text_aux = text_aux.replace('http://sjf2.scjn.gob.mx/detalle/tesis/','')
    text_aux = text_aux.replace(tesis_borrar,'')
    text_aux = text_aux.replace('  Fecha de impresión','')
    text_aux = text_aux.replace('Fecha de impresión','')
    text_aux = text_aux.replace(' 09/07/2021','')
    text_aux = text_aux.replace(' 10/07/2021','')
    text_aux = text_aux.replace('  \x0c','')
    text_aux = text_aux.replace('######\x0c','')
    text_aux = text_aux.replace('Semanario Judicial de la Federación ','')
    
    return text_aux