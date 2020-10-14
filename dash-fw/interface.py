import dash
import dash_core_components as dcc
import dash_html_components as html
import utils.dash_reusable_components as drc
import numpy as np
import pandas as pd
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import base64



def run_once(f):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            wrapper.has_run = True
            return f(*args, **kwargs)
        else:
            raise Exception('Run once: ' + str(f))
    wrapper.has_run = False
    return wrapper


def div_header(title, link, banner, link2) :
    return html.Div(
        className="banner",
        children=[
            # Change App Name here
            html.Div(
                className="container scalable",
                children=[
                    # Change App Name here
                    html.H2(
                        id="banner-title",
                        children=[
                            html.A(
                                title,
                                href=link,
                                style={
                                    "text-decoration": "none",
                                    "color": "inherit",
                                    },
                                )
                            ],
                        ),
                    html.A(
                        id="banner-logo",
                        children=[ html.Img(src=banner) ],
                        href=link2,
                        ),
                    ],
                )
            ],
        )

def div_input_line(name, id,  value):
    return html.Div([
            drc.NamedInput(
                name=name[i],
                id=id[i],
                type="number",
                value=value[i]
                ) for i in range(len(name))
            ], style={
                "display": "flex",
                "width": "95%",
                },
            )

def card0():
    return drc.Card(
        id = 'select_card',
        children=[
            drc.ButtonInput('Random seed', 'rnd_seed',
                id =  'seed_val', value = 0),
            dcc.Dropdown(
                id="model-select",
                value = None,
                clearable=False,
                searchable=False,
                ),
            html.Div([
                html.Button(
                    "Show / Hide",
                    id="btn-edit",
                    style={
                    'color': 'inherit',
                    "display": "flex",
                    "width": "95%",
                    },
                    ),
                html.Button(
                    "Delete",
                    id="btn-delete",
                    style={
                    'color': 'inherit',
                    "display": "flex",
                    "width": "95%",
                    },
                    ), 
            ], style={
                "display": "flex",
                },
            ),
            ]
        )


def card1():
    return drc.Card(
        id="card1",
        hidden = True,
        children=[
            drc.NamedRadioItems(
                name='Model',
                id='model-type',
                labelStyle={
                    'margin-right': '7px',
                    'display': 'inline-block'
                    },
                value=None,
                ),
            div_input_line(
                ["Phi", "Chi", "Eta"],
                ["Phi", "Chi", "Eta"],
                [None, None, None],
                ),
            div_input_line(
                ["alpha_w", "alpha_o", "alpha_n"],
                ["alpha_w", "alpha_o", "alpha_n"],
                [None, None, None],
                ),
            div_input_line(
                ["alpha_p", "sigma_f", "sigma_c"],
                ["alpha_p", "sigma_f", "sigma_c"],
                [None, None, None],
                ),
            div_input_line(
                ["chi1", "nu", "sigma_n"],
                ["chi1", "nu", "sigma_n"],
                [None, None, None],
                ),
            ]
        )

