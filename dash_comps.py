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

def circle_graph(p):
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Pie(
                    values = [p, 100-p],
                    hole=0.8,
                    showlegend=False,
                    textinfo='none',
                    title={
                        'text':str(int(p)) + '%',
                        'font': {
                            'size':30
                        }
                    }
                )
            ],
            layout = {
                'margin': {
                    't':20,
                    'b':20,
                    'l':20,
                    'r':20,
                    'pad':20,
                    'autoexpand':True,
                },
                'piecolorway':['#339966', '#cccccc',],
            }
        ),
        style = {
            'height': 300
        }
    )