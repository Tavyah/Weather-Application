from dash import Dash, dcc, html, Input, Output
import os
import pandas as pd
import plotly.graph_objects as oGraph
import graph_display
import units_met

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data_folder = '/data/'
    filename = '/oslo_met.csv'
    filepath = current_dir + data_folder + filename

    df = pd.read_csv(filepath)
    app = Dash(__name__)

    app_layout(app)
    @app.callback(
        Output(component_id='graph-plty', component_property='figure'),
        [Input(component_id='dropdown', component_property='value'),
        Input(component_id='checklist_plot', component_property='value'),
        Input(component_id='checklist_api', component_property='value')]
    )
    def update_graph(dropdownValue, checklistValue, api):
        figure = oGraph.Figure()
        
        if 'bar' in checklistValue:
            figure_bar = graph_display.bar_graph(df, dropdownValue)
            figure.add_traces(figure_bar.data)
            
        if 'line' in checklistValue:
            figure_line = graph_display.line_graph(df, dropdownValue)
            figure.add_traces(figure_line.data)
        
        figure = graph_display.make_labels(figure, dropdownValue, name_strip(filename), units_met.unit(dropdownValue))

        return figure
    
    app.run_server(debug = True, use_reloader = True) 

def app_layout(app):
    app.layout = html.Div(init_app())

def init_app():
    init_layout = []

    init_layout = html.Div([
        dcc.Dropdown(id='dropdown', options= [
            {'label': 'air_temperature', 'value': 'air_temperature'},
            {'label': 'air_pressure_at_sea_level', 'value': 'air_pressure_at_sea_level'},
            {'label': 'cloud_area_fraction', 'value': 'cloud_area_fraction'},
            {'label': 'relative_humidity', 'value': 'relative_humidity'},
            {'label': 'wind_from_direction', 'value': 'wind_from_direction'},
            {'label': 'wind_speed', 'value': 'wind_speed'},
            {'label': 'next_1_hours_precipitation_amount', 'value': 'next_1_hours_precipitation_amount'},
        ], value = 'air_temperature'),
        dcc.Checklist(id = 'checklist_plot', options = [
            {'label': 'Line plot', 'value': 'line'},
            {'label': 'Bar plot', 'value': 'bar'}
        ], value = ['line']),
        dcc.Checklist(id='checklist_api', options= [
            {'label': 'Meteorologisk institutt', 'value': 'MET'},
            {'label': 'Sveriges meteorologiska och hydrologiska institut','value': 'SMHI'}
        ], value = ['MET']),
        dcc.Graph(id='graph-plty')
    ])
    return init_layout

def name_strip(filename: str) -> str:
    split_name, _ = filename.split('_')
    stripped_name = split_name.strip('/')
    return stripped_name

if __name__ == '__main__':
    main()