def card_swipe():
    istyle = {'color': 'inherit',
            'width': '95%',
             }
    return drc.Card(
        id = "card_swipe",
        hidden = True,
        children=[
             dcc.Dropdown(
                options = [
                        {'label': 'Phi',     'value': 'phi'},
                        {'label': 'Chi',     'value': 'chi'},
                        {'label': 'Eta',     'value': 'eta'},
                        {'label': 'alpha_w', 'value': 'alpha_w'},
                        {'label': 'alpha_o', 'value': 'alpha_O'},
                        {'label': 'alpha_n', 'value': 'alpha_n'},
                        {'label': 'alpha_p', 'value': 'alpha_p'},
                        {'label': 'sigma_f', 'value': 'sigma_f'},
                        {'label': 'sigma_c', 'value': 'sigma_c'},
                        {'label': 'sigma_n', 'value': 'sigma_n'},
                        {'label': 'nu',      'value': 'nu'},
                        {'label': 'chi1', 'value': 'chi1'},
                        ],
                 id="swipe-select",
                 value = 'phi',
                 clearable=False,
                 searchable=False,
                 style={
                     'display': 'block',
                     },
                 ),
            html.Div(
                style={
                    #"margin-left": "6px",
                     'display': 'flex',
                    },
                children = [
                    drc.NInput('Start', id = 'swipe_start', value = None,
                        type = 'number', style = istyle,),

                    drc.NInput('Step', id = 'swipe_step', value = None,
                        type = 'number', style = istyle,),

                    drc.NInput('Stop', id = 'swipe_stop', value = None,
                        type = 'number', style = istyle,),
                    ]
                ),
             dcc.Dropdown(
                options = [
                        {'label': 'Price',   'value': 'Price'},
                        {'label': 'Return',  'value': 'Return'},
                        ],
                 id="swipe-type",
                 value = 'Return',
                 clearable=False,
                 searchable=False,
                 style={
                     'display': 'block',
                     },
                 ),
            html.Div(
                id = 'return_params',
                style={
                     'display': 'flex',
                     #'display': 'none',
                    },
                children = [
                    drc.NInput('Start Period', id = 'start_period', value = 2,
                        type = 'number', style = istyle,),

                    drc.NInput('Stop Period', id = 'stop_period', value = 500,
                        type = 'number', style = istyle,),

                    ]
                ),
            dcc.Checklist(
                id = 'hold',
                options=[
                    {'label': 'Hold', 'value': 'hold'},
                ],
                ),
            html.Button(
                "Swipe",
                id="btn_swipe",
                style = {'color': 'inherit',
                         'display': 'flex',
                         "width": "100%"},
                )
            ]
        )


def card2():
    return drc.Card(
        id="button-card",
        children=[
            div_input_line(
                ["Periods", "Paths"],
                ["periods", "paths"],
                [500, 100],
                ),
            drc.NamedSlider(
                name="Market Liquidity",
                id="slider-ml",
                min=0,
                max=0.1,
                step=0.001,
                marks={
                    i/100: str(i/100)
                    for i in range(0, 11, 2)
                    },
                tooltip = {"always_visible": False,
                        "placement": "top"},
                value=0.01,
                ),
            drc.NamedSlider(
                name="Switching Strength",
                id="slider-ss",
                min=0.1,
                max=2,
                marks={
                    i / 10: str(i / 10)
                    for i in range(0, 20, 4)
                    },
                step=0.1,
                tooltip = {"always_visible": False,
                        "placement": "top"},
                value=1
                ),
            drc.CheckboxSlider("Fundamental price window", 'rvmean_cb', enabled = False,
                id = 'rvmean',
                min = 1,
                max = 365,
                marks={
                    i: str(i)
                    for i in range(0, 365, 90)
                    },
                tooltip = {
                    "always_visible": False,
                    "placement": "top"
                    },
                value = 180,
                ),
            drc.CheckboxSlider("Effective return window", 'retmean_cb', enabled = False,
                id = 'retmean',
                min = 1,
                max = 21,
                marks={
                    i: str(i)
                    for i in range(0, 21, 5)
                    },
                tooltip = {
                    "always_visible": False,
                    "placement": "top"
                    },
                value = 5,
                ),
            html.Button(
                "Simulate",
                id="btn-simulate",
                style = {'color': 'inherit', },
                ),
            dcc.Checklist(
                id = 'pick_checkbox',
                options=[
                    {'label': 'Start from picked point', 'value': 'enable'},
                ],
		value = []
                ),
            html.Button(
                "Pick Start",
                id="pick_start",
                style = {'color': 'inherit', },
                ),
            ],
        )


