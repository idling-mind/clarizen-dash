import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq

from helper_functions import status_colour
import plotly.graph_objs as go

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
                    hoverinfo='none',
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

def number_card(n, title, progress=None, pcolor='green'):
    if progress:
        p = html.Div(className='progress progress-sm', children=[
            html.Div(className='progress-bar bg-{}'.format(pcolor), 
                     style={'width': '{}%'.format(progress)},
                     children="")
        ])
    else:
        p = ""
    return html.Div(className='card', children=[
            html.Div(className='card-body text-center', children=[
                html.Div(className='h5', children=title),
                html.Div(className='display-4 font-weight-bold mb-4', children=str(n)),
                p
            ])
        ])

def tip_card(tip, domain):
    try:
        dtotal, dcompleted, dpercent = 0, 0, 0
        for deliverable in tip['Deliverables']:
            dtotal +=1
            if deliverable['State']['Name'] == 'Completed':
                dcompleted +=1
        dpercent = dcompleted/dtotal * 100
    except KeyError:
        pass
    except ZeroDivisionError:
        dpercent = 0
    return html.Div(className='row align-items-center', children=[
        html.Div(className='col-auto', children=[circle_graph(dpercent, size=50, fontsize=12)]),
        html.Div(className='col-auto', children=[indicate(tip['TrackStatus']['Name'])]),
        html.Div(className='col', children=[
            html.B(tip['Name']), 
            html.Small(className='d-block item-except text-sm text-muted', children=[tip['ProjectManager']['Name']]),
            html.Div(children=[
                "{} deliverables of {} completed".format(dcompleted, dtotal),
            ]),
            html.Span(className='badge bg-info', children=[domain]),
        ]),
    ], style={'padding': '10px'})

def tip_deliverable_card(tip):
    """ Card for showing the priority deliverables """
    return html.Div(className='row align-items-center', children=[
        html.Div(className='col', children=[
            html.B(tip['TipName']), 
            html.Small(className='d-block item-except text-sm text-muted', children=[tip['ProjectManager']]),
            html.Div(children=[
                html.Div(className='row align-items-center', children=[
                    html.Div(className='col-auto', children=[indicate(deliverable['Status'])]),
                    html.Div(className='col-auto', children=[
                        deliverable['DeliverableName'],
                        html.Span(className='badge', children=[
                            deliverable['Due']
                            ], style={
                                'background-color':status_colour(deliverable['Status']),
                                'margin-left':'10px'
                                }
                        )
                    ]),
                ], style={'padding': '5px'}) for deliverable in tip['Deliverables']
            ], style={'padding-left':'5px'}),
        ], style={'margin-left': '10px'}),
    ])