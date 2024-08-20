import plotly.express as plty
import pandas as pd
import plotly.graph_objects as oGraph
  
def line_graph(df: pd.DataFrame, weather_parameter: str) -> oGraph.Figure:
    figure = plty.line(df[f'{weather_parameter}'])
    return figure

def bar_graph(df: pd.DataFrame, weather_parameter: str) -> oGraph.Figure:
    figure = plty.bar(df[f'{weather_parameter}'])
    return figure

def make_labels(figure: oGraph.Figure, weather_parameter: str, city: str, unit: str, date: str) -> oGraph.Figure:
    figure.update_layout(
        width = 800,
        height = 600,
        title_x = 0.5,
        title = f'Weather for {city.capitalize()}: {date}',
        xaxis_title = f'{weather_parameter}',
        yaxis_title = f'{unit}',
        title_font_size = 30,
        showlegend = False
    )
    return figure