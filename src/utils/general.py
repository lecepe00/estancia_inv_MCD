import pandas as pd
import numpy as np
import re


def funcion_auxiliar_ponentes(x0,x1,x2,x3):
    if len(x0)!= 0 :
        result = x0
    elif len(x1)!= 0:
        result = x1
    elif len(x2)!= 0:
        result =["No se menciona el nombre del ponente sólo del relator"]
    elif x3 == 1:
        result =["Revisar texto tesis"]    
    return result


def funcion_auxiliar_secretarios(x0,x1,x10):
    if len(x0)!= 0 :
        result = x0
    elif len(x1)!= 0:
        result = ['NA']
    elif x10 == 1:
        result =['NA']    
    return result


def busca_tipo_tesis(text):
    
    #Eliminar tabulaciones adicionales
    text_aux = text.strip()

    pos_tipo = text_aux.find('Tipo:')
    if text_aux[pos_tipo:].find('\n\n') < text_aux[pos_tipo:].find('\n') :
        pos_final_tipo = text_aux[pos_tipo:].find('\n\n')
    else:
        pos_final_tipo = text_aux[pos_tipo:].find('\n')-2
    len_tipo = len('Tipo:')
    tipo = text_aux[pos_tipo+len_tipo:pos_tipo+pos_final_tipo+2].replace('\n',' ').strip()
    
    return tipo


def extraccion_encabezado(text):
    
    #Eliminar tabulaciones adicionales
    text_aux = text.strip()
    text_aux = text_aux.replace(' Fuente:','\n\nFuente:')
    
    #Posicion en el texto de las variables
    pos_registro_digital = text_aux.find('Registro digital:')
    pos_final_registro_digital = text_aux[pos_registro_digital:].find('\n')
    
    pos_instancia = text_aux.find('Instancia:')
    pos_final_instancia_aux1 = text_aux[pos_instancia:].find('\n\n')

    lista  = []

    lista.append(text_aux[pos_instancia:].find('Primera Época'))
    lista.append(text_aux[pos_instancia:].find('Segunda Época'))
    lista.append(text_aux[pos_instancia:].find('Tercera Época'))
    lista.append(text_aux[pos_instancia:].find('Cuarta Época'))
    lista.append(text_aux[pos_instancia:].find('Quinta Época'))
    lista.append(text_aux[pos_instancia:].find('Sexta Época'))
    lista.append(text_aux[pos_instancia:].find('Séptima Época'))
    lista.append(text_aux[pos_instancia:].find('Octava Época'))
    lista.append(text_aux[pos_instancia:].find('Novena Época'))
    lista.append(text_aux[pos_instancia:].find('Décima Época'))
    lista.append(text_aux[pos_instancia:].find('Undécima Época'))

    pos_final_instancia_aux2 = min([x for x in lista if x > -1])
    
    if pos_final_instancia_aux1 < pos_final_instancia_aux2:
        pos_final_instancia = pos_final_instancia_aux1
    else:
        pos_final_instancia = pos_final_instancia_aux2

    pos_epoca_aux1 = text_aux.find('\n\n')

    lista  = []

    lista.append(text_aux.find('Primera Época'))
    lista.append(text_aux.find('Segunda Época'))
    lista.append(text_aux.find('Tercera Época'))
    lista.append(text_aux.find('Cuarta Época'))
    lista.append(text_aux.find('Quinta Época'))
    lista.append(text_aux.find('Sexta Época'))
    lista.append(text_aux.find('Séptima Época'))
    lista.append(text_aux.find('Octava Época'))
    lista.append(text_aux.find('Novena Época'))
    lista.append(text_aux.find('Décima Época'))
    lista.append(text_aux.find('Undécima Época'))

    pos_epoca_aux2 = min([x for x in lista if x > -1])

    if pos_epoca_aux1 < pos_epoca_aux2:
        pos_epoca = pos_epoca_aux1
    else:
        pos_epoca = pos_epoca_aux2

    if pos_epoca_aux1 < pos_epoca_aux2:
        pos_final_epoca = text_aux[pos_epoca+2:].find('\n\n')
    else:
        pos_final_epoca = text_aux[pos_epoca+2:].find('\n')
        
    pos_materia = text_aux.find('Materia(s):')
    pos_final_materia = text_aux[pos_materia:].find('\n\n')

    pos_tesis = text_aux.find('Tesis:')
    pos_final_tesis = text_aux[pos_tesis:].find('\n\n')

    #Tamaño de las variables
    len_registro_digital = len('Registro digital:')
    len_instancia = len('Instancia:')
    if pos_epoca_aux1 < pos_epoca_aux2:
        len_epoca = len('\n\n')
    else:
        len_epoca = 0
    len_materia = len('Materia(s):')
    len_tesis = len('Tesis:')
    
    tesis = text_aux[pos_tesis+len_tesis:pos_tesis+pos_final_tesis+2].replace('\n',' ').strip()
    instancia = text_aux[pos_instancia+len_instancia:pos_instancia+pos_final_instancia].replace('\n',' ').strip()
    epoca = text_aux[pos_epoca+len_epoca:pos_epoca+pos_final_epoca+2].replace('\n',' ').strip()
    materia = text_aux[pos_materia+len_materia:pos_materia+pos_final_materia+2].replace('\n',' ').strip()
       
    return [tesis,instancia,epoca,materia]


