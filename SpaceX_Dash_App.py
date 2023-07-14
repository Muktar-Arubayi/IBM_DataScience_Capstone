import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),
        html.Div(
            [
                html.Label('Launch Site'),
                dcc.Dropdown(
                    id='site-dropdown',
                    options=[
                        {'label': 'All Sites', 'value': 'ALL'},
                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                    ],
                    value='ALL',
                    placeholder='Select a Launch Site',
                    searchable=True
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id='success-pie-chart')
            ]
        ),
        html.Br(),
        html.Div(
            [
                html.P("Payload Range (kg):"),
                dcc.RangeSlider(
                    id='payload-slider',
                    min=min_payload,
                    max=max_payload,
                    step=1000,
                    value=[min_payload, max_payload]
                )
            ]
        ),
        html.Br(),
        html.Div(
            [
                dcc.Graph(id='success-payload-scatter-chart')
            ]
        )
    ]
)

# Callback function for success-pie-chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            names='Launch Site',
            title='Success Rate by Launch Site'
        )
        return fig
    else:
        site_filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(
            site_filtered_df,
            names='class',
            title=f'Success Rate for {entered_site}'
        )
        return fig

# Callback function for success-payload-scatter-chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    if selected_site == 'ALL':
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
            (spacex_df['Payload Mass (kg)'] <= payload_range[1])
        ]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Payload vs. Launch Outcome (All Sites)'
        )
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(
            filtered_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Payload vs. Launch Outcome at {selected_site}'
        )

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()