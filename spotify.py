
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Load and preprocess the data
file_path = 'Top_50.csv'
datos = pd.read_csv(file_path)
datos = datos.drop(columns='Unnamed: 0').dropna(subset=['Country', 'Track Name', 'Artist Name'])

import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# Load and preprocess the data
file_path = 'Top_50.csv'
datos = pd.read_csv(file_path)
datos = datos.drop(columns='Unnamed: 0').dropna(subset=['Country', 'Track Name', 'Artist Name'])

# Replace country abbreviations with full names
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
datos['Country'] = datos['Country'].map(country_mapping)

# Separate "Global" data and clean up dataset
global_data = datos[datos['Country'] == "Global"]
datos = pd.concat([datos, global_data], ignore_index=True)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Music Insights Dashboard"

# Layout
def create_layout():
    return html.Div([
        dbc.Container([
            html.H1("Music Insights Dashboard", className="text-center mb-4", style={"color": "#2c3e50", "fontWeight": "bold"}),

            # Mapa en la parte superior
            dbc.Row([
                dbc.Col(dcc.Graph(id='world-map', style={"height": "65vh", "border": "1px solid #ddd", "borderRadius": "10px"}), width=12),
            ], className="mb-4"),

            # Filtros, detalles y gráfico radial en la misma altura
            dbc.Row([
                # Columna para filtros
                dbc.Col([
                    html.H5("Filters", className="text-center mb-4", style={"color": "#34495e"}),
                    dbc.Accordion([
                        dbc.AccordionItem([
                            dcc.Dropdown(
                                id='country-dropdown',
                                options=[{'label': country, 'value': country} for country in datos['Country'].unique()],
                                placeholder="Select a country",
                                clearable=True,
                                style={"marginBottom": "10px"}
                            ),
                        ], title="Filter by Country"),

                        dbc.AccordionItem([
                            dcc.Dropdown(
                                id='song-dropdown',
                                placeholder="Select a song",
                                clearable=True,
                                style={"marginBottom": "10px"}
                            ),
                        ], title="Filter by Song"),

                        dbc.AccordionItem([
                            dcc.Dropdown(
                                id='artist-dropdown',
                                placeholder="Select an artist",
                                clearable=True,
                                style={"marginBottom": "10px"}
                            ),
                        ], title="Filter by Artist"),
                    ], start_collapsed=True),
                    html.Button("Reset Filters", id='reset-button', n_clicks=0, className="btn btn-primary mt-3"),
                ], width=3),

                # Columna para detalles de canciones y características
                dbc.Col([
                    html.H5("Details for Selected Songs", className="text-center mb-4", style={"color": "#34495e"}),
                    html.Div(id='details', style={
                        "padding": "20px",
                        "backgroundColor": "#ecf0f1",
                        "borderRadius": "10px",
                        "border": "1px solid #ddd",
                        "height": "40vh",
                        "overflowY": "auto",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                    }),
                    html.Div(id='song-characteristics', style={
                        "padding": "20px",
                        "backgroundColor": "#bdc3c7",
                        "borderRadius": "10px",
                        "border": "1px solid #ddd",
                        "height": "20vh",
                        "marginTop": "20px",
                        "overflowY": "auto",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                    })
                ], width=5),

                # Columna para gráfico radial y detalles comparativos
                dbc.Col([
                    html.H5("Song Comparison", className="text-center mb-4", style={"color": "#34495e"}),
                    dcc.Dropdown(
                        id='song1-dropdown',
                        options=[{'label': song, 'value': song} for song in datos['Track Name'].unique()],
                        placeholder="Select first song",
                        style={"marginBottom": "10px"}
                    ),
                    dcc.Dropdown(
                        id='song2-dropdown',
                        options=[{'label': song, 'value': song} for song in datos['Track Name'].unique()],
                        placeholder="Select second song",
                        style={"marginBottom": "10px"}
                    ),
                    dcc.Graph(id='song-comparison-radar', style={"height": "60vh", "border": "1px solid #ddd", "borderRadius": "10px"}),
                    html.Div(id='comparison-details', style={
                        "padding": "20px",
                        "backgroundColor": "#ecf0f1",
                        "borderRadius": "10px",
                        "border": "1px solid #ddd",
                        "marginTop": "20px",
                        "height": "20vh",
                        "overflowY": "auto",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
                    })
                ], width=4),
            ])
        ], fluid=True)
    ])

app.layout = create_layout

