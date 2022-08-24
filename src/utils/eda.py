import pandas as pd
import numpy as np
import re
from matplotlib.ticker import FuncFormatter


def number_formatter(number, pos=None):
    """
    Convierte número a un formato leíble
    """
    
    magnitude = 0
    while abs(number) >= 1000:
        magnitude += 1
        number /= 1000.0
    
    return '%d%s' % (number, ['', 'K', 'M', 'B', 'T', 'Q'][magnitude])


def cuenta_nulos_por_columnas(df):
    """
    Función que realiza una tabla con la cuenta de missing values por columna y obtiene 
    la proporción que estos missing values representan del total
    * Args:
         - df: el data frame al que se le va a realizar el conteo de los nulos por cada columna
    * Return:
         - Data Frame: entrega el data frame que indica cuántos elementos nulos fueron encontrados en cada columna
    """
    
    valores_nulos = df.isnull().sum()
    porcentaje_valores_nulos = 100 * df.isnull().sum() / len(df)
    tabla_valores_nulos = pd.concat([valores_nulos, porcentaje_valores_nulos], axis=1)
    tabla_valores_nulos_ordenada = tabla_valores_nulos.rename(
        columns={0: 'Missing Values', 1: '% del Total'})
    tabla_valores_nulos_ordenada = tabla_valores_nulos_ordenada[
        tabla_valores_nulos_ordenada.iloc[:, 1] != 0].sort_values(
        '% del Total', ascending=False).round(1)
    print("El dataframe tiene " + str(df.shape[1]) + " columnas.\n"
                                                     "Hay " + str(tabla_valores_nulos_ordenada.shape[0]) +
          " columnas que tienen NA's.")
    
    return tabla_valores_nulos_ordenada


def CreaTablaConteoPorcentaje(df, nomColumna, booleanNA):
    """
    Esta función crea la tabla con información sobre los conteos y el porcentaje al que corresponden del total de los datos
    * Args:
      - df: el data frame completo.
      - nomColumna: El nombre de la columna sobre la que se quiere realizar la tabla
      - booleanNA: Indicador booleano que indica si se requiere que se muestren los NA's en la tabla
    * Return:
      - Data Frame: entrega el data frame con el conteo pertinente y porcentaje
    """

    df_resultado = df[nomColumna].value_counts(dropna=booleanNA)
    df_resultado = pd.DataFrame(data=df_resultado)
    df_resultado = df_resultado.rename_axis(None)
    df_resultado = df_resultado.rename(columns={nomColumna: 'Conteo'})
    df_resultado = df_resultado['Conteo'].map('{:,}'.format)
    df_resultado = pd.DataFrame(data=df_resultado)

    #obteniendo los porcentajes
    df_resultado['%'] = df[nomColumna].value_counts(dropna=booleanNA, normalize=True).mul(100).round(2).astype(str)+'%'

    return df_resultado


def CreaTablaConteoPorcentajeGrupo(df,nomColumna,grupo,booleanNA):
    """
    Esta función crea la tabla con información sobre los conteos y el porcentaje al que 
    corresponden del total de los datos,considerando un grupo.
    * Args:
      - df: el data frame completo
      - nomColumna: El nombre de la columna sobre la que se quiere realizar la tabla
      - grupo: El nombre de la columna por el cual agrupar
      - booleanNA: Indicador booleano que indica si se requiere que se muestren los NA's en la tabla
    * Return:
      - Data Frame: entrega el data frame con el conteo pertinente y porcentaje
    """

    df_resultado = df.groupby([nomColumna])[grupo].nunique()
    df_resultado = pd.DataFrame(data=df_resultado)
    df_resultado = df_resultado.rename_axis(None)
    df_resultado = df_resultado.rename(columns={grupo: 'Conteo'})
    df_resultado = pd.DataFrame(data=df_resultado)
    df_resultado = df_resultado.astype({'Conteo':'int'}) 
    total_resultado = df_resultado['Conteo'].sum()
    df_resultado = df_resultado.sort_values(by=['Conteo'], ascending=False)
    df_resultado['%'] = df_resultado['Conteo']/total_resultado*100  
    df_resultado['%'] = df_resultado['%'].round(2).astype(str)+'%' 
    df_resultado['Conteo'] = df_resultado['Conteo'].apply('{:,}'.format)

    return df_resultado


