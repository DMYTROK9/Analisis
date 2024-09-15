import dash_core_components as dcc

# Define the list of launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create the dropdown component
dcc.Dropdown(
    id='site-dropdown',
    options=[
        {'label': 'All Sites', 'value': 'ALL'}
    ] + [{'label': site, 'value': site} for site in launch_sites],
    value='ALL',  # Default value when loaded
    placeholder="Select a Launch Site here",
    searchable=True
)
[
    {'label': 'All Sites', 'value': 'ALL'},
    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
    
]

# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Sample data from spacex_df (for demonstration purposes, replace with actual data)
spacex_df = pd.DataFrame({
    'Launch Site': ['CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS LC-40', 'VAFB SLC-4E'],
    'class': [1, 0, 1, 1, 0]  # Success (1) or failure (0)
})

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.Graph(id='success-pie-chart')  # This will display the pie chart
])

# Define callback to update the pie chart based on selected site
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # If "ALL" is selected, show the total success vs failure across all sites
    if entered_site == 'ALL':
        # Calculate success and failure counts across all sites
        fig = px.pie(
            data_frame=spacex_df,
            names='class',
            title='Total Success Launches for All Sites',
            hole=.3  # Makes it a donut chart for better visualization
        )
        fig.update_traces(marker=dict(colors=['red', 'green']), 
                          hoverinfo="label+percent", textinfo='value')
        return fig
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Create pie chart for the specific site showing success (1) and failure (0) counts
        fig = px.pie(
            data_frame=filtered_df,
            names='class',
            title=f'Success vs Failure for {entered_site}',
            hole=.3
        )
        fig.update_traces(marker=dict(colors=['red', 'green']), 
                          hoverinfo="label+percent", textinfo='value')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

import dash_core_components as dcc
import dash_html_components as html

# Define min and max payloads for the slider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Layout for the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard'),

    # Dropdown for launch site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),

    # RangeSlider for payload mass selection
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},  # Marks at every 1000 kg
        value=[min_payload, max_payload]  # Initial range set to full payload range
    ),

    dcc.Graph(id='success-payload-scatter-chart')  # This will display a scatter plot
])
marks={0: '0', 1000: '1000', 2000: '2000', ..., 10000: '10000'}

import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Sample data for demonstration (Replace with actual data)
spacex_df = pd.DataFrame({
    'Launch Site': ['CCAFS LC-40', 'VAFB SLC-4E', 'KSC LC-39A', 'CCAFS LC-40', 'VAFB SLC-4E'],
    'Payload Mass (kg)': [5000, 2000, 3000, 4500, 6000],
    'class': [1, 0, 1, 1, 0],
    'Booster Version Category': ['Falcon 9', 'Falcon Heavy', 'Falcon 9', 'Falcon 9', 'Falcon Heavy']
})

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard'),
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: f'{i}' for i in range(0, 10001, 1000)},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),
    dcc.Graph(id='success-payload-scatter-chart')
])

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')
)
def update_scatter_plot(selected_site, payload_range):
    # Filter data based on payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= payload_range[0]) &
        (spacex_df['Payload Mass (kg)'] <= payload_range[1])
    ]
    
    # Further filter data based on selected site
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Success vs. Payload Mass for {selected_site}' if selected_site != 'ALL' else 'Success vs. Payload Mass for All Sites',
        labels={'class': 'Launch Outcome'},
        color_continuous_scale=px.colors.cyclical.IceFire,
        size_max=15
    )
    
    # Update layout for better visualization
    fig.update_layout(
        xaxis_title='Payload Mass (kg)',
        yaxis_title='Launch Outcome',
        legend_title='Booster Version',
        hovermode='closest'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
