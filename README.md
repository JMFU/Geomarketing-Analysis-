# Geomarketing Analysis MVP for MiPymes in Mexico City

Overview: This project presents a Minimum Viable Product (MVP) for a geomarketing analysis tool designed to empower Micro, Small, and Medium-sized Enterprises (MiPymes) in Mexico City. Leveraging real-world business data from Mexico's National Institute of Statistics and Geography (INEGI), this interactive application provides data-driven insights for strategic decision-making in market entry, competitive analysis, and location optimization.

Key Features:

Dynamic Data Retrieval: Utilizes the INEGI DENUE API to fetch up-to-date business establishment data based on customizable search parameters (business type, location, radius).
Spatial Density Analysis: Implements a grid-based spatial aggregation technique (using geopandas and shapely) to visualize business concentration via choropleth maps, helping identify high-competition areas and potential market gaps.
Interactive Mapping: Integrates folium and streamlit-folium to create interactive maps, allowing users to explore overall business distribution, density layers, and individual establishment details.
Advanced Filtering: Enables granular analysis through filters for Clase_actividad (business activity) and Estrato (business size), facilitating targeted competitive intelligence.
Actionable Insights Generation: Provides clear, comprehensive insights on market saturation, competitive intensity, and optimal location strategies, derived directly from the spatial analysis.
Streamlit Application: Packaged as an intuitive web application using Streamlit, making complex geospatial analysis accessible to non-technical users.
Technical Stack:

Python: Core programming language.
Libraries: pandas, numpy, requests, geopandas, shapely, folium, streamlit, streamlit-folium, pyngrok (for deployment).
APIs: INEGI DENUE API.
Geospatial Tools: EPSG:4326 (WGS84) and EPSG:6372 (Mexico City projected CRS) for accurate calculations.
Deployment: ngrok for exposing the Streamlit app temporarily.
Why this matters for MiPymes: In a competitive urban landscape like Mexico City, intelligent location and market understanding are paramount. This tool provides MiPymes with a cost-effective, powerful solution to:

Identify underserved areas for expansion.
Understand competitive landscapes for specific business types.
Optimize site selection for new ventures.
Develop targeted marketing strategies.
Future Enhancements:

Integration of additional demographic and socioeconomic data.
Predictive modeling for market demand.
User authentication and persistent data storage.
Enhanced UI/UX features.