def busqueda_ponentes(text_aux):

    x0_ponente = re.findall("(?:Ponente: Secretario Lic\. |Ponente: |Ponente |Ponente. |Ponentes: |Ponente:\.|Ponente:)([\s\S]*?)(?:.###|. Secretar|.Secretar|,|.\nSecretar|\. secretari|\. Relacionada|\. Disidente|\. Improcedencia|\. Semanario|\. Encargad|\. Competencia|\. Incidente|\. Queja|\. Reclamaci|\. Recurso|\. Juicio|\. Jurisprudencia| Magistrado|\. Tomo|\. Vol\wmen|;|\. Nota|\. NOTA|\. En| en funciones| en sustitución|\.; en su| y el engrose|Pág\.|Vol|\.Tom|\. V\wase|\. V\wanse|\. Revisión|\. Amparo| Amparo directo|\. Ausente|\. Séptima|\. Sexta|\.\"\.| \(en su ausencia|\. Texto|\. Cinco|\. Impedido|\. en su ausencia)",text_aux) 
    x1_ponente = re.findall("publicación ([\s\S]*?) del ponente",text_aux )
    x2_ponente = re.findall("Relator: ([\s\S]*?)\.",text_aux ) #re.findall(r"Relator",text_aux)
    x3_ponente = 1
    ponentes = funcion_auxiliar_ponentes(x0_ponente,x1_ponente,x2_ponente,x3_ponente)
        
    if len(re.findall('La publicación no menciona el nombre del ponente',text_aux)) != 0: 
        NA_ponentes = [('NA') for i in range(len(re.findall('La publicación no menciona el nombre del ponente',text_aux)))]
        ponentes.extend(NA_ponentes)
    if len(x2_ponente) != 0: 
        ponentes.extend(x2_ponente)
    
    return ponentes


def busqueda_fecha(text_aux,ponentes):
    
    #Búsqueda de párrafo donde se mencione reiteración con ponente con fecha   
    ponente_fecha_aux = re.findall(r'(?:Amparo|Revisión|Contradicción|Queja|Facultad|Incidente|Reclamación|Inconformidad|Competencia|Recurso de|Impedimento|Acción de inconstitucionalidad|Varios |Controversia constitucional|Reconocimiento de inocencia|Improcedencia|Aclaración de sentencia en la contra|Repetición|Inejecuci|Expediente vario|Solicitud|Acumulaci\wn|Trámite|Consulta|Recurso en|Juicio|Reposici\wn|Incompetencia|Incidente|Conflicto competencial|Vol\wmen \d{1,2}, p\wgina|Indulto necesario|C\. C\. \d{2,3}/\d{2})([\s\S]*?)(Ponente: |Ponente |Ponente\.|Ponente:\.|Ponente:|La publicación no menciona el nombre del ponente)([\s\S]*?)(?:Secretari\w: |Secretari\ws:|Secretari\w. )?([\s\S]*?)(?:\.?)', text_aux)
    ponente_fecha_texto = ''.join([''.join(j) for j in ponente_fecha_aux])
        
    fecha = re.findall('(\d{1,2}( de|de)*? [a-zA-Z]{4,10}( de| del)*? \d{4})',ponente_fecha_texto)
    fecha_aux = pd.DataFrame(fecha,columns=['fecha','del1','del2']).drop(columns=['del1','del2'])
    fecha = fecha_aux['fecha'].values.tolist()
    
    if len(re.findall('La publicación no menciona la fecha de resolución',text_aux)) != 0: 
        NA_fecha1 = [('NA') for i in range(len(re.findall('La publicación no menciona la fecha de resolución',text_aux)))]
        fecha.extend(NA_fecha1)
    
    #Si no son las mismas fechas que ponentes, agrega 'NA' a la lista
    if len(fecha) != len(ponentes): 
        NA_fecha2 = [('NA') for i in range(len(ponentes)-len(fecha))]
        fecha.extend(NA_fecha2)
    
    return fecha


