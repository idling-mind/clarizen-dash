import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_caching import Cache

import clarizen
from dash_comps import indicate, progress, circle_graph
from helper_functions import status_colour
from components import number_card, tip_card

app = dash.Dash(__name__)

cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

TIMEOUT = 360

@cache.memoize(timeout=TIMEOUT)
def tips_data():
    projs = clarizen.get_subprojects("/Project/1nn8h0sy46ic07izfvbk84sm281")
    kpis = clarizen.work_items_by_topic("GAI KPI 2019")
    mkpis = clarizen.work_items_by_topic("GAI Manager KPI 2019")
    tips = clarizen.strategy_tip_list("GAI Strategy Domain")
    tipcount = clarizen.tip_count(tips)
    dtotal, dcompleted = clarizen.delivery_count(tips)
    return {
        'projs': projs,
        'kpis': kpis,
        'mkpis': mkpis,
        'tips': tips, 
        'tipcount': tipcount,
        'dtotal': dtotal,
        'dcompleted': dcompleted,
    }

def dash_main():
    return html.Div(className='page', children=[
        html.Div(className='container-fluid', children=[ 
            html.Div(className='page-header', children=[
                html.H3(className='page-title', children='GAI Strategy Matrix 2019')
            ]),
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
                    ]),
                ]),
            ]),
        ]),
    ])

app.layout = dash_main()

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')