import plotly.express as plty
import pandas as pd
import plotly.graph_objects as oGraph
import random
  
def line_graph(df: pd.DataFrame, weather_parameter: str, city: str) -> oGraph.Figure:
    figure = plty.line(df, x='time', y=f'{weather_parameter}', title=f'{city}', labels={'time': 'Time', weather_parameter: f'{weather_parameter}'})
    figure.add_trace(
        oGraph.Scatter(
            x=df['time'], 
            y=df[weather_parameter],
            mode='lines',
            name=f'{weather_parameter.capitalize()} ({city.capitalize()})',
            line=dict(color=_random_color())
        )
    )
    figure.update_layout(showlegend=True)
    return figure

def bar_graph(df: pd.DataFrame, weather_parameter: str, city: str) -> oGraph.Figure:
    figure = plty.bar(df, x='time', y=f'{weather_parameter}',  title=f'{city}', labels={'time': 'Time', weather_parameter: f'{weather_parameter}'})
    figure.add_trace(
        oGraph.Bar(
            x=df['time'], 
            y=df[weather_parameter],
            name=f'{weather_parameter.capitalize()} ({city.capitalize()})',
            marker_color=_random_color()
        )
    )
    figure.update_layout(showlegend=True)
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
        showlegend = True
    )
    return figure

def _random_color():
    colors = ['blue', 'green', 'pink', 'red', 'purple']
    return random.choice(colors)