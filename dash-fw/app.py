import time
import importlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State

import plotly
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px

import utils.figures as figs

from interface import *
from abm_logic import *
from abm_graphs import *

import pandas as pd

import os
import base64
import io

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
server = app.server


def generate_data(n_samples, dataset, noise):
    if dataset == "moons":
        return datasets.make_moons(n_samples=n_samples, noise=noise, random_state=0)

    elif dataset == "circles":
        return datasets.make_circles(
            n_samples=n_samples, noise=noise, factor=0.5, random_state=1
        )

    elif dataset == "linear":
        X, y = datasets.make_classification(
            n_samples=n_samples,
            n_features=2,
            n_redundant=0,
            n_informative=2,
            random_state=2,
            n_clusters_per_class=1,
        )

        rng = np.random.RandomState(2)
        X += noise * rng.uniform(size=X.shape)
        linearly_separable = (X, y)

        return linearly_separable

    else:
        raise ValueError(
            "Data type incorrectly specified. Please choose an existing dataset."
        )



app.layout = html.Div(
    children=[
        div_header("Franke-Westerhoff Explorer",
               "https://github.com/talagent",
               app.get_asset_url("logo_talagent_glyph.svg"),
               "https://talagentfinancial.com"),
        div_panel(),
    ]
)


@app.callback(
    Output("model-select",     "options"),
    [
        Input("intermediate-value","children"),
    ],
)
def populate_params(fw_params):
    fw_params = pd.read_json(fw_params, orient='split')
    options = [
            {'label': row['Name'], 'value': index}
            for index, row in fw_params.iterrows()
            ]

    return options

@app.callback(
    [
        Output("model-type",  "value"),
        Output("Phi",	  "value"),
        Output("Chi",	  "value"),
        Output("Eta",	  "value"),
        Output("alpha_w", "value"),
        Output("alpha_o", "value"),
        Output("alpha_n", "value"),
        Output("alpha_p", "value"),
        Output("sigma_f", "value"),
        Output("sigma_c", "value"),
    ],
    [
        Input("model-select","value"),
    ],
    [
        State("intermediate-value","children"),
    ],
)
def set_params(model_num, fw_params):
    if fw_params is None:
        raise dash.exceptions.PreventUpdate()
    fw_params = pd.read_json(fw_params, orient='split')
    vals = fw_params.iloc[model_num]
    if vals.empty:
        raise dash.exceptions.PreventUpdate()

    ret = [vals.values[1]]
    for v in vals.values[2:]:
        ret.append(np.float64(v))

    return ret

@app.callback(Output('rvmean', 'disabled'),
              [Input('rvmean_cb', 'value')],
              )
def enable_revmean(cb):
    return not cb

@app.callback(Output('intermediate-value', 'children'),
              [Input('upload', 'contents')],
              )
def update_output(contents):
    if contents is None:
        fw_params = pd.read_csv('data.csv')
        return fw_params.to_json(date_format='iso', orient='split')

    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(contents)
    ret = pd.read_csv(io.StringIO(str(contents)))

    return dict(ret)


@app.callback(
    [
        Output("btn-edit",   "style"),
        Output("btn-delete", "style"),
    ],
    [
        Input('model-select', 'value')
    ],
)
def set_visible(value):
    if value is None:
        disp = 'none'
    else:
        disp = 'flex'

    style = {'display': disp, 'width': '95%'}
    return [style, style]


@app.callback(
    Output("model-type",   "options"),
    [
        Input('intermediate-value', 'children')
    ],
)
def set_options(fw_params):
    return [
            {'label': 'DCA', 'value': 'DCA'},
            {'label': 'TPA', 'value': 'TPA'}
           ]


@app.callback(
        Output('card1', 'hidden'),
        [
            Input('btn-edit', 'n_clicks'),
        ],
        [
            State('card1', 'hidden'),
        ]
    )
def card1_hide(n_clicks, hidden):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate()

    return not hidden

def top5vol_tracks(data):
    if data is None:
        return [], []

    paths = np.array(data['exog_signal'])
    vol = np.std(paths, axis = 0)
    top5 = np.argsort(vol)[-5:]
    return top5

    
@app.callback(
    [
        Output("selected_curves", "children"),
        Output("old_selected_curves", "children"),
    ],
    [
        Input("graph_all_curves", "clickData"),
        Input("btn-top5vol", "n_clicks")
    ],
    [
        State("selected_curves", "children"),
        State("simulated_data", "data"),
    ]
)
def select_trace(clickData, top5, sel_curves, returns):
    ctx = dash.callback_context
    if ctx.triggered and ctx.triggered[0]['prop_id'] == 'btn-top5vol.n_clicks':
        old = sel_curves[:]
        return top5vol_tracks(returns), old

    nplots = 4
    # No click handler
    if clickData is None:
        raise dash.exceptions.PreventUpdate()

    # Get curve
    line_n = clickData['points'][0]['curveNumber'] // nplots

    old_sel_curves = sel_curves[:]
    
    # update color
    # Currently 4 graphs in subplot
    # Future improvements should allow for more or user based decision
    if line_n not in sel_curves:
        sel_curves.append(line_n)
    else:
        sel_curves.remove(line_n)

    return sel_curves, old_sel_curves


