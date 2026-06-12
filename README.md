# Geomarketing Analysis MVP for MiPymes in Mexico City

![Project Banner](https://via.placeholder.com/1200x400?text=Geomarketing+Analysis+Banner) <!-- Replace with an actual project banner/screenshot -->

## Table of Contents
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Deployment](#deployment)
- [How to Run Locally](#how-to-run-locally)
- [Usage](#usage)
- [Actionable Insights](#actionable-insights)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)
- [License](#license)

## Project Overview
This project presents a Minimum Viable Product (MVP) of a geomarketing analysis tool specifically designed for Micro, Small, and Medium-sized Enterprises (MiPymes) in Mexico City. Leveraging official INEGI (Instituto Nacional de Estadística y Geografía) business data, this Streamlit application empowers businesses to make data-driven decisions for market strategy, expansion, and competitive positioning.

The interactive web application allows users to search for specific business types within a defined radius, visualize business density, and filter results based on activity and size. It provides a powerful framework for identifying market saturation, uncovering underserved areas, and understanding competitive landscapes.

## Problem Statement
MiPymes often lack the resources and expertise to conduct comprehensive market research. This can lead to suboptimal decisions regarding business location, expansion, and competitive strategy. Traditional market analysis can be costly and time-consuming, creating a significant barrier for smaller businesses aiming for growth and sustainable development.

This tool addresses these challenges by providing an accessible, interactive, and data-driven solution to visualize and analyze local business ecosystems.

## Features
-   **Customizable Search Parameters**: Define business type, central latitude/longitude, and search radius.
-   **Interactive Business Density Map**: Visualize the concentration of businesses using a choropleth map, highlighting areas of high competition and potential market gaps.
-   **Individual Business Locations**: Display specific business locations with detailed information via interactive markers.
-   **Dynamic Filtering**: Filter businesses by `Clase_actividad` (business activity) and `Estrato` (business size) to refine market analysis.
-   **Actionable Insights Report**: Provides a summary of insights derived from the analysis, guiding strategic decision-making.
-   **User-Friendly Interface**: Built with Streamlit for an intuitive and interactive user experience.

## Technologies Used
-   **Python**: Core programming language.
-   **Streamlit**: For creating interactive web applications.
-   **GeoPandas**: For handling geospatial data (GeoDataFrames).
-   **Folium**: For creating interactive maps and visualizations.
-   **Shapely**: For geometric operations.
-   **NumPy**: For numerical operations.
-   **Pandas**: For data manipulation and analysis.
-   **Requests**: For consuming the INEGI DENUE API.

## Deployment
This application is deployed on Streamlit Community Cloud for easy access. You can view the live application here:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_app_badge.svg)](https://geomarketinganalysis.streamlit.app/) <!-- Replace YOUR_STREAMLIT_APP_URL with your actual Streamlit deployment URL -->

**API Key Management**: The INEGI API token is securely managed using Streamlit's `st.secrets` feature, ensuring that sensitive credentials are not exposed in the codebase.

## How to Run Locally
To run this project on your local machine, follow these steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/Geomarketing-Analysis-.git
    cd Geomarketing-Analysis-
    ```

2.  **Create a virtual environment (recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your INEGI API Token**:
    Create a directory named `.streamlit` in the root of your project, and inside it, create a file named `secrets.toml`. Add your INEGI API token to this file:
    ```toml
    # .streamlit/secrets.toml
    TOKEN = "YOUR_INEGI_API_TOKEN"
    ```
    Replace `"YOUR_INEGI_API_TOKEN"` with your actual token.

5.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```
    The application will open in your default web browser.

## Usage
1.  **Customize Search Parameters**: Use the sidebar to enter the desired business type (e.g., "cafeterias", "restaurantes"), latitude, longitude, and search radius in meters.
2.  **Run Search and Analysis**: Click the "Run Search and Analysis" button to fetch data and generate the maps.
3.  **Filter Businesses**: After the initial search, use the second section in the sidebar to filter businesses by 'Activity' and 'Size (Estrato)'.
4.  **Explore Maps**: Interact with the map on the main screen to zoom, pan, and toggle layers (e.g., business density, all businesses, filtered businesses).
5.  **Review Insights**: Read the "Actionable Insights" section for interpretations and recommendations based on the displayed data.

## Actionable Insights
This tool provides valuable insights for MiPymes:
-   **Market Gap Identification**: Lighter areas on the density map indicate potential underserved markets, ideal for new ventures.
-   **Competitive Analysis**: Darker areas signify high competition, prompting strategies for differentiation.
-   **Optimal Location**: Combine density and filtered views to pinpoint strategic locations for new establishments or expansions.
-   **Niche Market Identification**: Filter by specific activities to find areas with less competition for specialized businesses.

## Future Enhancements
-   **Time-Series Analysis**: Incorporate historical data (if available) to analyze trends and seasonality.
-   **Predictive Modeling**: Implement models for sales forecasting or optimal location prediction.
-   **Integration with Other Data Sources**: Include demographic data, consumer spending patterns, or foot traffic data.
-   **Advanced Filtering**: Add more sophisticated filtering options, such as proximity to landmarks or transportation.
-   **User Accounts and Saved Searches**: Allow users to save their search configurations and results.
-   **Performance Optimization**: Optimize geospatial operations for larger datasets.

## Contact
If you have any questions or feedback, feel free to reach out:
-   **Your Name/Alias**: [JMFU]
-   **LinkedIn**: [https://www.linkedin.com/in/jmartinfu/]
-   **Email**: [jmartinfu@outlook.es]

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