def busqueda_secretarios(text_aux,ponentes):
    
    x0_secretario = re.findall("(?:Secretar\w\w: |Secretari\ws: |Secretari\w\. |secretari\w: )([\s\S]*?)(?:\.###|\. Amparo|\. Facultad| Amparo directo|\. Inconformidad|\. Acción|\. Varios|\. Controversia|\. Reconocimiento|\. Expediente vario|\. Consulta|\. Reposici\wn|\. \(|\. La |\. Incompetencia|\. Vol\wmenes|se encargo|Quinta Epoca:|\. Hay cosa|\. Acumulación|Impedimento|Antecedente:|Revisión|Expediente|Los señores|Jurisprudencia|demás que las|XIV.|las demás que|fallado|no superan|Aplicada|De conformidad|contra el|para el|Lo resolvió|Secretarrio:|Presidente|Secretario encargado|ha estimado|Disidente.|Veáse|\. Impedido:|Vease:|Por |Sexta Epoca|Integró|Para|Tribunal|\. Ausente|votos|_________________|Texto|Secretarios|Reproduce|Véanse:|Ponente:|EL|Tomo|Resuelto|Ausentes|Que |Varios|Con |\. Aclaración|Tomando|\. Juicio|Relator|\. Ministro|Incidente|/.|Texto aprobado|Relacionada|Séptima|Acción|Facultad|Controversia|\. Solicitud|Sostiene|La |\. Inejecución|Octava|En |Este |Se |\. Repetición|Reitera|\. El |Contradicción|La presente|El Tribunal|Tesis|La Primera|Sostienen|Informe|Véase|Esta|Importa|Disidentes:|Voto|Ausente:|Secretario:|###|Inconformidad|\. Conflicto|Nota|Criterios|Competencia|Precedente|\. Recurso| Recurso de|Secretaria|;|\. Nota\:|\. Notas\:|Nota\:|Pág\.|Vol|\. Volumen|\. Volúme|\.Tom|\. Véase|\. \. Amparo|\. Amparo di|\.   Amparo dir|\. Amparo in|Amparo en|\. Undécima Época|\. Décima Época|\. Novena Época|\. Octava Época|\. Séptima Época|\. Sexta Época|\. Quinta Época|\. Cuarta Época|\. Tercera Época|\. Segunda Época|\. Primera Época|\. Undécima Epoca|\. Décima Epoca|\. Novena Epoca|\. Octava Epoca|\. Séptima Epoca|\. Sexta Epoca|\. Quinta Epoca|\. Cuarta Epoca|\. Tercera Epoca|\. Segunda Epoca|\. Primera Epoca|\. Improcedencia civil|Sostiene la misma tesis:|\. Revisión fiscal|\. Unanimidad|\. Queja|Queja|\. Competencia|\. Reclamación|\.   Reclamación /.|\.  de enero de|\.  de febrero de|\.  de marzo de|\.  de abril de|\.  de mayo de|\.  de junio de|\.  de julio de|\.  de agosto de|\.  de septiembre de|\.  de octubre de|\.  de noviembre de|\.  de diciembre de|\. Disidente:|\. Precedentes|\. Improcedencia|\. Impedimento|\. Excusa|\. Incidente|\. Encargad|\. Revisión|\. Tomo|por licencia concedida|en funciones de Magistrado por Ministerio de Ley|\. Engrose: |\. Criterios|\. Tesis|\.   Tesis|\. El Tribunal|\. Contradicción de tesis|\. Texto|\. NOTA|\. Recurso de|\.   El Tribunal|\. Véanse|\.   Revisión|.   Notas|\. Semanario|\. Secretario|\. Tercera|\. C\. C\.)", text_aux)                                
    x1_secretario = re.findall("(?:La publicación |La publicacion)([\s\S]*?) (?:del ponente|el ponente)",text_aux)
    x10_secretario = 1
    secretarios = funcion_auxiliar_secretarios(x0_secretario,x1_secretario,x10_secretario)
    
    #Si no son los mismos secretarios que ponentes, agrega 'NA' a la lista
    if len(secretarios) != len(ponentes):
        NA_sec = [('NA') for i in range(len(ponentes)-len(secretarios))]
        secretarios.extend(NA_sec)
    
    return secretarios


def crea_tabla(id_tesis,tesis,instancia,epoca,materia,ponentes,secretarios,fecha):
    
    #Vectores para crear tabla
    vector_reiteracion = [(i+1) for i in range(len(ponentes))]
    vector_id_tesis = len(ponentes)*id_tesis
    vector_tesis = [(tesis) for i in range(len(ponentes))]
    vector_instancia = [(instancia) for i in range(len(ponentes))]
    vector_epoca = [(epoca) for i in range(len(ponentes))]
    vector_materia = [(materia) for i in range(len(ponentes))]

    tabla_iteracion = pd.DataFrame({'id_tesis':vector_id_tesis,'tesis':vector_tesis,'instancia':vector_instancia,'epoca':vector_epoca,'materia':vector_materia,'#_reiteracion':vector_reiteracion,'ponente':ponentes,'secretario':secretarios,'fecha':fecha})
                
    return tabla_iteracion