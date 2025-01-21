import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# Cargar datos
file_path = 'Top_50.csv'
spotify_data = pd.read_csv(file_path).dropna(subset=['Country', 'Track Name', 'Artist Name'])

# Reemplazar abreviaciones de países
country_mapping = {
    "Global": "Global",
    "DEU": "Germany",
    "SAU": "Saudi Arabia",
    "ARG": "Argentina",
    "AUS": "Australia",
    "AUT": "Austria",
    "BLR": "Belarus",
    "BRA": "Brazil",
    "BGR": "Bulgaria",
    "BEL": "Belgium",
    "CAN": "Canada",
    "CHL": "Chile",
    "COL": "Colombia",
    "KOR": "South Korea",
    "CRI": "Costa Rica",
    "DNK": "Denmark",
    "ARE": "United Arab Emirates",
    "ECU": "Ecuador",
    "EGY": "Egypt",
    "SLV": "El Salvador",
    "SVK": "Slovakia",
    "ESP": "Spain",
    "USA": "United States",
    "EST": "Estonia",
    "PHL": "Philippines",
    "FIN": "Finland",
    "FRA": "France",
    "GRC": "Greece",
    "GTM": "Guatemala",
    "HND": "Honduras",
    "HKG": "Hong Kong",
    "HUN": "Hungary",
    "IND": "India",
    "IDN": "Indonesia",
    "IRL": "Ireland",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "CZE": "Czech Republic",
    "DOM": "Dominican Republic",
    "LVA": "Latvia",
    "LTU": "Lithuania",
    "NLD": "Netherlands",
    "LUX": "Luxembourg",
    "MYS": "Malaysia",
    "MAR": "Morocco",
    "MEX": "Mexico",
    "NIC": "Nicaragua",
    "NGA": "Nigeria",
    "NOR": "Norway",
    "NZL": "New Zealand",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PRY": "Paraguay",
    "PER": "Peru",
    "POL": "Poland",
    "PRT": "Portugal",
    "GBR": "United Kingdom",
    "ROU": "Romania",
    "SGP": "Singapore",
    "ZAF": "South Africa",
    "SWE": "Sweden",
    "CHE": "Switzerland",
    "THA": "Thailand",
    "TWN": "Taiwan",
    "TUR": "Turkey",
    "UKR": "Ukraine",
    "URY": "Uruguay",
    "VEN": "Venezuela",
    "VNM": "Vietnam"
}
spotify_data['Country'] = spotify_data['Country'].map(country_mapping)

# Escalador y modelo KNN
features = ['Danceability', 'Energy', 'Tempo', 'Positiveness', 'Acousticness', 
            'Liveness', 'Speechiness', 'Instrumentalness', 'Loudness']
scaler = StandardScaler()
normalized_features = scaler.fit_transform(spotify_data[features])
knn = NearestNeighbors(n_neighbors=6, metric='euclidean')
knn.fit(normalized_features)

# Función para recomendaciones
def recommend_songs(track_names, n_neighbors=5):
    selected_indices = spotify_data[spotify_data['Track Name'].isin(track_names)].index
    recommended_indices = set()
    for idx in selected_indices:
        distances, indices = knn.kneighbors([normalized_features[idx]], n_neighbors=n_neighbors + 1)
        recommended_indices.update(indices[0][1:])
    playlist = spotify_data.iloc[list(recommended_indices)][['Track Name', 'Artist Name', 'Country']]
    return playlist

# Título de la aplicación
st.title("Dashboard de Canciones y Recomendaciones")

# Panel de navegación
st.sidebar.title("Navegación")
selected_tab = st.sidebar.radio("Seleccione una pestaña:", ["🌍 Mapa Interactivo", "📊 Comparación de Canciones", "🎧 Recomendador de Canciones"])