def StringLowercase(df):
    """
    Función cambiar todos los strings de un dataframe a lowercase (columnas y observaciones)
    * Args:
         - df: dataframe al que se desea hacer la modificación
    * Return:
         - df: dataframe modificado
    """
    
    ### Columnas
    DataFrameColumns = df.columns

    for col in DataFrameColumns:
        df.rename(columns={col:col.lower()}, inplace=True)

    ### Observaciones
    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        if col != 'geometry':
            df[col] = df[col].str.lower()

    return df


def StringAcentos(df):
    """
    Función para eliminar acentos, dieresis y eñes de los strings de un dataframe (columnas y observaciones)
    * Args:
         - df: dataframe al que se desea hacer la modificación
    * Return:
         - df: dataframe modificado
    """
    
    ### Columnas
    df.columns = df.columns.str.replace('á', 'a')
    df.columns = df.columns.str.replace('é', 'e')
    df.columns = df.columns.str.replace('í', 'i')
    df.columns = df.columns.str.replace('ó', 'o')
    df.columns = df.columns.str.replace('ú', 'u')
    df.columns = df.columns.str.replace('ü', 'u')
    df.columns = df.columns.str.replace('ñ', 'n')

    ### Observaciones
    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        if col != 'geometry':
            df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    return df


def StringStrip(df):
    """
    Función para eliminar espacios al inicio y al final de los strings de un dataframe (columnas y observaciones)
    * Args:
         - df: dataframe al que se desea hacer la modificación
    * Return:
         - df: dataframe modificado
    """
    
    ### Columnas
    df.columns = [col.strip() for col in df.columns]

    ### Observaciones
    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        if col != 'geometry':
            df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def StringEspacios(df):
    """
    Función para eliminar espacios dobles (o mas) de los strings de un
    dataframe (columnas y observaciones)
    * Args:
         - df: dataframe al que se desea hacer la modificación
    * Return:
         - df: dataframe modificado
    """
    
    ### Columnas
    df.columns = [re.sub(' +', ' ', col) for col in df.columns]

    ### Observaciones
    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        if col != 'geometry':
            df[col] = df[col].apply(lambda x: re.sub(' +', ' ', x) if isinstance(x, str) else x)

    return df


def EstandarizaFormato(df):
    """
    Función para estandarizar un dataframe: minúsculas, sin espacios en blanco,
    sin signos de puntuación (columnas y observaciones)
    * Args:
         - df: dataframe al que se desea hacer la modificación
    * Return:
         - df: dataframe modificado
    """

    ### Minúsculas
    df = StringLowercase(df)

    ### Acentos
    df = StringAcentos(df)

    ### Quitamos espacios al principio y al final
    df = StringStrip(df)

    ### Quitamos espacios
    df = StringEspacios(df)
    
    ### Quita espacios en columnas
    df.columns = df.columns.str.replace(' ', '_')

    return df


