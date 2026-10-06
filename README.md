# El pulso mensual del mercado hipotecario español

Aplicación interactiva en Streamlit para explorar la evolución mensual de los préstamos hipotecarios formalizados en España por comunidad autónoma.

**Caso completo en el portfolio:** https://tomaspieroni-cloud.github.io/proyectos/hipotecas-streamlit.html

## Qué permite hacer

- Filtrar por año y por comunidad autónoma.
- Ver el número de hipotecas, la cuantía total, el importe medio y la estacionalidad mensual.
- Consultar la tabla de datos filtrada.

## Datos

Fuente: Colegio Oficial de Notarios de España. La aplicación lee el archivo `hipotecas_simplificado_plus.csv` (separador `;`) con las columnas `Año`, `Mes`, `Comunidad`, `Hipotecas` y `Cuantía`.

## Cómo ejecutarla

```
pip install -r requirements.txt
streamlit run app.py
```

## Limitaciones

- Describe datos observados: no realiza proyecciones.
- Las comparaciones entre comunidades deben considerar sus diferencias de tamaño.

**Autor:** Tomás Pieroni · Python · Streamlit · Pandas · Plotly