if selected_tab == "🌍 Mapa Interactivo":
    st.header("Mapa Interactivo de Canciones 🎶")

    # Mantener estado de filtro en sesión
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = ''
    if 'selected_artist' not in st.session_state:
        st.session_state.selected_artist = ''
    if 'selected_song' not in st.session_state:
        st.session_state.selected_song = ''

    # Botón para reiniciar filtros
    if st.button("🔄 Reiniciar Filtros"):
        st.session_state.selected_country = ''
        st.session_state.selected_artist = ''
        st.session_state.selected_song = ''

    # Filtrar dinámicamente los datos
    filtered_data = spotify_data

    # Opciones para los filtros
    available_countries = [''] + spotify_data['Country'].dropna().unique().tolist()
    country = st.selectbox("Seleccione un país:", available_countries, index=available_countries.index(st.session_state.selected_country) if st.session_state.selected_country in available_countries else 0)
    if country:
        st.session_state.selected_country = country
        filtered_data = filtered_data[filtered_data['Country'] == country]

    available_artists = [''] + filtered_data['Artist Name'].dropna().unique().tolist()
    artist = st.selectbox("Seleccione un artista:", available_artists, index=available_artists.index(st.session_state.selected_artist) if st.session_state.selected_artist in available_artists else 0)
    if artist:
        st.session_state.selected_artist = artist
        filtered_data = filtered_data[filtered_data['Artist Name'] == artist]

    available_songs = [''] + filtered_data['Track Name'].dropna().unique().tolist()
    song = st.selectbox("Seleccione una canción:", available_songs, index=available_songs.index(st.session_state.selected_song) if st.session_state.selected_song in available_songs else 0)
    if song:
        st.session_state.selected_song = song
        filtered_data = filtered_data[filtered_data['Track Name'] == song]

    # Crear mapa interactivo dinámico
    filtered_counts = filtered_data.groupby('Country').size().reset_index(name='Song Count')

    fig = px.choropleth(
        filtered_counts,
        locations='Country',
        locationmode='country names',
        color='Song Count',
        color_continuous_scale='Viridis',
        title="Popularidad por País",
        labels={'Song Count': 'Canciones'}
    )
    fig.update_geos(
        showcoastlines=True, coastlinecolor="LightGray",
        showland=True, landcolor="#f9f9f9",
        showcountries=True, countrycolor="Gray"
    )
    fig.update_layout(
        title_font_size=24,
        geo=dict(bgcolor='rgba(255,255,255,0)'),
        margin={"r":0,"t":40,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

    # Mostrar características de la canción seleccionada
    if song:
        st.subheader(f"🎤  Características de la canción: {song}")
        song_features = filtered_data[filtered_data['Track Name'] == song][features].iloc[0]
        st.write(song_features)

elif selected_tab == "📊 Comparación de Canciones":
    st.header("Comparación de Canciones 🎼")

    song1 = st.selectbox("🎵 Seleccione la primera canción:", [''] + spotify_data['Track Name'].unique().tolist())
    song2 = st.selectbox("🎵 Seleccione la segunda canción:", [''] + spotify_data['Track Name'].unique().tolist())
    if song1 and song2:
        song1_data = spotify_data[spotify_data['Track Name'] == song1].iloc[0]
        song2_data = spotify_data[spotify_data['Track Name'] == song2].iloc[0]

        attributes = ['Danceability', 'Energy', 'Tempo', 'Positiveness', 'Acousticness', 
                      'Liveness', 'Speechiness', 'Instrumentalness', 'Loudness']
        song1_values = [song1_data[attr] for attr in attributes]
        song2_values = [song2_data[attr] for attr in attributes]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=song1_values + [song1_values[0]], theta=attributes + [attributes[0]], fill='toself', line=dict(color='blue'), name=song1))
        fig.add_trace(go.Scatterpolar(r=song2_values + [song2_values[0]], theta=attributes + [attributes[0]], fill='toself', line=dict(color='red'), name=song2))

        fig.update_layout(title="Comparación de características de canciones", polar=dict(radialaxis=dict(visible=True, range=[0, 1])))
        st.plotly_chart(fig)

elif selected_tab == "🎧 Recomendador de Canciones":
    st.header("Recomendador de Canciones 🎧")

    selected_songs = st.multiselect("🎵 Seleccione una o varias canciones para obtener recomendaciones:", [''] + spotify_data['Track Name'].unique().tolist())

    if selected_songs:
        recommendations = recommend_songs(selected_songs)
        st.write(f"🎶 Canciones recomendadas basadas en {', '.join(selected_songs)}:")
        st.dataframe(recommendations)