def genera_profiling_de_numericos(df,lista_numericas,vars_type):
    """
    Función que genera un perfilamiento para los datos numéricos
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento para variables numéricas
         - lista_numericas: una lista con el nombre de las variables que son de tipo numérico
         - vars_type: tabla con el tipo de variable
    * Return:
         - Data Frame: Data Frame con el perfilamiento para las variables numéricas
    """
    
    # Obtenemos los estadísticos de la columna si es numérica
    lista_perfilamiento_numerico = ['Tipo','Número de observaciones', 'Media', 'Desviación estándar',
                                    'Cuartil 25%','Cuartil 50%','Cuartil 75%','Mínimo','Máximo',
                                    'Número de observaciones únicas','Número de faltantes','Top1/veces/%',
                                    'Top2/veces/%','Top3/veces/%'
                                    ,'Top4/veces/%','Top5/veces/%']
    datos_dataframe_profiling_numericas = {'Métrica':lista_perfilamiento_numerico}
    dataframe_profiling_numericas = pd.DataFrame(data=datos_dataframe_profiling_numericas)
    
    for col in lista_numericas:
        # Tipo de dato
        vars_type_num = pd.DataFrame(vars_type)
        df_tipo = pd.DataFrame(data=vars_type_num.loc[vars_type_num["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]

        # Obtenemos las métricas relevantes
        descr_col = df[col].describe()
        descr_col = pd.DataFrame(descr_col)
        descr_col['Métrica']=descr_col.index
        descr_col.columns=['valor','Métrica']

        # Número de observaciones
        medida = 'count'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        num_observaciones_num = metrica['valor'][0]

        # Media
        medida = 'mean'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        media_obs_num = metrica['valor'][0]
        media_obs_num = media_obs_num.round(2)

        # Desviacion estándar
        medida = 'std'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        sd_obs_num = metrica['valor'][0]
        sd_obs_num = sd_obs_num.round(2)

        # Cuartil 25
        medida = '25%'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        cuant_25_obs_num = metrica['valor'][0]
        cuant_25_obs_num = cuant_25_obs_num.round(2)

        # Cuartil 50
        medida = '50%'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        cuant_50_obs_num = metrica['valor'][0]
        cuant_50_obs_num = cuant_50_obs_num.round(2)

        # Cuartil 75
        medida = '75%'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        cuant_75_obs_num = metrica['valor'][0]
        cuant_75_obs_num = cuant_75_obs_num.round(2)
        
        # Mínimo
        medida = 'min'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        minimo_obs_num = metrica['valor'][0]
        minimo_obs_num = minimo_obs_num.round(2)

        # Máximo
        medida = 'max'
        metrica = descr_col.loc[descr_col["Métrica"] == medida]
        maximo_obs_num = metrica['valor'][0]
        maximo_obs_num = maximo_obs_num.round(2)

        # Número de observaciones únicas
        num_obs_unicas_obs_num = df[col].nunique()

        # Número de observaciones con valores faltantes
        obs_faltantes_obs_num = df[col].isna().sum()

        # generamos tabla para las modas
        tabla_importantes = CreaTablaConteoPorcentaje(df,str(col),True)
        tabla_importantes.columns = ['conteo','porcentaje']

        top1 = tabla_importantes.index[0]
        veces1 = list(tabla_importantes['conteo'])[0]
        porcentaje1 = list(tabla_importantes['porcentaje'])[0]
        datos_top1 = [top1,veces1,porcentaje1]

        if(len(tabla_importantes)>1):
            top2 = tabla_importantes.index[1]
            veces2 = list(tabla_importantes['conteo'])[1]
            porcentaje2 = list(tabla_importantes['porcentaje'])[1]
            datos_top2 = [top2,veces2,porcentaje2]
        else:
            datos_top2 = ['NA','NA','NA']

        if(len(tabla_importantes)>2):
            top3 = tabla_importantes.index[2]
            veces3 = list(tabla_importantes['conteo'])[2]
            porcentaje3 = list(tabla_importantes['porcentaje'])[2]
            datos_top3 = [top3,veces3,porcentaje3]
        else:
            datos_top3 = ['NA','NA','NA']

        if(len(tabla_importantes)>3):
            top4 = tabla_importantes.index[3]
            veces4 = list(tabla_importantes['conteo'])[3]
            porcentaje4 = list(tabla_importantes['porcentaje'])[3]
            datos_top4 = [top4,veces4,porcentaje4]
        else:
            datos_top4 = ['NA','NA','NA']

        if(len(tabla_importantes)>4):
            top5 = tabla_importantes.index[4]
            veces5 = list(tabla_importantes['conteo'])[4]
            porcentaje5 = list(tabla_importantes['porcentaje'])[4]
            datos_top5 = [top5,veces5,porcentaje5]
        else:
            datos_top5 = ['NA','NA','NA']
        
        datos_variable = [tipo_dato,num_observaciones_num,media_obs_num,sd_obs_num,
                          cuant_25_obs_num, cuant_50_obs_num,cuant_75_obs_num,minimo_obs_num,
                          maximo_obs_num,num_obs_unicas_obs_num,obs_faltantes_obs_num,datos_top1,datos_top2,datos_top3,
                          datos_top4,datos_top5]
        dataframe_profiling_numericas[col]=datos_variable
    
    return dataframe_profiling_numericas


def genera_profiling_de_categorias(df, lista_category,vars_type):
    """
    Función que genera un perfilamiento para los datos categóricos
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento para variables categóricas
         - lista_category: una lista con el nombre de las variables que son de tipo categórico
         - vars_type: tabla con el tipo de variable
    * Return:
         - Data Frame: Data Frame con el perfilamiento para las variables categóricas
    """
    
    # Obtenemos los estadísticos de la columna si es categórica
    lista_perfilamiento_categorico = ['Tipo','Número de categorías', 'Número de observaciones',
                                      'Obs. nulas','% Obs. nulas', 'Obs. NA','% Obs. NA','Valores únicos',
                                      'Moda1/veces/%','Moda2/veces/%','Moda3/veces/%']
    datos_dataframe_profiling_categoricos = {'Métrica':lista_perfilamiento_categorico}
    dataframe_profiling_categoricas = pd.DataFrame(data=datos_dataframe_profiling_categoricos)
    
    for col in lista_category:
        
        # Tipo de dato
        vars_type_cat = pd.DataFrame(vars_type)
        
        # vars_type_cat
        df_tipo = pd.DataFrame(data=vars_type_cat.loc[vars_type_cat["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]

        # Obtenemos las métricas relevantes
        descr_col = df[col]
        descr_col = pd.DataFrame(descr_col)
        descr_col['metrica']=descr_col.index
        descr_col.columns=['valor','Métrica']

        # Número de categorías
        num_categorias=descr_col.nunique()["valor"]
        
        # Número de observaciones
        num_observaciones=len(descr_col)

        # Valores nulos
        num_obs_nulas=df[col].isna().sum()

        # Porcentaje valores nulos
        por_obs_nulas=str(round(num_obs_nulas/num_observaciones*100, 2))+'%'
        
        # Valores NA
        num_obs_NA=(df[col].values=='NA').sum()

        # Porcentaje valores NA
        por_obs_NA=str(round(num_obs_NA/num_observaciones*100, 2))+'%'

        # Valor de las categorías
        valores_unicos = list(df[col].unique())

        # Generamos tabla para las modas
        tabla_importantes = CreaTablaConteoPorcentaje(df,str(col),True)
        tabla_importantes.columns = ['conteo','porcentaje']

        moda1 = tabla_importantes.index[0]
        veces1 = tabla_importantes['conteo'][0]
        porcentaje1 = tabla_importantes['porcentaje'][0]
        datos_moda1 = [moda1,veces1,porcentaje1]

        moda2 = tabla_importantes.index[1]
        veces2 = tabla_importantes['conteo'][1]
        porcentaje2 = tabla_importantes['porcentaje'][1]
        datos_moda2 = [moda2,veces2,porcentaje2]

        moda3 = tabla_importantes.index[2]
        veces3 = tabla_importantes['conteo'][2]
        porcentaje3 = tabla_importantes['porcentaje'][2]
        datos_moda3 = [moda3,veces3,porcentaje3]
        
        # Formato
        num_categorias='{:0,.0f}'.format(num_categorias)
        num_observaciones='{:0,.0f}'.format(num_observaciones)
        num_obs_nulas='{:0,.0f}'.format(num_obs_nulas)
        num_obs_NA='{:0,.0f}'.format(num_obs_NA)

        datos_variable = [tipo_dato,num_categorias,num_observaciones,num_obs_nulas,por_obs_nulas,
                          num_obs_NA,por_obs_NA,valores_unicos,datos_moda1,datos_moda2,datos_moda3]
        dataframe_profiling_categoricas[col]=datos_variable
        
    return dataframe_profiling_categoricas


def genera_profiling_de_texto(df,lista_texto,vars_type):
    """
    Función que genera un perfilamiento para los datos de tipo texto
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento para variables de texto
         - lista_texto: una lista con el nombre de las variables que son de tipo texto (object)
         - vars_type: tabla con el tipo de variable
    * Return:
         - Data Frame: Data Frame con el perfilamiento para las variables de tipo texto
    """
    
    # Obtenemos los estadísticos de la columna si es catagorica
    lista_perfilamiento_txt = ['Tipo','Número de observaciones', 'Obs. únicas', '% Observaciones únicas',
                                    'Tamaño promedio','Tamaño mínimo','Tamaño máximo']
    datos_dataframe_profiling_txt = {'Métrica':lista_perfilamiento_txt}
    dataframe_profiling_txt = pd.DataFrame(data=datos_dataframe_profiling_txt)
    
    for col in lista_texto:
        
        # Tipo de dato
        vars_type_txt = pd.DataFrame(vars_type)
        
        # vars_type_txt
        df_tipo = pd.DataFrame(data=vars_type_txt.loc[vars_type_txt["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]

        # Obtenemos las métricas relevantes
        descr_col = df[col]
        descr_col = pd.DataFrame(descr_col)
        descr_col['Métrica']=descr_col.index
        descr_col.columns=['valor','Métrica']

        # Número de observaciones
        num_observaciones=len(descr_col)

        # Observaciones únicas
        num_obs_unicas=df[col].nunique()

        # % Observaciones únicas
        por_obs_unicas=num_obs_unicas/num_observaciones

        # Tamaño promedio
        tam_prom=df[col].str.len().mean()

        # Tamaño mínimo
        tam_min=df[col].str.len().min()

        # Tamaño máximo
        tam_max=df[col].str.len().max()

        datos_variable = [tipo_dato,num_observaciones,num_obs_unicas,por_obs_unicas,tam_prom,tam_min,tam_max]
        dataframe_profiling_txt[col]=datos_variable
    
    return dataframe_profiling_txt


def genera_profiling_de_fechas(df,lista_date,vars_type):
    """
    Función que genera un perfilamiento para los datos de tipo fecha
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento para variables de fecha
         - lista_date: una lista con el nombre de las variables que son de tipo fecha
         - vars_type: tabla con el tipo de variable
    * Return:
         - Data Frame: Data Frame con el perfilamiento para las variables de fecha
    """
    
    # Obtenemos los estadísticos de la columna si es fecha
    lista_perfilamiento_fechas = ['Tipo','Número de observaciones', 'Mínimo','Máximo',
                                  'Número de obs. únicas','Número de faltantes','Top1/veces/%',
                                    'Top2/veces/%','Top3/veces/%']
    
    datos_dataframe_profiling_fechas = {'Métrica':lista_perfilamiento_fechas}
    dataframe_profiling_fechas = pd.DataFrame(data = datos_dataframe_profiling_fechas)
    
    for col in lista_date:
        # Tipo de dato
        vars_type_fechas = pd.DataFrame(vars_type)
        
        # vars_type
        df_tipo = pd.DataFrame(data = vars_type_fechas.loc[vars_type_fechas["variable"] == col])
        tipo_dato = df_tipo['tipo'][0]

        # Número de observaciones
        num_observaciones = df[col].count()

        # Mínimo
        minimo_obs = str(df[col].min())[:10]

        # Máximo
        maximo_obs = str(df[col].max())[:10]
        
        # Número de observaciones unicas
        num_obs_unicas = df[col].nunique()

        # Número de observaciones con valores faltantes
        obs_faltantes = df[col].isna().sum()

        # Generamos tabla para las modas
        tabla_importantes = CreaTablaConteoPorcentaje(df,str(col),True)
        tabla_importantes.columns = ['conteo','porcentaje']

        top1 = str(tabla_importantes.index[0])[:10]
        veces1 = list(tabla_importantes['conteo'])[0]
        porcentaje1 = list(tabla_importantes['porcentaje'])[0]
        datos_top1 = [top1,veces1,porcentaje1]

        if(len(tabla_importantes)>1):
            top2 = str(tabla_importantes.index[1])[:10]
            veces2 = list(tabla_importantes['conteo'])[1]
            porcentaje2 = list(tabla_importantes['porcentaje'])[1]
            datos_top2 = [top2,veces2,porcentaje2]
        else:
            datos_top2 = ['NA','NA','NA']

        if(len(tabla_importantes)>2):
            top3 = str(tabla_importantes.index[2])[:10]
            veces3 = list(tabla_importantes['conteo'])[2]
            porcentaje3 = list(tabla_importantes['porcentaje'])[2]
            datos_top3 = [top3,veces3,porcentaje3]
        else:
            datos_top3 = ['NA','NA','NA']
            
        # Formato
        num_observaciones='{:0,.0f}'.format(num_observaciones)
        num_obs_unicas='{:0,.0f}'.format(num_obs_unicas)
        obs_faltantes='{:0,.0f}'.format(obs_faltantes)
        
        datos_variable = [tipo_dato, num_observaciones, minimo_obs, maximo_obs,
                          num_obs_unicas, obs_faltantes, datos_top1, datos_top2, datos_top3]
        dataframe_profiling_fechas[col] = datos_variable
    
    return dataframe_profiling_fechas


def genera_profiling_por_variable(df):
    """
    Función que genera un perfilamiento para cada tipo de variable en el data frame
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento por variable
    * Return:
         - profiling_numericas: Data Frame con el perfilamiento para las variables numéricas
         - profiling_categoricas: Data Frame con el perfilamiento para las variables categóricas
         - profiling_de_texto: Data Frame con el perfilamiento para las variables de tipo texto
         - profiling_fechas: Data Frame con el perfilamiento para las variables de tipo fecha
    """
    # Dividimos variables por tipo de datos
    vars_type = df.dtypes
    vars_type = pd.DataFrame(vars_type, columns = ['tipo'])
    vars_type['variable'] = vars_type.index

    # Variables numéricas
    variables_int = vars_type.loc[vars_type["tipo"] == "int64"]
    variables_float = vars_type.loc[vars_type["tipo"] == "float64"]
    variables_numericas = variables_int.append(variables_float, ignore_index=True)
    lista_numericas = list(variables_numericas['variable'])

    # Variables fecha
    variables_date = vars_type.loc[vars_type["tipo"] == 'datetime64[ns]']
    lista_date = list(variables_date['variable'])

    # Variables categóricas
    variables_category = vars_type.loc[vars_type["tipo"] == "category"]
    lista_category = list(variables_category['variable'])

    # Variables texto
    variables_texto = vars_type.loc[vars_type["tipo"] == "object"]
    lista_texto = list(variables_texto['variable'])

    if len(lista_numericas)==0:
        profiling_numericas = "No hay variables numéricas"
    else:
        profiling_numericas = genera_profiling_de_numericos(df,lista_numericas,vars_type)

    if len(lista_category)==0:
        profiling_categoricas = "No hay variables categóricas"
    else:
        profiling_categoricas = genera_profiling_de_categorias(df,lista_category,vars_type)

    if len(lista_texto)==0:
        profiling_texto = "No hay variables de tipo texto"
    else:
        profiling_texto = genera_profiling_de_texto(df,lista_texto,vars_type)
        
    if len(lista_date)==0:
        profiling_fechas = "No hay variables de fecha"
    else:
        profiling_fechas = genera_profiling_de_fechas(df,lista_date,vars_type)

    return (profiling_numericas,profiling_categoricas,profiling_texto,profiling_fechas)


def genera_profiling_general(df):
    """
    Función que genera la tabla con un perfilamiento general del data set, sin entrar al detalle por variable
    * Args:
         - df: el data frame al que se le va a realizar el perfilamiento general
    * Return:
         - Data Frame: entrega el data frame con un perfilamiento general del data set
    """
    
    cuenta_de_variables = len(df.columns)
    cuenta_observaciones = len(df)
    total_celdas = cuenta_de_variables*cuenta_observaciones

    # Contamos el tipo de datos del dataset
    vars_type = df.dtypes
    vars_type = pd.DataFrame(vars_type, columns = ['tipo'])

    # Asignamos un valor para cada tipo

    ## Numéricas
    cantidad_numericas = len(vars_type.loc[vars_type["tipo"] == "int64"])
    cantidad_numericas = cantidad_numericas + len(vars_type.loc[vars_type["tipo"] == "float64"])

    ## Fechas
    cantidad_fecha = len(vars_type.loc[vars_type["tipo"] == "datetime64[ns]"])

    ## Categóricas
    cantidad_categoricas = len(vars_type.loc[vars_type["tipo"] == "category"])

    ## Texto
    cantidad_texto = len(vars_type.loc[vars_type["tipo"] == "object"])

    # Contamos los faltantes
    nulos_totales = cuenta_nulos_por_columnas(df)['Missing Values'].sum()

    # Obtenemos el porcentaje de datos que son faltantes
    nulos_porcentaje = ((nulos_totales/(total_celdas))*100).round(1).astype(str)+'%'

    # Obtenemos el total de columnas duplicadas
    ds_duplicados = df.duplicated(subset=None, keep='first')
    ds_duplicados = pd.DataFrame(ds_duplicados,columns = ['duplicated'])
    numero_de_duplicados = len(ds_duplicados.loc[ds_duplicados["duplicated"] == True])

    # Obtenemos el porcentaje de duplicados
    porcentaje_de_duplicados = str(((numero_de_duplicados/(total_celdas))*100))+'%'

    estadisticas = ['Total de variables','Conteo de observaciones','Total de celdas',
                        'Cantidad de variables numéricas','Cantidad de variables de fecha',
                        'Cantidad de variables categóricas', 'Cantidad de variables de texto',
                        'Valores faltantes','Porcentaje de valores faltantes',
                        'Renglones duplicados', 'Porcentaje de valores duplicados']

    valores_estadisticas = [cuenta_de_variables,cuenta_observaciones,total_celdas,cantidad_numericas,
                        cantidad_fecha,cantidad_categoricas,cantidad_texto,nulos_totales,nulos_porcentaje,
                        numero_de_duplicados,porcentaje_de_duplicados]

    valores = {'Estadísticas':estadisticas,'Resultado':valores_estadisticas}

    df_perfilamiento_general = pd.DataFrame(data=valores)
    
    return df_perfilamiento_general