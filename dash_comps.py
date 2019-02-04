import dash_core_components as dcc
import dash_daq as daq
import plotly.graph_objs as go

def indicate(status='On Track'):
    c = "#00CC96",
    if status == 'On Track':
        c = "#00CC96",
    elif status == 'At Risk':
        c = "#FDB507",
    elif status == 'Off Track':
        c = "#FD3A07"
    return daq.Indicator(
        color=c,
        value=True
    )

def progress(p):
    return daq.GraduatedBar(
        value=p/10
    )

def progress_status(status='On Track', p=0):
    c = "#00CC96",
    if status == 'On Track':
        c = "#00CC96",
    elif status == 'At Risk':
        c = "#FDB507",
    elif status == 'Off Track':
        c = "#FD3A07"
    
    return daq.GraduatedBar(
        max=100,
        value=p,
        color=c
    )

def circle_graph(p):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(
                    values = [p, 100-p],
                    hole=0.8,
                    showlegend=False
                )
            ],
            layout = {
                'margin': {
                    't':10,
                    'b':10,
                    'l':10,
                    'r':10,
                    'pad':10,
                    'autoexpand':True,
                }
            }
        ),
        style = {
            'height': 500
        }
    )