def card3():
    return drc.Card(
        id="last-card",
        children=[
            html.Div([
                drc.ButtonInput('Random', 'btn_rand',
                   id =  'rand_val', value = 20),
                drc.ButtonInput('Most volatile', 'mostvol',
                   id =  'mostvol_val', value = 10),
                drc.ButtonInput('Least volatile', 'lessvol',
                   id =  'lessvol_val', value = 10),
                drc.ButtonInput('Max drawdown', 'maxdd',
                   id =  'maxdd_val', value = 10),
            ], style={
            #    "display": "flex",
                },
            ),
            ],
        )


def graph_tabs():
    return html.Div([
                dcc.Tabs(id="tabs",
                         vertical=False,
                         value = 'One',
                         parent_style={'flex-direction': 'column',
                                       '-webkit-flex-direction': 'column',
                                       '-ms-flex-direction': 'column',
                                       'display': 'flex'},
                         colors={"border": "white",
                                 "primary": "white",
                                 "background": "grey"
                                 },
                         children=[

                             dcc.Tab(
                                 label='Save/Load',
                                 style={'backgroundColor': "inherit"},
                                 selected_style={'backgroundColor': "inherit",'color':'white'},
                                 value = 'ABM1',
                                 children = [
                                     html.Div(
                                           id="saved_title1",
                                           children = [
                                               dcc.Markdown(''' ### Save Model '''),
                                               ]
                                           ),
                                     html.Div([
                                        dcc.Input(
                                            id="filename",
                                            type='text',
                                            style={
                                            'color': 'inherit',
                                            "display": "flex",
                                            "width": "100%",
                                            },
                                            placeholder="File Name"
                                            ),
                                        html.Button(
                                            "Save",
                                            id="btn_save",
                                            style={
                                            'color': 'inherit',
                                            "display": "flex",
                                            "width": "30%",
                                            },
                                            ),
                                        ], style={
                                        "display": "flex",
                                        },
                                    ),
                                    html.Div(
                                        id="saved_title2",
                                        children = [
                                            dcc.Markdown(''' ### Load Model '''),
                                            ]
                                     ),
                                     html.Div([
                                        dcc.Dropdown(
                                            id="load_filename",
                                            value = None,
                                            clearable=False,
                                            searchable=False,
                                            style={
                                                'color': 'inherit',
                            #                    "display": "flex",
                                                "width": "100%",
                                            },
                                            placeholder="File Name"
                                            ),
                                            html.Button(
                                                "Load",
                                                id="btn_load",
                                                style={
                                                'color': 'inherit',
                                                "display": "flex",
                                                "width": "30%",
                                                },
                                                ),
                                        ], style={
                                            "display": "flex",
                                            },
                                        ),
                                        html.Div(
                                           id="saved_comment",
                                           #style = {'display': 'inline-block'},
                                           children = [
                                               dcc.Markdown(''' ### Comments '''),
                                               ]
                                           ),
                                        html.Div(
                                           #id="comments_txt",
                                           #style = {'display': 'inline-block'},
                                           children = [
                                               dcc.Textarea(id="comments_txt", 
                                                            style={'width': 1500, 
                                                                   'height':420, 
                                                                   'font-size': 18,
                                                                   'color':'white'}),
                                               ],
                                           style=dict(display='flex')
                                           )
                                     ],
                                ),
                             dcc.Tab(
                                 label='Main view',
                                 style={'backgroundColor': "inherit"}, 
                                 selected_style={'backgroundColor': "inherit",'color':'white'},
                                 value = 'One',
                                 children = [
                                     html.Div(
                                         id="div-graphs",
                                             children=dcc.Graph(
                                                 id="graph_all_curves",
                                                 figure=dict(
                                                     layout=dict(
                                                         plot_bgcolor="#282b38",
                                                         paper_bgcolor="#282b38"
                                                     )
                                                 ),
                                             ),
                                         )
                                     ]
                                ),
                               dcc.Tab(
                                   label='Detailed view',
                                   value = 'Two',
                                   style={'backgroundColor': "inherit"}, 
                                   selected_style={'backgroundColor': "inherit",'color':'white'},
                                   children = [
                                       html.Div(
                                           id="dv",
                                           children=dcc.Graph(
                                               id="graph_sel_curves",
                                               figure=dict(
                                                   layout=dict(
                                                       plot_bgcolor="#282b38",
                                                       paper_bgcolor="#282b38"
                                                       )
                                                   ),
                                               ),
                                           )
                                       ]
                                   ),
                               dcc.Tab(
                                   label='Sensitivity',
                                   value = 'tab_sensitivity',
                                   style={'backgroundColor': "inherit"}, 
                                   selected_style={'backgroundColor': "inherit",'color':'white'},
                                   children = [
                                       html.Div(
                                           id="sens",
                                           #style = {'display': 'inline-block'},
                                           children = [
                                               dcc.Graph(
                                                   id="phi_sens",
                                                   figure=dict(
                                                       layout=dict(
                                                           plot_bgcolor="#282b38",
                                                           paper_bgcolor="#282b38"
                                                           )
                                                       ),
                                                   ),
                                               dcc.Graph(
                                                   id="chi_sens",
                                                   figure=dict(
                                                       layout=dict(
                                                           plot_bgcolor="#282b38",
                                                           paper_bgcolor="#282b38"
                                                           )
                                                       ),
                                                   ),
                                               ]
                                           )
                                       ]
                                   ),
                               dcc.Tab(
                                   label='User Guide',
                                   value = 'User Guide',
                                   style={'backgroundColor': "inherit"}, 
                                   selected_style={'backgroundColor': "inherit",'color':'white'},
                                   children = [ ###
                                       dcc.Tabs(id="tabs_guide",
                                         vertical=False,
                                         value = 'tabsguide',
                                         parent_style={'flex-direction': 'column',
                                                       '-webkit-flex-direction': 'column',
                                                       '-ms-flex-direction': 'column',
                                                       'display': 'flex'},
                                         colors={"border": "white",
                                                 "primary": "white",
                                                 "background": "grey"
                                                 },
                                         children=[
                                             dcc.Tab(
                                               label='Model controls',
                                               #value = 'User Guide Tab 1',
                                               style={'backgroundColor': "inherit"}, 
                                               selected_style={'backgroundColor': "inherit",'color':'white'},
                                               children = [
                                                   dcc.Markdown('''

### Model controls 
#### Section 1. Basic settings - Left Panel

This is the Exploration tool for the Franke-Westerhoff structural stochastic volatility model.
Start working with the explorer by choosing an appropriate **SEED**, or let the tool pick a random
value for you.

7 models from the original paper, as well as an extended model including a leveraged agent, 
are presented as presets. Choose a model to simulate from the drop box. The models may be customized by 
the user if needed. 

                                                    '''),

                                                html.Img(src=dash.Dash().get_asset_url('01_seed_model_show.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),
              
              
                                                   dcc.Markdown('''              
#### Section 2. Model parameters - Left Panel

All parameters are editable by clicking **SHOW / HIDE** button. Original values of the parameters
are preserved while experimenting.

                                                    '''),

                                                html.Img(src=dash.Dash().get_asset_url('02_params_showhide.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),                                                 


                                                   dcc.Markdown(''' 
\n              
Use **Periods** and **Paths** input boxes to set length of simulation and number of individual
trajectory paths accordingly.

Market Liquidity and Switching Strength sliders set corresponding model parameters as appropriate.

                                                    '''),

                                                html.Img(src=dash.Dash().get_asset_url('03_Periods_paths_sliders.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),
                                                

                                                   dcc.Markdown(''' 
\n
**Fundamental price window** and **Effective return window** are two extensions added to the model
that allow to extend simulation flexibility.

**Fundamental price window** is used to determine a time period for calculating the fundamental price.
If disabled, the fundamental price is always **1**, while if the feature is enabled, the fundamental price
is calculated as an average price for the last **N** periods, as set on slider control. This control affects
the Fundamentalists behaviour. If at some specific simulation the price deviates from **1** for a period of
time comparable to the window, the price effectively becomes a new fundamental value.

**Effective return window** affects the behaviour of the chartists. If disabled, chartists's
prediction on market is based on last return. If the feature is enabled, the average return of the last
**N** periods is used used to calculate the 'effective return'. This feature may be used to simulate 
'weekly chartists', for example.

                                                    '''),
                                                    
                                                    html.Img(src=dash.Dash().get_asset_url('04_price_windows.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),


                                                   dcc.Markdown('''
#### Section 3. Generate Model Simulations - Left Panel

\n
**Simulate** button starts the simulaton. No simulation traces will appear when the simulation is complete.
Refer to the **Display** tab of this guide for plotting outputs.
\n
**Pick Start** and **Start from picked point** are discussed in **Section 4. Display Model Simulations**.

                                                    '''),

                                                    html.Img(src=dash.Dash().get_asset_url('05_simulate.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),

                                                 
                                                   ]
                                               ),
                                                                
                                                                
                 
                                            # Display  Main                  
                                            dcc.Tab(
                                               label='Results - Main View',
                                               style={'backgroundColor': "inherit"}, 
                                               selected_style={'backgroundColor': "inherit",'color':'white'},
                                               children = [
                                                   dcc.Markdown('''
### Display Model Simulations 
                                                   
#### Section 1. Select simulations - Left Panel

\n
Displaying all simulated traces is computationally expensive and can crash the output. 
We structured the output traces by properties, and marked them with individual colours. 
User can pick traces with the desired properties to display at will, together with the number of traces 
per option.

\n
The supported properties are:
* Random: pick random traces
* Most volatile: pick N most volatile traces
* Least volatile: pick N least volatile traces
* Max drawdown: pick traces demonstrating maximal loss in price at any point in time

                                                    '''),
                                                    
                                                   html.Img(src=dash.Dash().get_asset_url('06_display_option.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),
              
                                                   dcc.Markdown('''
\n
#### Section 2. Simulations display - Main View Tab
The selected traces are displayed in the **Main View** tab. 

The plot is interactive and the user can:
* zoom in by selecting a zone in the graph area
* zoom out by double clicking a zone in the graph area
* select a trace by clicking on it on the graph and get detailed graphical results in **Detailed View** tab (1)
* hide/show a simulation by clicking on its name in the legend (2)
* show a unique/all simulation(s) on screen by **double** clicking on its name in the legend (2)
* reset the display by clicking on the house icon in the Plotly toolbar (3)


                                                    '''),
                                                   html.Img(src=dash.Dash().get_asset_url('07_DisplayMain.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'90%'}),                                                    
                                                 
                                                   ]
                                               ),
                                                                
                                                                
                                                                
                                            # Display  Swipe                  
                                            dcc.Tab(
                                               label='Results - Swipe',
                                               style={'backgroundColor': "inherit"}, 
                                               selected_style={'backgroundColor': "inherit",'color':'white'},
                                               children = [
                                                   dcc.Markdown('''
### Display Parameter sensitivities
     
\n
The user can run simulations for a specific range of a parameter, keeping all others variables intact.
The result of these simulations is displayed as statistical plots defining the sensitivities of
the model to that specific parameter accross that range.

#### Section 1. Define Parameters - Left Panel

\n
The user can:
* Choose an appropriate parameter (1) 
* Define a value range and a step size (default: 50% to 150% with a 10% step size)
* Select effect on returns or price (2)
* Select the period accross which the parameter is swiped (default: 2 to 500)
* Click swipe to get results (3) 
* Selecting "hold" will allow the user to repeat the above while keeping actual results on the plots


                                                    '''),
                                                    
                                                   html.Img(src=dash.Dash().get_asset_url('10_controlswipe.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'25%'}),
              
                                                   dcc.Markdown('''
\n
#### Section 2. Swipe display - Sensitivity Tab
The results are displayed in the **Sensitivity** tab. 
The distribution for lowest, highest and current values of the parameter are displayed as well

The plot is interactive and the user can:
* zoom in by selecting a zone in the graph area
* zoom out by double clicking a zone in the graph area
* Observe the parameter's range is located on the x axis of the plots (1)
* Hoover above traces will allow the user to know the values of the parameter (2)
* Reset the display by clicking on the house icon in the Plotly toolbar (3)
a
 

                                                    '''),
                                                   html.Img(src=dash.Dash().get_asset_url('11_resultswipe.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'90%'}),                                                   
                                                 
                                                   ]
                                               ),
                                        
                                                                
                                                                
                                                                
                                                                
                                            # Load / Save Tab                    
                                            dcc.Tab(
                                               label='Save Load',
                                               style={'backgroundColor': "inherit"}, 
                                               selected_style={'backgroundColor': "inherit",'color':'white'},
                                               children = [
                                                   dcc.Markdown('''
### Save and Load Models - Save/Load Tab

#### Section 1. Save Model

                                                                '''),
                                                   html.Img(src=dash.Dash().get_asset_url('08_Save.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'90%'}),
                                                                
                                                   dcc.Markdown('''                                                                
\n
You can save the current state of your model by following these steps:
* Click on the Save/Load Tab
* Under Save Model, choose an appropriate file name (1)
* If you want, you can write a comment in the text area - this will be saved with the model
* Click **SAVE** (2)
* Your current model has been saved

#### Section 2. Load Model


                                                                '''),
                                                                
                                                   html.Img(src=dash.Dash().get_asset_url('09_Load.png'), 
                                                         style={'height':'auto', 'width':'auto',
                                                                'max-width':'90%'}),



                                                   dcc.Markdown('''

You can load a previously saved model by following these steps:
* Click on the Save/Load Tab
* Under Load Model, select the model you wish to load (1)
* If you wrote a comment for the selected model, it will appear in the comment section
* Click **LOAD** (2)
* Your model has been loaded
 
                                                    '''),

                                                   ]
                                               )
                                             ]
                                         )
                                       ]
                                   ),                         
                               ],
                         ),
                                                            
                                                            
                               
                           html.Div(
                               id = 'selected_curves',
                               children = [],
                               style={'display': 'none'}
                               ),
                           html.Div(
                               id = 'old_selected_curves',
                               children = [],
                               style={'display': 'none'}
                               ),
                ],
                style={'width': '75%',
                       #'float': 'left'
                       }
                )


def div_panel():
    return html.Div(
            id="body",
            #className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                dcc.Upload(
                                    id='upload',
                                    children=html.Div([
                                        'Drag and Drop or ',
                                        html.A('Select FW file.')
                                        ]),
                                    disabled = True,
                                    style={'display': 'none'},
                                    #multiple = False,
                                    ),
                                card0(),
                                card1(),
                                card_swipe(),
                                card2(),
                                card3(),
                                #card_save(),
                                dcc.Store(id='cal_params'),
				dcc.Store(id='click_data'),
                                dcc.Store(id='start_params'),
                                dcc.Store(id='simulated_data'),
                                dcc.Store(id='visible_topvol', data = None),
                                dcc.Store(id='visible_lessvol', data = None),
                                dcc.Store(id='visible_maxdd', data = None),
                                dcc.Store(id='visible_random', data = None),
                                dcc.Store(id='Swipe_data', data = None),
                                dcc.Store(id='Load_trigger', data = None),
                        ],
                        #style={'width':'30%'},
                    ),
                        graph_tabs(),
                    ],
                    #style={'width':'30%'},
                    #style={'display': 'flex'},
            )
        ],
        style={'display': 'flex'},
    ) 
