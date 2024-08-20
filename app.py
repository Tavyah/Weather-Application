from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as oGraph
import graph_display
import units_met
import dataframe_handler as df_handler

def main():
    app = Dash(__name__)

    app_layout(app)
    @app.callback(
        Output(component_id='graph-plotly', component_property='figure'),
        [Input(component_id='dropdown', component_property='value'),
        Input(component_id='checklist_plot', component_property='value'),
        Input(component_id='checklist_api', component_property='value')]
    )
    def update_graph(dropdownValue, checklistValue, api_list):
        figure = oGraph.Figure()
        
        if 'MET' in api_list: 
            df = df_handler.get_dataframe('MET')
            if 'bar' in checklistValue:
                figure_bar = graph_display.bar_graph(df, dropdownValue)
                figure.add_traces(figure_bar.data)
                
            if 'line' in checklistValue:
                figure_line = graph_display.line_graph(df, dropdownValue)
                figure.add_traces(figure_line.data)
            
            figure = graph_display.make_labels(figure, dropdownValue, df_handler.get_name(api_list), units_met.unit(dropdownValue), df_handler.get_date(api_list))

        if 'SMHI' in api_list:
            df = df_handler.get_dataframe('SMHI')
            if 'bar' in checklistValue:
                figure_bar = graph_display.bar_graph(df, dropdownValue)
                figure.add_traces(figure_bar.data)
                
            if 'line' in checklistValue:
                figure_line = graph_display.line_graph(df, dropdownValue)
                figure.add_traces(figure_line.data)
            
            figure = graph_display.make_labels(figure, dropdownValue, df_handler.get_name(api_list), units_met.unit(dropdownValue), df_handler.get_date(api_list))

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
        dcc.Graph(id='graph-plotly')
    ])
    return init_layout

if __name__ == '__main__':
    main()