@app.callback(
    [Output('world-map', 'figure'),
     Output('country-dropdown', 'value'),
     Output('song-dropdown', 'options'),
     Output('artist-dropdown', 'options'),
     Output('song-characteristics', 'children')],
    [Input('country-dropdown', 'value'),
     Input('song-dropdown', 'value'),
     Input('artist-dropdown', 'value'),
     Input('world-map', 'clickData'),
     Input('reset-button', 'n_clicks')]
)
def update_filters(selected_country, selected_song, selected_artist, click_data, reset_clicks):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'reset-button':
        selected_country = None
        selected_song = None
        selected_artist = None

    elif trigger == 'world-map' and click_data:
        selected_country = click_data['points'][0]['location'] if selected_country != click_data['points'][0]['location'] else None

    filtered_data = datos

    if selected_country:
        if selected_country == "Global":
            filtered_data = global_data
        else:
            filtered_data = datos[datos['Country'] == selected_country]

    if selected_song:
        filtered_data = filtered_data[filtered_data['Track Name'] == selected_song]

    if selected_artist:
        filtered_data = filtered_data[filtered_data['Artist Name'] == selected_artist]

    song_counts = filtered_data.groupby('Country').size().reset_index(name='Song Count')

    fig = px.choropleth(
        song_counts,
        locations='Country',
        locationmode='country names',
        color='Song Count',
        color_continuous_scale='Viridis',
        title="Songs by Country"
    )

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
        ),
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        title_font=dict(size=24, color='#2c3e50', family='Arial'),
        coloraxis_colorbar=dict(title='Songs Count', ticks='outside')
    )

    song_options = [{'label': song, 'value': song} for song in filtered_data['Track Name'].unique()]
    artist_options = [{'label': artist, 'value': artist} for artist in filtered_data['Artist Name'].unique()]

    # Update song characteristics if a song is selected
    characteristics = ""
    if selected_song:
        song_data = datos[datos['Track Name'] == selected_song].iloc[0]
        characteristics = html.Div([
            html.H6(f"Characteristics for {song_data['Track Name']} by {song_data['Artist Name']}", className="text-primary"),
            html.Ul([
                html.Li(f"Danceability: {song_data['Danceability']:.2f}"),
                html.Li(f"Energy: {song_data['Energy']:.2f}"),
                html.Li(f"Speechiness: {song_data['Speechiness']:.2f}"),
                html.Li(f"Acousticness: {song_data['Acousticness']:.2f}"),
                html.Li(f"Liveness: {song_data['Liveness']:.2f}"),
                html.Li(f"Positiveness: {song_data['Positiveness']:.2f}")
            ])
        ])

    return fig, selected_country, song_options, artist_options, characteristics

@app.callback(
    [Output('song-comparison-radar', 'figure'),
     Output('comparison-details', 'children')],
    [Input('song1-dropdown', 'value'),
     Input('song2-dropdown', 'value')]
)
def compare_songs(song1, song2):
    if not song1 or not song2:
        return go.Figure(), "Select two songs to see their characteristics."

    # Obtener datos de las canciones seleccionadas
    song1_data = datos[datos['Track Name'] == song1].iloc[0]
    song2_data = datos[datos['Track Name'] == song2].iloc[0]

    # Atributos a comparar
    attributes = ['Danceability', 'Acousticness', 'Energy', 'Liveness', 'Speechiness', 'Positiveness']

    # Crear datos para el gráfico radar
    song1_values = [song1_data[attr] for attr in attributes]
    song2_values = [song2_data[attr] for attr in attributes]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=song1_values + [song1_values[0]],
        theta=attributes + [attributes[0]],
        fill='toself',
        name=song1_data['Track Name'],
        line=dict(color='#3498db')
    ))

    fig.add_trace(go.Scatterpolar(
        r=song2_values + [song2_values[0]],
        theta=attributes + [attributes[0]],
        fill='toself',
        name=song2_data['Track Name'],
        line=dict(color='#e74c3c')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], gridcolor='#bdc3c7')
        ),
        showlegend=True,
        title=dict(text="Comparison of Song Characteristics", x=0.5, font=dict(size=20, color='#2c3e50')),
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5, bgcolor='#ecf0f1', bordercolor='#ddd', borderwidth=1)
    )

    # Detalles comparados
    comparison_details = html.Div([
        html.H6("Comparison Details", className="text-primary"),
        html.Ul([
            html.Li(f"{song1_data['Track Name']} - Danceability: {song1_data['Danceability']:.2f} vs {song2_data['Danceability']:.2f}"),
            html.Li(f"{song1_data['Track Name']} - Energy: {song1_data['Energy']:.2f} vs {song2_data['Energy']:.2f}"),
            html.Li(f"{song1_data['Track Name']} - Acousticness: {song1_data['Acousticness']:.2f} vs {song2_data['Acousticness']:.2f}"),
            html.Li(f"{song1_data['Track Name']} - Speechiness: {song1_data['Speechiness']:.2f} vs {song2_data['Speechiness']:.2f}"),
            html.Li(f"{song1_data['Track Name']} - Liveness: {song1_data['Liveness']:.2f} vs {song2_data['Liveness']:.2f}"),
            html.Li(f"{song1_data['Track Name']} - Positiveness: {song1_data['Positiveness']:.2f} vs {song2_data['Positiveness']:.2f}"),
        ])
    ])

    return fig, comparison_details

@app.callback(
    Output('details', 'children'),
    [Input('song-dropdown', 'value'),
     Input('artist-dropdown', 'value')]
)
def update_details(selected_song, selected_artist):
    if selected_song:
        # Filtros por canción seleccionada
        filtered_data = datos[datos['Track Name'] == selected_song]
    elif selected_artist:
        # Filtros por artista seleccionado
        filtered_data = datos[datos['Artist Name'] == selected_artist]
    else:
        return "No song or artist selected."

    if not filtered_data.empty:
        song_details = filtered_data.iloc[0].to_dict()
        details = html.Div([
            html.H6(f"Details for '{song_details['Track Name']}' by {song_details['Artist Name']}", className="text-primary"),
            html.Ul([
                html.Li(f"Album: {song_details['Album Name']}"),
                html.Li(f"Popularity: {song_details['Popularity']}"),
                html.Li(f"Date: {song_details['Date']}"),
                html.Li(f"Duration: {song_details['duration']} ms"),
                html.Li(f"Tempo: {song_details['Tempo']} BPM")
            ])
        ])
        return details

    return "No details available."


# Función para abrir el navegador automáticamente
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")
server = app.server
# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8080)
