import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import requests

st.set_page_config(layout="wide")
st.title("Geomarketing Analysis MVP for MiPymes in Mexico City")
st.write("This application helps MiPymes (Micro, Small, and Medium-sized Enterprises) in Mexico City make data-driven decisions for market strategy, expansion, and competitive positioning.")


# --- CONFIGURACIÓN Y FUNCIONES ---

# Retrieve TOKEN securely from Streamlit secrets
TOKEN = st.secrets['TOKEN']

def consultar_denue(token, condicion, lat, lon, metros):
    url = f"https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/{condicion}/{lat},{lon}/{metros}/{token}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if not data:
            st.warning("No se encontraron resultados para la consulta.")
            return None

        df = pd.DataFrame(data)

        df['Latitud'] = pd.to_numeric(df['Latitud'], errors='coerce')
        df['Longitud'] = pd.to_numeric(df['Longitud'], errors='coerce')
        df = df.dropna(subset=['Latitud', 'Longitud'])

        geometry = [Point(xy) for xy in zip(df.Longitud, df.Latitud)]
        gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

        st.success(f"Éxito: Se encontraron {len(gdf)} establecimientos.")
        return gdf

    except requests.exceptions.RequestException as e:
        st.error(f"Error en la solicitud a la API: {e}")
        return None
    except Exception as e:
        st.error(f"Error al procesar los datos: {e}")
        return None

def calculate_density(gdf_negocios, cell_size=200):
    if gdf_negocios.empty:
        return gpd.GeoDataFrame()

    gdf_proj = gdf_negocios.to_crs(epsg=6372) # Projected CRS for Mexico City

    minx_proj, miny_proj, maxx_proj, maxy_proj = gdf_proj.total_bounds

    x_coords = np.arange(minx_proj, maxx_proj + cell_size, cell_size)
    y_coords = np.arange(miny_proj, maxy_proj + cell_size, cell_size)

    grid_cells = []
    for x in x_coords[:-1]:
        for y in y_coords[:-1]:
            grid_cells.append(Polygon([(x, y), (x + cell_size, y), (x + cell_size, y + cell_size), (x, y + cell_size)]))

    grid_gdf = gpd.GeoDataFrame(geometry=grid_cells, crs=gdf_proj.crs)

    gdf_proj['business_count'] = 1
    joined_gdf = gpd.sjoin(grid_gdf, gdf_proj, how="left", predicate='intersects')

    density_gdf = joined_gdf.groupby(joined_gdf.index).agg({
        'business_count': 'sum',
        'geometry': 'first'
    }).reset_index(drop=True)
    density_gdf = gpd.GeoDataFrame(density_gdf, geometry='geometry', crs=gdf_proj.crs)
    density_gdf = density_gdf.rename(columns={'business_count': 'num_businesses'})
    density_gdf['num_businesses'] = density_gdf['num_businesses'].fillna(0).astype(int)

    return density_gdf.to_crs(epsg=4326) # Reproject back to WGS84 for Folium

def filter_businesses(gdf, actividad=None, estrato=None):
    filtered_gdf = gdf.copy()
    if actividad and actividad != "All":
        filtered_gdf = filtered_gdf[filtered_gdf['Clase_actividad'] == actividad]
    if estrato and estrato != "All":
        filtered_gdf = filtered_gdf[filtered_gdf['Estrato'] == estrato]
    return filtered_gdf

