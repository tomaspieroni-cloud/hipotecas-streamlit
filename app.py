"""
Aplicación web para visualizar la evolución de los préstamos hipotecarios
en España por Comunidades Autónomas

Alumno: Tomás Nelio Pieroni
"""

# Importo librerias
import pandas as pd
import streamlit as st
from plotly import graph_objects as go

#_______________________________
#   CARGO LOS DATOS

# Leo el archivo csv de los datos. 
df = pd.read_csv("hipotecas_simplificado_plus.csv", sep=";")

# Creo una nueva variable de fecha uniendo las columnas de año y mes.
# Esto me permite ordenar correctamente la serie temporal en el eje X de mis gráficos
df["Fecha"] = pd.to_datetime(df["Año"].astype(str) + "-" + df["Mes"].astype(str))

# Calculo el importe medio de cada hipoteca dividiendo la cuantía total entre el número de hipotecas.
df["Hipoteca_media"] = df["Cuantía"] / df["Hipotecas"]

# Ordeno mi conjunto de datos cronológicamente usando la fecha que acabo de crear
df = df.sort_values("Fecha")

# Obtengo una lista limpia y ordenada alfabeticamente de las comunidades autonomas disponibles
comunidades = sorted(df["Comunidad"].unique())

# Obtengo una lista ordenada de los años para usarla en mi filtro lateral
años = sorted(df["Año"].unique())




#_____________________________
#   Configuro la App web 

# Defino el título principal que se mostrará en mi aplicación
st.title("Análisis de préstamos hipotecarios en España")

# Escribo una breve descripción para que el usuario entienda el propósito de la app.
st.write(
"""
Esta aplicación permite visualizar la evolución mensual de los préstamos 
hipotecarios formalizados en España por Comunidades Autónomas

Fuente de datos: Colegio Oficial de Notarios de España
"""
)

# Añado una línea separadora visual.
st.divider()



#_______________________________________
#   SELECCIONAMOS AÑOS Y COMUNIDADES AUTÓNOMAS

# Creo un encabezado en la barra lateral de opciones.
st.sidebar.header("Opciones de visualización")

# Cambio el selector a 'multiselect' para permitir elegir varios años a la vez.
# Por defecto, le paso la lista completa para que todos los años estén seleccionados de inicio.
años_elegidos = st.sidebar.multiselect(
    "Seleccionar años:",
    options=años,
    default=años
)

# Filtro mi dataframe original para quedarme SOLO con los datos de los años que he seleccionado.
# A partir de aquí, usaré 'df_filtrado' en lugar de 'df' para que la app sea interactiva.
df_filtrado = df[df["Año"].isin(años_elegidos)]


# Utilizo la barra lateral para permitir la selección de múltiples comunidades.
# Por defecto marco las 3 primeras de mi lista.
comunidades_elegidas = st.sidebar.multiselect(
    "Seleccionar Comunidades Autónomas:",
    comunidades,
    default=comunidades[:3]
)


#___________________________________
# Número de hipotecas - gráfico

st.subheader("Número de hipotecas")

# Inicializo mi primera figura de Plotly
fig1 = go.Figure()

# Recorro con un bucle cada comunidad que el usuario ha seleccionado.
for com in comunidades_elegidas:
    
    # IMPORTANTE: Filtro usando 'df_filtrado' para respetar el filtro de los años.
    datos = df_filtrado[df_filtrado["Comunidad"] == com]
    datos = datos.sort_values("Fecha")

    # Añado una traza (línea) a mi gráfico por cada comunidad iterada.
    # Uso mode="lines+markers" para marcar los puntos de cada mes y ver mejor la estacionalidad.
    fig1.add_trace(
        go.Scatter(
            x=datos["Fecha"],
            y=datos["Hipotecas"],
            mode="lines+markers", 
            name=com
        )
    )

# Personalizo los titulos de los ejes X e Y de mi primer gráfico
fig1["layout"]["xaxis"]["title"] = "Fecha"
fig1["layout"]["yaxis"]["title"] = "Número de hipotecas"

# Renderizo el gráfico en Streamlit, ajustándolo al ancho de la pantalla.
st.plotly_chart(fig1, use_container_width=True)


#___________________________________
# Cuantía total - gráfico

st.subheader("Cuantía total de las hipotecas")

# Inicializo mi segunda figura.
fig2 = go.Figure()

# Repito el bucle para generar el gráfico de la cuantía total
for com in comunidades_elegidas:

    # Vuelvo a usar 'df_filtrado' para aplicar el filtro temporal
    datos = df_filtrado[df_filtrado["Comunidad"] == com]
    datos = datos.sort_values("Fecha")

    # Añado la traza, nuevamente con marcadores para apreciar el dato mes a mes.
    fig2.add_trace(
        go.Scatter(
            x=datos["Fecha"],
            y=datos["Cuantía"],
            mode="lines+markers",
            name=com
        )
    )

# Personalizo los ejes de mi segundo grafico
fig2["layout"]["xaxis"]["title"] = "Fecha"
fig2["layout"]["yaxis"]["title"] = "Cuantía total (€)"

# Pinto el gráfico en la web
st.plotly_chart(fig2, use_container_width=True)


#___________________________________
# Hipotecas valor media - gráfico

st.subheader("Importe medio de las hipotecas")

# Inicializo mi tercera figura.
fig3 = go.Figure()

# Repito el bucle para graficar la variable que calculé al principio (Hipoteca_media)
for com in comunidades_elegidas:

    datos = df_filtrado[df_filtrado["Comunidad"] == com]
    datos = datos.sort_values("Fecha")

    fig3.add_trace(
        go.Scatter(
            x=datos["Fecha"],
            y=datos["Hipoteca_media"],
            mode="lines+markers",
            name=com
        )
    )

fig3["layout"]["xaxis"]["title"] = "Fecha"
fig3["layout"]["yaxis"]["title"] = "Importe medio (€)"

st.plotly_chart(fig3, use_container_width=True)



#___________________________________
# Agregamos estacionalidad por mes de las hipotecas

# Creo una cadena de texto uniendo los años seleccionados separados por comas.
años_str = ", ".join(map(str, años_elegidos))

# Añado la variable de los años al subtítulo para que quede documentado en la web.
st.subheader(f"Estacionalidad mensual (Promedio de los años: {años_str})")

# Calculo el promedio histórico de hipotecas por cada mes del año.
# Al usar 'df_filtrado', la media agrupa únicamente los años que estén seleccionados
estacionalidad = df_filtrado.groupby("Mes")["Hipotecas"].mean().reset_index()

# Inicializo mi cuarta figura para el gráfico de barras
fig4 = go.Figure()

# Añado una traza de tipo Bar para visualizar el promedio mensual
fig4.add_trace(
    go.Bar(
        x=estacionalidad["Mes"],
        y=estacionalidad["Hipotecas"]
    )
)

# Nombro los ejes de mi gráfico de estacionalidad y vuelvo a poner los años en el eje Y por claridad
fig4["layout"]["xaxis"]["title"] = "Mes"
fig4["layout"]["yaxis"]["title"] = f"Promedio de hipotecas ({años_str})"

# Muestro finalmente el gráfico de barras en la app
st.plotly_chart(fig4, use_container_width=True)


#___________________________________
# Insertar tabla de datos

st.divider()

# Agrego un checkbox por si el usuario quiere inspeccionar los datos
if st.checkbox("Mostrar tabla de datos"):
    # Muestro 'df_filtrado' para que la tabla también refleje los años seleccionados.
    st.dataframe(df_filtrado)
