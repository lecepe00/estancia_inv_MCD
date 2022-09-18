![](./images/ITAM_MCD.jpeg)

# Análisis de Redes de Tesis de Jurisprudencia en México

Estancia de Investigación de la Maestría en Ciencia de Datos con el proyecto "Análisis de Redes de Tesis de Jurisprudencia en México", en colaboración con el [Dr. Julio Ríos Figueroa](https://rios-figueroa.com/) del departamento de Derecho del ITAM. 

En este proyecto se estudiarán las redes de creación de **tesis de jurisprudencia por reiteración** en México.  Se analizarán los mecanismos de la generación del *primer criterio* de una tesis aislada, así como los mecanismos de difusión para las reiteraciones sucesivas que culminan en la generación de una tesis de jurisprudencia por reiteración.

Colaboradores del proyecto:

| Nombre                   | Mail             | Usuario Gh |
|--------------------------|------------------|------------|
| Cecilia Avilés Robles    | cavilesr@itam.mx | cecyar     |
| Leonardo Ceja Pérez      | lcejaper@itam.mx | lecepe00   |

## Desarrollo del Proyecto

La estructura general del proyecto en la siguiente:

1. **Extracción de Datos**. De 260,303 archivos *.txt* que contienen cada uno una tesis del Semanario Judicial de la Federación, se buscan aquéllos referentes a *tesis de jurisprudencia por reiteración* únicamente. De éstos, se extraen datos comunes del encabezado así como datos particulares de Ponente, Secretario y Fecha de cada reiteración.
2. **Análisis Exploratorio de los Datos**. Del paso anterior, se obtiene un conjunto de datos con 56,557 registros, equivalentes a 11,278 tesis de jurisprudencia por reiteración. Con estos datos, se realiza un análisis exploratorio de los datos.
3. **Correlación de Datos Sociodemográficos**. Referencia cruzada de nombres obtenidos en el paso 1 con una base de datos sociodemográficos de los juzgadores y funcionarios del Poder Judicial de la Federación que posee el Dr. Ríos. Se asocian atributos sociodemográficos a 1,215 de los 1,641 Ponentes, y a 1,492 de los 5,521 Secretarios.
4. **Modelos de Clasificación**. Se desarrollaron modelos de clasificación que ayuden a pronosticar la *materia* o *instancia* de una tesis. El objetivo de estos modelos no es en realidad el desarrollar un algoritmo predictivo para estas dos etiquetas de interés, sino el de generar pistas sobre las características operacionales o sociodemográficas más representativas que ayuden a clasificar y filtrar las redes en redes más pequeñas que faciliten su entendimiento. En específico, se realizó una regresión logística multinomial y bosques aleatorios de clasificación.
  4.1. Clasificación de Materias
  4.2. Clasificación de Instancias
5. **Análisis de Redes**. Se crearon redes que nos ayudaran a entender los mecanismos de creación y reiteración de las tesis en cuestión. En general, se analizaron 3 redes distintas: Red Ponente-Secretario, Red Ponente-Ponente y Red Primer Criterio (Ponente-Secretario). Haciendo uso del aprendizaje obtenido en el paso 4, se analizaron sub-redes a partir de estas tres principales.
  5.1. Redes por Instancia
  5.2. Redes por Materia
  
## Lenguaje de Programación

Los puntos 1 y 2 explicados anteriormente fueron desarrollados en `Python 3.8.10`. Del punto 3 al 5 se trabajó en `R 4.2.1` con `RStudio 2022.07.1+554`.

## Estructura del Repositorio

La estructura general del repositorio es la siguiente:

```  
├── R_Markdown              <-  Archivos .Rmd para "Clasificación" y "Análisis de Redes"
├── graficas                <-  Archivos .html con todas las gráficas y tablas generadas
├── images                  <-  Imágenes utilizadas en este repositorio
├── notebooks               <-  Jupyter notebooks para "Extracción de Datos" y "EDA"
├── outbook                 <-  Guarda de manera local archivos .csv y .pkl usados a lo largo del proyecto
└── src                     <-  Códigos fuentes usados en el proyecto
    └── utils               <-  Módulos usados en "Extracción de Datos" y "EDA"
├── .gitignore              <-  Lista de archivos o carpetas ignorados por Git
├── README.md               <-  Readme del proyecto
├── estancia_inv_MCD.Rproj  <-  Proyecto en R para "Clasificación" y "Análisis de Redes"
```

Por cuestiones de privacidad y datos sensibles, para obtener los datos y reproducir el proyecto favor de ponerse en contacto con alguno de los colaboradores del proyecto: [Cecilia Avilés](mailto:cavilesr@itam.mx), [Leonardo Ceja](mailto:lcejaper@itam.mx) o [Julio Ríos](mailto:julio.rios@itam.mx)
