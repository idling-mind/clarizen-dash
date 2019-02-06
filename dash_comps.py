import dash_core_components as dcc
import dash_daq as daq
import plotly.graph_objs as go
from helper_functions import status_colour

def indicate(status='On Track'):
    return daq.Indicator(
        color=status_colour(status),
        value=True
    )

def progress(p):
    return daq.GraduatedBar(
        value=p/10
    )

def circle_graph(p, status='On Track', size=280, fontsize=30):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(
                    values = [p, 100-p],
                    hole=0.8,
                    showlegend=False,
                    textinfo='none',
                    sort=False,
                    title={
                        'text':str(int(p)) + '%',
                        'font': {
                            'size':fontsize
                        }
                    }
                )
            ],
            layout = {
                'margin': {
                    't':0.05*size,
                    'b':0.05*size,
                    'l':0.05*size,
                    'r':0.05*size,
                    'pad':0.05*size,
                    'autoexpand':True,
                },
                'piecolorway':[status_colour(status), '#cccccc',],
                'width':size,
                'height':size,
            }
        ),
    )