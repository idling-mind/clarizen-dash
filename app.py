import dash
import dash_core_components as dcc
import dash_html_components as html

import clarizen

projs = clarizen.get_subprojects("/Project/1nn8h0sy46ic07izfvbk84sm281")

ext_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=ext_css)

app.layout = html.Div(children=[
    html.H1(children='GAI Strategy Matrix 2019'),   
    html.Table( 
        [html.Tr([
            html.Th(x) for x in ['Name', 'Status', 'Manager', 'PercentComplete']    
        ])] +
        [html.Tr([
            html.Td(x['Name']),
            html.Td(x['TrackStatus']['Name']),
            html.Td(x['ProjectManager']['Name']),
            html.Td(x['PercentCompleted']),
        ]) for x in projs['entities']]
    )
    ])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