def create_enhanced_map(gdf_negocios, density_gdf_wgs84, filtered_gdf=None, map_center=None, zoom_start=12):
    if map_center is None:
        if not gdf_negocios.empty:
            map_center = [gdf_negocios.geometry.y.mean(), gdf_negocios.geometry.x.mean()]
        else:
            map_center = [19.4326, -99.1332] # Default to CDMX center

    m = folium.Map(location=map_center, zoom_start=zoom_start, tiles='OpenStreetMap')

    if not density_gdf_wgs84.empty:
        density_gdf_wgs84['id'] = density_gdf_wgs84.index.astype(str)
        folium.Choropleth(
            geo_data=density_gdf_wgs84.to_json(),
            name='Business Density',
            data=density_gdf_wgs84,
            columns=['id', 'num_businesses'],
            key_on='feature.properties.id',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Number of Businesses per Cell',
            highlight=True
        ).add_to(m)

    if not gdf_negocios.empty:
        marker_cluster_all = MarkerCluster(name="All Businesses").add_to(m)
        for idx, row in gdf_negocios.iterrows():
            popup_text = f"""
            <b>Nombre:</b> {row.get('Nombre', 'N/A')}<br>
            <b>Actividad:</b> {row.get('Clase_actividad', 'N/A')}<br>
            <b>Estrato:</b> {row.get('Estrato', 'N/A')}<br>
            <b>Dirección:</b> {row.get('Ubicacion', 'N/A')}
            """
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_text, max_width=300)
            ).add_to(marker_cluster_all)

    if filtered_gdf is not None and not filtered_gdf.empty:
        filtered_marker_cluster = MarkerCluster(name="Filtered Businesses").add_to(m)
        for idx, row in filtered_gdf.iterrows():
            popup_text = f"""
            <b>Nombre:</b> {row.get('Nombre', 'N/A')}<br>
            <b>Actividad:</b> {row.get('Clase_actividad', 'N/A')}<br>
            <b>Estrato:</b> {row.get('Estrato', 'N/A')}<br>
            <b>Dirección:</b> {row.get('Ubicacion', 'N/A')}
            """
            folium.Marker(
                location=[row['Latitud'], row['Longitud']],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color='green', icon='star')
            ).add_to(filtered_marker_cluster)

    folium.LayerControl().add_to(m)
    return m

# --- Streamlit UI ---

st.sidebar.header("1. Customize Search Parameters")
condicion_input = st.sidebar.text_input("Business Type (e.g., cafeterias, restaurantes)", "cafeterias")
latitud_input = st.sidebar.number_input("Latitude", value=19.3496, format="%.4f")
longitud_input = st.sidebar.number_input("Longitude", value=-99.1601, format="%.4f")
distancia_metros_input = st.sidebar.slider("Search Radius (meters)", 100, 5000, 3000)

if st.sidebar.button("Run Search and Analysis"):
    with st.spinner("Fetching data and performing analysis..."):
        gdf_negocios = consultar_denue(TOKEN, condicion_input, latitud_input, longitud_input, distancia_metros_input)
        if gdf_negocios is not None and not gdf_negocios.empty:
            st.session_state['gdf_negocios'] = gdf_negocios
            st.session_state['density_gdf_wgs84'] = calculate_density(gdf_negocios)
        else:
            st.session_state['gdf_negocios'] = gpd.GeoDataFrame()
            st.session_state['density_gdf_wgs84'] = gpd.GeoDataFrame()