def highlight_trace(figure, trace, yes):
    nplots = 4
    if yes:
        for i in range(nplots):
            figure['data'][trace * nplots + i]['line']['width'] = 1.4
            figure['data'][trace * nplots + i]['line']['color'] = 'orange'
    else:
        for i in range(4):
            figure['data'][trace * nplots + i]['line']['width'] = 0.7
            figure['data'][trace * nplots + i]['line']['color'] = 'rgba(255,255,255,0.3)'


@app.callback(
    [
        Output("graph_all_curves", "figure"),
    ],
    [
        Input("selected_curves", "children"),
    ],
    [
        State("old_selected_curves", "children"),
        State("graph_all_curves", "figure"),
    ],
)
def update_trace(sel_curves, old_sel_curves, figure):
    # update color
    # Currently 4 graphs in subplot
    # Future improvements should allow for more or user based decision
    for trace in sel_curves:
        if trace not in old_sel_curves:
            highlight_trace(figure, trace, True)

    for trace in old_sel_curves:
        if trace not in sel_curves:
            highlight_trace(figure, trace, False)

    return [figure]


@app.callback(
    Output("dv", "children"),
    [
        Input('selected_curves', 'children'),
        Input('simulated_data', 'data'),
    ]
)
def update_sel_curves(sel_curves, ret):
    if sel_curves == [] or ret is None:
        raise dash.exceptions.PreventUpdate()

    paths = np.array(ret['exog_signal'])
    nc = np.array(ret['Nc'])
    scurves = {
            'exog_signal': paths[:,sel_curves],
            'Nc': nc[:,sel_curves],
            }

    #fig = generate_graph_prod(scurves)
    fig = distrib_plots(scurves, sel_curves)
    
    return dcc.Graph(
            id="graph_sel_curves",
            figure=fig,
            )

@app.callback(
    [
        Output("div-graphs", "children"),
        Output("simulated_data", "data"),
    ],
    [
        Input("btn-simulate", "n_clicks")
    ],
    [
        State("slider-ml", "value"),
        State("slider-ss", "value"),
        State("periods", "value"),
        State("paths", "value"),
        State("model-type", "value"),
        State("Phi",     "value"),
        State("Chi",     "value"),
        State("Eta",     "value"),
        State("alpha_w", "value"),
        State("alpha_o", "value"),
        State("alpha_n", "value"),
        State("alpha_p", "value"),
        State("sigma_f", "value"),
        State("sigma_c", "value"),
        State("rvmean", "value"),
        State("rvmean", "disabled"),
    ],
)
def update_graph(
    n_clicks,
    ml,
    ss,
    periods,
    paths,
    prob_type,
    Phi,
    Chi,
    Eta,
    alpha_w,
    alpha_o,
    alpha_n,
    alpha_p,
    sigma_f,
    sigma_c,
    rvmean,
    rvmean_disabled,
):
    if n_clicks == 0 or n_clicks is None:
        raise dash.exceptions.PreventUpdate()

    t_start = time.time()

    gparams = {
            "mu": ml,
            "beta": ss,
            "num_runs": paths,
            "periods": periods,
            "rvmean": None if rvmean_disabled else rvmean,
            "prob_type": prob_type,
            }

    cparams = {
            "phi": Phi,  ##AK: demand senstivity of the fundamental agents to price deviations.
            "chi": Chi,  ##AK: demand senstivity of the chartest agents to price deviations.
            "eta": Eta,  ##AK: performance memory (backward looking ewma)
            "alpha_w": alpha_w,  ## AK: importance of backward looking performance
            "alpha_O": alpha_o,  ## a basic predisposition toward the fundmental strategy
            "alpha_p": alpha_p,  ## misalignment; version to a fundamental strategy when price
                                 ## becomes too far from fundamental
            "sigma_f": sigma_f,  ## noise in the fundamental agent demand
            "sigma_c": sigma_c,  ## noise in the chartest agent demand
            }

    for param in cparams:
        val = cparams[param]
        if val is None:
            cparams[param] = 0

    ret = generate_constraint(gparams, cparams)
    fig = generate_graph_prod(ret)

    return [
            html.Div(
                id="svm-graph-container",
                children=dcc.Loading(
                    className="graph-wrapper",
                    children=dcc.Graph(id="graph_all_curves", figure=fig),
                    style={"display": "block"},
                    ),
                ),
            ret,
            ]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
