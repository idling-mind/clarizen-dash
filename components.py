import dash
import dash_core_components as dcc
import dash_html_components as html

from dash_comps import circle_graph, indicate

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
            html.Span(className='badge badge-default', children=[domain]),
        ]),
    ], style={'padding': '10px'})