if 'gdf_negocios' in st.session_state and not st.session_state['gdf_negocios'].empty:
    gdf_negocios = st.session_state['gdf_negocios']
    density_gdf_wgs84 = st.session_state['density_gdf_wgs84']

    st.sidebar.header("2. Filter Businesses")
    unique_actividades = ['All'] + gdf_negocios['Clase_actividad'].unique().tolist()
    unique_estratos = ['All'] + gdf_negocios['Estrato'].unique().tolist()

    selected_actividad = st.sidebar.selectbox("Filter by Activity", unique_actividades)
    selected_estrato = st.sidebar.selectbox("Filter by Size (Estrato)", unique_estratos)

    filtered_gdf = filter_businesses(gdf_negocios, selected_actividad, selected_estrato)

    st.subheader("Interactive Geomarketing Map")
    st.write("Explore business density and individual business locations.")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("### Business Map")
        enhanced_map = create_enhanced_map(gdf_negocios, density_gdf_wgs84, filtered_gdf)
        st_map = st_folium(enhanced_map, width=900, height=600)

    with col2:
        st.markdown("### Filtered Businesses Summary")
        if not filtered_gdf.empty:
            st.write(f"Total filtered businesses: {len(filtered_gdf)}")
            st.dataframe(filtered_gdf[['Nombre', 'Clase_actividad', 'Estrato', 'Ubicacion']].head(10))
        else:
            st.info("No businesses match the current filter criteria.")

    st.subheader("Actionable Insights")
    st.markdown("""
    This section provides actionable insights based on the analysis.

    **Market Gap Identification:** Look for lighter colored areas on the density map for potential underserved markets.
    **Competitive Analysis:** Darker areas indicate high competition. Use filters to assess competition for specific business types and sizes.
    **Optimal Location:** Combine density and filtered business views to identify strategic locations for new ventures or expansion.
    """)

    st.markdown("--- ")
    st.markdown("### Comprehensive Actionable Insights Report for MiPymes in Mexico City")
    st.markdown("""
    This geomarketing analysis tool provides a powerful framework for Micro, Small, and Medium-sized Enterprises (MiPymes) in Mexico City to make data-driven decisions regarding their market strategy, expansion, and competitive positioning.

    #### 1. Business Density Analysis: Identifying Market Saturation and Gaps
    The density analysis, visualized through the choropleth map, reveals significant variations in business concentration across the defined search area. A grid-based approach with 200-meter cells was used to quantify this density.

    *   **High-Density Zones (Dark Red Hues):** These areas indicate a high concentration of businesses, suggesting mature or highly competitive markets. MiPymes considering these areas must prepare for aggressive market entry strategies and strong differentiation.
    *   **Low-Density Zones / Potential Market Gaps (Lighter/Uncolored Cells):** These areas represent regions with very few or no businesses. They signify potentially underserved markets or market gaps. Identifying these low-density areas is crucial for MiPymes seeking less competitive locations for expansion or new market entry, offering a higher chance of success.
    *   **Spatial Distribution:** Businesses are not uniformly distributed but tend to cluster in specific commercial corridors or urban centers, highlighting the importance of localized analysis.

    #### 2. Filtering Capabilities: Targeted Market Analysis
    The notebook's filtering capabilities allow for a highly targeted analysis of specific business segments by `Clase_actividad` (business activity) and `Estrato` (business size).

    *   **Niche Market Identification:** By filtering for a specific business type and then examining its distribution on the density map, MiPymes can identify areas with low competition for that niche.
    *   **Assessing Competitive Intensity for Specific Segments:** A MiPyme can filter for its `Clase_actividad` and `Estrato`. High-density zones for this specific filter indicate intense competition.
    *   **Strategic Expansion by Business Size:** The `Estrato` filter is invaluable for understanding competition among businesses of a similar scale.
    """)

    st.markdown("--- ")
    st.markdown("### Enhanced Notebook as a Minimum Viable Product (MVP) for Geomarketing Consulting")
    st.markdown("""
    The enhanced geomarketing analysis notebook represents a robust Minimum Viable Product (MVP) for providing consulting services to Micro, Small, and Medium-sized Enterprises (MiPymes) in Mexico City. Its value lies in its **flexibility**, **data-driven approach**, and ability to generate **actionable insights**.

    #### 1. Flexibility: Customizable and Adaptable Analysis
    The MVP offers significant flexibility through its customizable search parameters. Consultants can easily adapt the analysis to diverse client needs.

    #### 2. Data-Driven Approach: Leveraging INEGI Data for Robust Insights
    The MVP is built upon a solid data-driven foundation, utilizing real-world business data from INEGI. This ensures that the analyses are grounded in current and reliable information.

    #### 3. Actionable Insights: Guiding Strategic Decisions
    The MVP translates complex spatial data into clear, actionable insights that directly support MiPymes' strategic decisions, helping in identifying market gaps, assessing competitive intensity, and optimizing location decisions.
    """)

else:
    st.info("Please run the search and analysis using the sidebar controls.")
