import plotly.express as plty
import pandas as pd
import plotly.graph_objects as oGraph

def main() -> None:
    print('You just extracted from the graph_display module! GZ!')
    
def line_graph(df: pd.DataFrame, weather_parameter: str) -> oGraph.Figure:
    figure = plty.line(df[f'{weather_parameter}'])
    return figure

def bar_graph(df: pd.DataFrame, weather_parameter: str) -> oGraph.Figure:
    figure = plty.bar(df[f'{weather_parameter}'])
    return figure

def make_labels(figure: oGraph.Figure, weather_parameter: str, city: str, unit: str) -> oGraph.Figure:
    figure.update_layout(
        width = 800,
        height = 600,
        title_x = 0.5,
        title = f'Weather for {city}',
        xaxis_title = f'{weather_parameter}',
        yaxis_title = f'{unit}',
        title_font_size = 30,
        showlegend = False
    )
    return figure
    

if __name__ == '__main__':
    main()