import dash
import dash_core_components as dcc
import dash_html_components as html

import clarizen
from dash_comps import indicate, progress, progress_status, circle_graph

projs = clarizen.get_subprojects("/Project/1nn8h0sy46ic07izfvbk84sm281")

ext_css = ['https://raw.githubusercontent.com/tabler/tabler/dev/dist/assets/css/dashboard.css']
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div(className='page', children=[
    html.Div(className='container-fluid', children=[
        html.Div(className='page-header', children=[
            html.H3(className='page-title', children='GAI Strategy Matrix 2019'),
        ]),
        html.Div(className='row row-cards', children=[
            html.Div(className='col-lg-2', children=[
                html.Div(className='card', children=[
                    circle_graph(55, 'Overall Progress'),
                ]),
            ]),
            html.Div(className='col-lg-2', children=[
                html.Div(className='card', children=[
                    circle_graph(65, 'KPI Progress'),
                ]),
            ]),
            html.Table( 
                [html.Tr([
                    html.Th(x) for x in ['Name', 'Status', 'Manager', 'PercentComplete']    
                ])] +
                [html.Tr([
                    html.Td(x['Name']),
                    html.Td(indicate(x['TrackStatus']['Name'])),
                    html.Td(x['ProjectManager']['Name']),
                    html.Td(progress(x['PercentCompleted'])),
                ]) for x in projs['entities']]
            ),
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
