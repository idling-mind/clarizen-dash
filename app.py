import dash
import dash_core_components as dcc
import dash_html_components as html

import clarizen
from dash_comps import indicate, progress, circle_graph
from helper_functions import status_colour

projs = clarizen.get_subprojects("/Project/1nn8h0sy46ic07izfvbk84sm281")
kpis = clarizen.work_items_by_topic("GAI KPI 2019")
tips = clarizen.strategy_tip_list("GAI Strategy Domain")

app = dash.Dash(__name__)

app.layout = html.Div(className='page', children=[
    html.Div(className='container-fluid', children=[
        html.Div(className='page-header', children=[
            html.H3(className='page-title', children='GAI Strategy Matrix 2019'),
        ]),
        html.Div(className='row row-cards', children=[
            html.Div(className='col-lg-2', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children=[
                        html.H3(className='card-title', children='Overall Progress')
                    ]),
                    circle_graph(55),
                ]),
            ]),
            html.Div(className='col-lg-2', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children=[
                        html.H3(className='card-title', children='KPI Progress')
                    ]),
                    circle_graph(65, 'Off Track'),
                ]),
            ]),
            html.Div(className='col-lg-2', children=[
                html.Div(className='card', children=[
                    html.Div(className='card-header', children=[
                        html.H3(className='card-title', children='KPI Progress')
                    ]),
                    circle_graph(1, 'At Risk'),
                ]),
            ]),
        ]),
        html.Div(className='row row-cards row-deck', children=[
            html.Div(className='col-12', children=[
                html.Div(className='card', children=[
                    html.Div(className='table-responsive', children=[
                        html.Table(className='table table-hover table-outline table-vcenter card-table', children=[
                            html.Tr([
                                html.Th(x) for x in ['Name', 'Status', 'Manager', 'Status Text']    
                            ])] +
                            [html.Tr([
                                html.Td(x['Name']),
                                html.Td(indicate(x['TrackStatus']['Name'])),
                                html.Td(x['ProjectManager']['Name']),
                                html.Td(x['InternalStatus'], style={'color':status_colour(x['TrackStatus']['Name'])}),
                            ]) for x in kpis['entities']]
                        ),
                    ])
                ])
            ])
        ]),
        html.Div(className='row row-cards row-deck', children=[
            html.Div(className='col-12', children=[
                html.Div(className='card', children=[
                    html.Div(className='table-responsive', children=[
                        html.Table(className='table table-hover table-outline table-vcenter card-table', children=[
                            html.Tr([
                                html.Th(x) for x in ['Name', 'Status', 'Manager', 'PercentComplete']    
                            ])] +
                            [html.Tr([
                                html.Td(x['Name']),
                                html.Td(indicate(x['TrackStatus']['Name'])),
                                html.Td(x['ProjectManager']['Name']),
                                html.Td(circle_graph(float(x['PercentCompleted']), status=x['TrackStatus']['Name'], size=50, fontsize=15)),
                            ]) for x in projs['entities']]
                        ),
                    ])
                ])
            ])
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
