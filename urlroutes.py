import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div(className='page', children=[
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url','pathname')])
def ret_page(path):
    if path == "/dashboard":
        return html.Div(className='ticker', children=[
            html.Ul(children=[
                html.Li("ticker 1"),
                html.Li("ticker 2"),
                html.Li("ticker 3"),
                html.Li("ticker 4"),
                html.Li("ticker 5"),
                html.Li("ticker 6"),
                html.Li("ticker 7"),
                html.Li("ticker 8"),
                html.Li("ticker 9"),
                html.Li("ticker 10"),
            ])
        ]),
    else:
        return html.H1("No Dashboard here")

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')