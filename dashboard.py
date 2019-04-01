#!/home/yy53393/.conda/envs/dash/bin/python
import os
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_caching import Cache

import clarizen
from dash_comps import indicate, progress, circle_graph
from helper_functions import status_colour
from components import number_card, tip_card, tip_deliverable_card

app = dash.Dash(__name__)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

TIMEOUT = 3600

@cache.memoize(timeout=TIMEOUT)
def tips_data():
    projs = clarizen.work_items_by_topic("GAI Strategy Domain")
    print("Extracted Domains")
    kpis = clarizen.work_items_by_topic("GAI KPI 2019")
    mkpis = clarizen.work_items_by_topic("GAI Manager KPI 2019")
    print("Extracted KPIs")
    tips = clarizen.strategy_tip_list("GAI Strategy Domain")
    print("Extracted TIPs")
    prio_tips = clarizen.prio_tips(tips)
    print("Extracted priority deliverables")
    tipcount = clarizen.tip_count(tips)
    dtotal, dcompleted = clarizen.delivery_count(tips)
    return {
        'projs': projs,
        'kpis': kpis,
        'mkpis': mkpis,
        'tips': tips, 
        'prio_tips': prio_tips,
        'tipcount': tipcount,
        'dtotal': dtotal,
        'dcompleted': dcompleted,
    }

def dash_main():
    return html.Div(className='page', children=[
        html.Div(style={'margin':'10px'}, children=[ 
            html.Div(className='container-fluid', children=[
                html.Div(className='d-flex', children=[ 
                    html.H3(className='page-title', children='GAI Strategy Matrix 2019'),
                    html.Div(className='d-flex order-lg-2 ml-auto', children=[
                        html.Small(className='d-block item-except text-sm text-muted', children=[
                            "Last Updated: {}".format(
                                datetime.now().replace(microsecond=0).isoformat(' ')
                            )
                        ]),
                    ]),
                ]),
            ]),
        ]),
        html.Div(className='container-fluid', children=[ 
            html.Div(className='row row-cards', children=[ 
                html.Div(className='col-6', children=[ 
                    html.Div(className='row', children=[
                        html.Div(className='col-lg-4', children=[
                            number_card(tips_data()['tipcount'], "Number of TIPs"),
                        ]),
                        html.Div(className='col-lg-4', children=[
                            number_card(tips_data()['dtotal'], "Number of Deliverables"),
                        ]),
                        html.Div(className='col-lg-4', children=[
                            number_card(tips_data()['dcompleted'], "Completed Deliverables", progress=tips_data()['dcompleted']/tips_data()['dtotal']*100),
                        ]),
                        html.Div(className='col-12', children=[
                            html.Div(className='card', children=[
                                html.Div(className='card-header', children=[html.H3(className='card-title', children=[html.B('TIP List')])]),
                                html.Div(className='ticker', children=[
                                    html.Ul(className='list-unstyled list-separated', children=[
                                        html.Li(className='list-separated-item', children=[tip_card(tip, domain['Name'])]) for domain in tips_data()['tips']['entities'] for tip in domain['subprojects']
                                    ])
                                ]), 
                            ]),
                        ]),
                    ]),
                ]),
                html.Div(className='col-6', children=[ 
                    html.Div(className='row', children=[
                        html.Div(className='col-lg-4', children=[
                            html.Div(className='card', children=[
                                html.Div(className='card-header', children=[
                                    html.H3(className='card-title', children=domain['Name'])
                                ]),
                                circle_graph(float(domain['PercentCompleted']),status=domain['TrackStatus']['Name']),
                            ]),
                        ]) for domain in tips_data()['projs']['entities']
                    ] + [
                        html.Div(className='col-lg-12', children=[
                            html.Div(className='card', children=[
                                html.Div(className='card-header', children=html.B("Priority Deliverables (Overdue or Due in next 30 days)")),
                                html.Ul(className='list-unstyled list-separated', children=[
                                    html.Li(className='list-separated-item', children=[tip_deliverable_card(x)]) for x in tips_data()['prio_tips']
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ])

app.layout = html.Div(children=[
    html.Div(id='main', children=[
        dash_main()
    ]),
    dcc.Interval(
        id='interval_comp',
        interval=1*1000*60*60,
        n_intervals=0
    ),
])

@app.callback(Output('main','children'),
              [Input('interval_comp', 'n_intervals')])
def update_ticker(n):
    return dash_main()


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')