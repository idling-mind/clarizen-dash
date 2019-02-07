import dash
import dash_core_components as dcc
import dash_html_components as html

def number_card(n, title, progress=None, pcolor='green'):
    if progress:
        p = html.Div(className='progress progress-sm', children=[
            html.Div(className='progress-bar bg-{}'.format(pcolor), 
                     style={'width': '{}%'.format(progress)},
                     children="")
        ])
    else:
        p = ""
    return html.Div(className='col-lg-2 col-sm-4', children=[
        html.Div(className='card', children=[
            html.Div(className='card-body text-center', children=[
                html.Div(className='h5', children=title),
                html.Div(className='display-4 font-weight-bold mb-4', children=str(n)),
                p
            ])
        ])
    ])