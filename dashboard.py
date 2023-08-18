#################################################
#### importing libraries
#################################################

from dash import Dash,html,dcc
import dash_bootstrap_components as dbc
from dash.dependencies import State,Input,Output
import geocoder
import folium
from branca.element import Figure
import openrouteservice
from folium import plugins
from geopy.distance import distance
from random_coordinates import create_dataset
import pandas as pd
import plotly.graph_objs as go
import urllib.request
import json
import math
import numpy as np
import dash_auth
import utm

#################################################
### finding default coordinates to be used on the placeholders
#################################################

bt = geocoder.osm('blantyre,malawi')
zomba = geocoder.osm('zomba,malawi')

#################################################
### creating the application
#################################################

def create_dash_application(flask_app):
    
    app = Dash(server = flask_app,name = 'Dashboard',url_base_pathname = '/dash/',suppress_callback_exceptions = True,prevent_initial_callbacks = False,external_stylesheets = [dbc.themes.DARKLY,dbc.themes.CYBORG,dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME])

    
    dash_auth.BasicAuth(app,
                               {'precious':'xenerageo',
                                'precious2':'xenerageo2'})
    
    # creating navigation butttons
    navigation =  dbc.Nav([
                                    
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-globe",style = {'color':'peachpuff'}),'  Explore Map']),href = '/dash/',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-pencil",style = {'color':'peachpuff'}),'  Edit Map']),href = '/edit_map',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-road",style = {'color':'peachpuff'}),'  Distances']),href = '/distance',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-level-up",style = {'color':'peachpuff'}),'  Elevation']),href = '/elevation',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-angle-double-up",style = {'color':'peachpuff'}),'  Elevation Profile']),href = '/ele_profile',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-map-marker",style = {'color':'peachpuff'}),'  Geocoding']),href = '/geocoding',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-calculator",style = {'color':'peachpuff'}),'  Calculator']),href = '/calculator',active = 'exact'),
                        dbc.NavLink(children = html.H6([html.I(className = "fa-solid fa-sign-out",style = {'color':'peachpuff'}),'  Log Out']),href = '/',external_link = True,active = 'exact')
                        
                        ],pills = True,vertical = True,style = {'position':'fixed','left':'100px'})
        
    # creating the content object
    content = dbc.Row([
        dbc.Col(id = 'contents',width = {'size':12},style = {'height':'auto',"background-image": "url('https://images.unsplash.com/photo-1597773150796-e5c14ebecbf5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZGFyayUyMGJsdWV8ZW58MHx8MHx8&w=1000&q=80')",'background-size':'cover','background-position':'center'})])
    
    # designing the layout
    app.layout = dbc.Container([
        
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        html.Img(src = 'https://w5nby5.deta.dev/stream_site_pic/j.jpg',alt = '',style = {'border-radius':'50%','border-style':'ridge'},height = '200px',width = '200px')
                        ],width = {'size':10,'offset':2})
                    ]),
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        html.Br(),
                        navigation
                        ],width = {'size':12})
                    ])
                ],style = {'position':'fixed','bottom':0,'left':0,'top':0,'background-color':'rgb(20, 33, 54)','border-right-style':'ridge'},width = {'size':3}),
            dbc.Col([
                dcc.Location(id = 'url'),
                content],width = {'size':9,'offset':3})
            ])
    
    ],fluid = True)
    
    
    # a function to return contents
    @app.callback(Output('contents','children'),Input('url','pathname'))
    def content_map_type(url_):
        
        try:
            
            # contents for homepage
            if url_ == '/dash/':
                
                output = [
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Input(id = 'latitude_map_type',placeholder = 'Latitude',value = float(bt.lat),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4,'offset':1}),
                            dbc.Col([
                                dcc.Input(id = 'longtude_map_type',placeholder = 'longtude',value = float(bt.lng),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4}),
                            dbc.Col([
                                dbc.Button(id = 'map_search',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Locate']),style = {'height':'40px','width':'110px','border-radius':'10px'}),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                        dbc.ModalBody(id = "modal-body2",style = {'background-color':'rgb(20, 33, 54)'})
                                    ],id="modal2",is_open=False)
                                ],width = {'size':3})])
                        ],style = {'height':'100px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white','border-radius':'10px'}),
                    html.Br(),
                    html.Div([
                            html.Iframe(id = 'map_type_map',height = '100%',width = '100%',style = {'border-radius':'10px'})
                            ],style = {'width':'980px','height':'500px','border-style':'ridge','border-radius':'10px'}),
                    html.Br(),
                    html.Br()
                        
                    ]
             
            # contents for edit map page
            elif url_ == '/edit_map':
                
                output = [
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Input(id = 'latitude_map_type2',placeholder = 'Latitude',value = float(bt.lat),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4,'offset':1}),
                            dbc.Col([
                                dcc.Input(id = 'longtude_map_type2',placeholder = 'longtude',value = float(bt.lng),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4}),
                            dbc.Col([
                                dbc.Button(id = 'map_search2',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Locate']),style = {'height':'40px','width':'110px','border-radius':'10px'}),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                        dbc.ModalBody(id = "modal-body3",style = {'background-color':'rgb(20, 33, 54)'})
                                    ],id="modal3",is_open=False)
                                ],width = {'size':3})])
                        ],style = {'height':'100px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white','border-radius':'10px'}),
                    html.Br(),
                    html.Div([
                            html.Iframe(id = 'map_type_map2',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                            ],style = {'width':'980px','height':'500px','border-style':'ridge','border-radius':'10px'}),
                    html.Br(),
                    html.Br()
                    ]
              
            # contents for distance page
            elif url_ == '/distance':
                
                output = [
                    
                    dbc.Row([
                        
                        dbc.Col([
                            
                            html.Br(),
                            html.Div([html.Iframe(id = 'straight_line_map',height = '100%',width = '100%',style = {'border-radius':'10px'})],style = {'height':'600px','width':'650px','border-style':'ridge','border-radius':'10px'}),
                            html.Br(),
                            html.Br()
                                  
                            ],width = {'size':8}),
                        dbc.Col([
                            html.Br(),
                            html.Div([
                                
                                dbc.Card([
                                    html.Br(),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Input(id = 'latitude_origin',placeholder = 'Origin Latitude',value = float(bt.lat),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                            ],width = {'size':9,'offset':2})
                                        ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Input(id = 'longtude_origin',placeholder = 'Origin Longtude',value = float(bt.lng),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                            ],width = {'size':9,'offset':2})
                                        ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Input(id = 'destination_latitude',placeholder = 'Destination Latitude',value = float(zomba.lat),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                            ],width = {'size':9,'offset':2})
                                        ]),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Input(id = 'destination_longtude',placeholder = 'Destination Longtude',value = float(zomba.lng),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                            ],width = {'size':9,'offset':2})
                                        ]),
                                    html.Br(),
                                    html.Hr(),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.RadioItems(id = 'path_type',value = 'straight line',options = [{'label':'straight line','value':'straight line'},{'label':'route','value':'route'}])
                                            ],width = {'size':9,'offset':3})
                                        ]),
                                    html.Br(),
                                    html.Hr(),
                                    html.Br(),
                                    dbc.Row([
                                        dbc.Col([
                                            dcc.Dropdown(id = 'route_profile',value = 'foot-walking',options = [{'label':'driving-car','value':'driving-car'},{'label':'foot-walking','value':'foot-walking'},{'label':'cycling-road','value':'cycling-road'},{'label':'cycling-mountain','value':'cycling-mountain'},{'label':'cycling-regular','value':'cycling-regular'},{'label':'foot-hiking','value':'foot-hiking'}],style = {'background-color':'rgb(69, 205, 230)','border-radius':'10px','color':'black','text-align':'center'})
                                            ],width = {'size':8,'offset':2})
                                        ]),
                                    html.Br(),
                                    html.Hr(),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Button(id = 'change_path_type',children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Locate']),n_clicks = 0,style = {'height':'40px','width':'110px','border-radius':'10px'}),
                                            dbc.Modal(
                                                [
                                                    dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                    dbc.ModalBody(id = "modal-body4",style = {'background-color':'rgb(20, 33, 54)'})
                                                ],id="modal4",is_open=False)
                                            ],width = {'size':8,'offset':4})
                                        ])
                                    ],style = {'height':'100%','width':'100%','border-color':'white'})
                                ],style = {'height':'600px','width':'300px'})
                            ],width = {'size':4})
                        
                        ])
                    
                    ]
             
            # contents for elevation page
            elif url_ == '/elevation':
                
                output = [
                    
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Input(id = 'latitude_map_type3',placeholder = 'Latitude',value = float(bt.lat),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4,'offset':1}),
                            dbc.Col([
                                dcc.Input(id = 'longtude_map_type3',placeholder = 'longtude',value = float(bt.lng),style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':4}),
                            dbc.Col([
                                dbc.Button(id = 'map_search3',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Locate']),style = {'height':'40px','width':'110px','border-radius':'10px'}),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                        dbc.ModalBody(id = "modal-body5",style = {'background-color':'rgb(20, 33, 54)'})
                                    ],id="modal5",is_open=False)
                                ],width = {'size':3})])
                        ],style = {'height':'100px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white','border-radius':'10px'}),
                    html.Br(),
                    html.Div([
                            html.Iframe(id = 'elevation_map',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                            ],style = {'width':'980px','height':'500px','border-style':'ridge','border-radius':'10px'}),
                    html.Br(),
                    html.Br() 
                    
                    ]
            # contents for geocoding page   
            elif url_ == '/geocoding':
                
                output = [
                    
                    html.Br(),
                    dbc.Card([
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                dcc.Input(id = 'place_name',placeholder = 'place',value = 'zomba,malawi',style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'})
                                ],width = {'size':5,'offset':3}),
                            dbc.Col([
                                dbc.Button(id = 'map_search4',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Locate']),style = {'height':'40px','width':'110px','border-radius':'10px'}),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                        dbc.ModalBody(id = "modal-body6",style = {'background-color':'rgb(20, 33, 54)'})
                                    ],id="modal6",is_open=False)
                                ],width = {'size':4})])
                        ],style = {'height':'100px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white','border-radius':'10px'}),
                    html.Br(),
                    html.Div([
                            html.Iframe(id = 'geocoding_map',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                            ],style = {'width':'980px','height':'500px','border-style':'ridge','border-radius':'10px'}),
                    html.Br(),
                    html.Br()
                    
                    ]
             
            #contents for calculator    
            elif (url_ == '/calculator') | (url_ == '/utm'):
                
                nav = dbc.Nav([
                                                
                                    dbc.NavLink(children = 'To Lat/Lng',href = '/calculator',active = 'exact'),
                                    dbc.NavLink(children = 'To Eas/Nort',href = '/utm',active = 'exact')
     
                                    ],pills = True)
                
                if url_ == '/calculator':
                    
                    output = [
                    
                        html.Br(),
                        nav,
                        html.Br(),
                        dbc.Row([
                            
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'Easting',placeholder = 'Easting',value = 746255.000,style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'Northing',placeholder = 'Northing',value = 8294118.000,style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])

                                            
                                            ],width = {'size':12})
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'Zone Number',placeholder = 'Zone Number',value = 36,style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'Zone Letter',placeholder = 'Zone Letter',value = 'L',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])
                                            ],width = {'size':12})
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Button(id = 'calcu',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Compute']),style = {'height':'40px','width':'120px','border-radius':'10px'}),
                                                    dbc.Modal(
                                                        [
                                                            dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                            dbc.ModalBody(id = "modal-bodyc",style = {'background-color':'rgb(20, 33, 54)'})
                                                        ],id="modalc",is_open=False)
                                                    ],width = {'size':4,'offset':4})
                                                ])
                                            ],width = {'size':12})
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'tolat',placeholder = 'Latitude',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'tolon',placeholder = 'Longtude',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])
                                            ])
                                        ])
                                    
                                    ],style = {'background-color':'rgb(20, 33, 54)','height':'550px','border-radius':'10px','border-color':'white'})
                                
                                ],width = {'size':6,'offset':3})
                            
                            ]),
                        html.Br(),
                        html.Br(),
                        html.Br()
                    
                        ]
                    
                elif url_ == '/utm':
                        
                    output = [
                        
                        html.Br(),
                        nav,
                        html.Br(),
                        dbc.Row([
                            
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'lat_2',placeholder = 'Latitude',value = zomba.lat,style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'lon_2',placeholder = 'Longtude',value = zomba.lng,style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])

                                            
                                            ],width = {'size':12})
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Button(id = 'calcu2',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Compute']),style = {'height':'40px','width':'120px','border-radius':'10px'}),
                                                    dbc.Modal(
                                                        [
                                                            dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                            dbc.ModalBody(id = "modal-bodyc2",style = {'background-color':'rgb(20, 33, 54)'})
                                                        ],id="modalc2",is_open=False)
                                                    ],width = {'size':4,'offset':4})
                                                ])
                                            ],width = {'size':12})
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'east2',placeholder = 'Easting',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'north2',placeholder = 'Northing',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])
                                            ])
                                        ]),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Br(),
                                            html.Br(),
                                            dbc.Row([
                                                dbc.Col([
                                                    dcc.Input(id = 'Zone Number2',placeholder = 'Zone Number',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4,'offset':2}),
                                                dbc.Col([
                                                    dcc.Input(id = 'Zone Letter2',placeholder = 'Zone Letter',style = {'border-radius':'10px','width':'150px','text-align':'center'})
                                                    ],width = {'size':4})
                                                ])
                                            ],width = {'size':12})
                                        ])
                                    
                                    ],style = {'background-color':'rgb(20, 33, 54)','height':'550px','border-radius':'10px','border-color':'white'})
                                
                                ],width = {'size':6,'offset':3})
                            
                            ]),
                        html.Br(),
                        html.Br(),
                        html.Br()
                        
                        ]
              
             # contents for elevation profile   
            elif (url_ == '/ele_profile') | (url_ == '/ele_profile/2model') | (url_ == '/ele_profile/dmodel'):
                
                nav = dbc.Nav([
                                                
                                    dbc.NavLink(children = '3D model',href = '/ele_profile',active = 'exact'),
                                    dbc.NavLink(children = '2D model',href = '/ele_profile/2model',active = 'exact'),
                                    dbc.NavLink(children = 'Distance model',href = '/ele_profile/dmodel',active = 'exact')

                                    
                                    ],pills = True)
                
                
                if url_ == '/ele_profile':
                
                    output = [
                    
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                        html.Iframe(id = 'map_for_profile',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                                        ],style = {'width':'980px','height':'300px','border-style':'ridge','border-radius':'10px'})
                                ],width = {'size':12})
                            ]),
                        html.Br(),
                        nav,
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                
                                dbc.Card([
                                    dbc.Row([
                                                dbc.Col([
                                                        
                                                    dbc.Row([
                                                            dbc.Col([
                                                                dcc.Graph(id = 'terrain',style = {'height':'398px','width':'640px'})
                                                                ],width = {'size':12})
                                                            ])
                                                        
                                                        ],width = {'size':9}),
                                                    dbc.Col([
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'points',placeholder = 'number of points',value = 500,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'min_lat',placeholder = 'min lat',value = bt.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'max_lat',placeholder = 'max lat',value = zomba.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'min_lng',placeholder = 'min lng',value = bt.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'max_lng',placeholder = 'max lng',value = zomba.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        dbc.Row([
                                                            dbc.Col([
                                                                
                                                                dbc.Button(id = 'simulate',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Simulate']),style = {'height':'40px','width':'120px','border-radius':'10px'}),
                                                                dbc.Modal(
                                                                    [
                                                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                                        dbc.ModalBody(id = "modal-body7",style = {'background-color':'rgb(20, 33, 54)'})
                                                                    ],id="modal7",is_open=False)
                                                                ],width = {'size':9,'offset':2})
                                                        ])
                                                        ],width = {'size':3})
                                                    
                                                    ])
                                                ],style = {'height':'400px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white'})
                                
                                ],width = {'size':12})
                            ]),
                        html.Br()
                    
                    
                        ]
                    
                elif url_ == '/ele_profile/2model':
                        
                        output = [
                            
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                            html.Iframe(id = 'map_for_profile',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                                            ],style = {'width':'980px','height':'300px','border-style':'ridge','border-radius':'10px'})
                                    ],width = {'size':12})
                                ]),
                            html.Br(),
                            nav,
                            html.Br(),
                            dbc.Row([
                                dbc.Col([
                                    
                                    dbc.Card([
                                        
                                        dbc.Row([
                                            dbc.Col([
                                                
                                                dbc.Row([
                                                        dbc.Col([
                                                            dcc.Graph(id = 'terrain2d',style = {'height':'398px','width':'640px'})
                                                            ],width = {'size':12})
                                                        ])
                                                
                                                ],width = {'size':9}),
                                            dbc.Col([
                                                
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'points2',placeholder = 'number of points',value = 100,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'startl',placeholder = 'start lat',value = bt.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'startl2',placeholder = 'start lng',value = bt.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'endl',placeholder = 'end lat',value = zomba.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'endl2',placeholder = 'end lng',value = zomba.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        dbc.Row([
                                                            dbc.Col([
                                                                
                                                                dbc.Button(id = 'simulate22',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Simulate']),style = {'height':'40px','width':'120px','border-radius':'10px'}),
                                                                dbc.Modal(
                                                                    [
                                                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                                        dbc.ModalBody(id = "modal-body8",style = {'background-color':'rgb(20, 33, 54)'})
                                                                    ],id="modal8",is_open=False)
                                                                ],width = {'size':9,'offset':2})
                                                        ])
                                                
                                                ],width = {'size':3})
                                            ])
                                        
                                        ],style = {'height':'400px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white'})
                                    
                                    
                                    ],width = {'size':12})
                                ]),
                            html.Br()
                            
                            ]
                        
                elif url_ == '/ele_profile/dmodel':
                    
                    output = [
                        
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                        html.Iframe(id = 'map_for_profile',height = '100%',width = '100%',style = {'border-radius':'10px','border-style':'ridge'})
                                        ],style = {'width':'980px','height':'300px','border-style':'ridge','border-radius':'10px'})
                                ],width = {'size':12})
                            ]),
                        html.Br(),
                        nav,
                        html.Br(),
                        dbc.Row([
                            
                            dbc.Col([
                                
                                dbc.Card([
                                    
                                    dbc.Row([
                                        
                                        dbc.Col([
                                            
                                            dbc.Row([
                                                dbc.Col([
                                                    
                                                    html.Div([
                                                            html.Iframe(id = 'map_model',height = '100%',width = '100%')
                                                            ],style = {'height':'398px','width':'640px'})
                                                    
                                                    ],width = {'size':12})
                                                ])
                                            
                                            ],width = {'size':9}),
                                        dbc.Col([
                                            
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.RadioItems(id = 'distance_model',value = 'straight',options = [{'label':'straight','value':'straight'},{'label':'slope','value':'slope'}],style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white','width':'190px'}),
                                                        html.Br(),
                                                        dcc.Input(id = 'startlB',placeholder = 'start lat',value = bt.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'startl2B',placeholder = 'start lng',value = bt.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'endlB',placeholder = 'end lat',value = zomba.lat,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        dcc.Input(id = 'endl2B',placeholder = 'end lng',value = zomba.lng,style = {'border-radius':'10px','text-align':'center','background-color':'rgb(69, 205, 230)','color':'white'}),
                                                        html.Br(),
                                                        html.Br(),
                                                        html.Br(),
                                                        dbc.Row([
                                                            dbc.Col([
                                                                
                                                                dbc.Button(id = 'simulate3',n_clicks = 0,children = html.P([html.I(className = "fa-solid fa-compass",style = {'color':'peachpuff'}),'  Simulate']),style = {'height':'40px','width':'120px','border-radius':'10px'}),
                                                                dbc.Modal(
                                                                    [
                                                                        dbc.ModalHeader(children = dbc.ModalTitle("Message"),style = {'background-color':'rgb(20, 33, 54)'}),
                                                                        dbc.ModalBody(id = "modal-body9",style = {'background-color':'rgb(20, 33, 54)'})
                                                                    ],id="modal9",is_open=False)
                                                                ],width = {'size':9,'offset':2})
                                                        ])
                                            
                                            ],width = {'size':3})
                                        
                                        ])
                                    
                                    ],style = {'height':'400px','width':'980px','background-color':'rgb(20, 33, 54)','border-color':'white'})
                                
                                ],width = {'size':12})
                            ]),
                        html.Br()
                        
                        ]
                
                    
            return output
        
        # exception contents
        except Exception:
            return [
                    
                    dbc.Row([
                        dbc.Col([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            dbc.Card([
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.H5(['Oops, invalid url or slow internet connection,Try again'],style = {'text-align':'center','font-family':'forte','color':'rgb(193,224,227)'})
                                ],style = {'height':'250px','width':'600px','background-color':'red','border-color':'white','border-radius':'20px',"background-image": "url('https://images.unsplash.com/photo-1597773150796-e5c14ebecbf5?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZGFyayUyMGJsdWV8ZW58MHx8MHx8&w=1000&q=80')",'background-size':'cover','background-position':'center'})
                            ],width = {'size':6,'offset':4})
                        ],style = {'position':'fixed','height':'auto'})
                
                ]
     
    # creating the map object
    def map_data_(btlat,btlng):
        
        map_data = folium.Map(location = [btlat,btlng],zoom_start = 8,control_scale = True)
        folium.TileLayer(tiles = 'Stamen Terrain').add_to(map_data)
        folium.TileLayer(tiles = 'Stamen Toner').add_to(map_data)
        folium.TileLayer(tiles = 'cartodbdark_matter').add_to(map_data)
        folium.TileLayer(tiles = 'cartodbpositron').add_to(map_data)
        folium.TileLayer(tiles = 'cartodbpositron').add_to(map_data)
        folium.TileLayer(tiles = 'stamenwatercolor').add_to(map_data)
        folium.TileLayer(
            tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr = 'Esri',
            name = 'Esri Satellite',
            overlay = False,
            control = True
            ).add_to(map_data)
        
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite",
            control=True,
        ).add_to(map_data)
            
        folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attr="Google",
                name="Google Maps",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
                attr="Google",
                name="Google Terrain",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
                attr="Google",
                name="Google Satellite 2",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Ocean",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Standard",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Terrain",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Transportation",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Topo World",
                control=True,
            ).add_to(map_data)
            
        folium.TileLayer(
                tiles="http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri National Geographic",
                control=True,
                ).add_to(map_data)
         
        folium.TileLayer(
                tiles="https://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
                attr="Esri",
                name="Esri Shaded Relief",
                control=True,
                ).add_to(map_data)
        
        folium.LayerControl().add_to(map_data)
        
        return map_data
    
    # returns the map for geocoding page
    @app.callback(Output('geocoding_map','srcDoc'),State('place_name','value'),Input('map_search4','n_clicks'))
    def coding_map(name,n):
        
        place = geocoder.osm(name)
        
        lat = place.lat
        lng = place.lng
        
        map_data = map_data_(lat,lng)
        
        draw = plugins.Draw()
        map_data.add_child(draw)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        measure = plugins.MeasureControl()
        map_data.add_child(measure)
        
        locate = plugins.LocateControl()
        map_data.add_child(locate)
        
        folium.Marker(location = [lat,lng],popup = 'Latitude : {}'.format(lat) + '\n' + '\n' + 'Longtude : {}'.format(lng)).add_to(map_data)
        
        folium.LatLngPopup().add_to(map_data)
        
        fig = Figure()
        
        fig.add_child(map_data)
        
        fig.save('routes.html')
        
        return open('routes.html','r').read()
    
    # returns the map for elevation page
    @app.callback(Output('elevation_map','srcDoc'),[State('latitude_map_type3','value'),State('longtude_map_type3','value')],Input('map_search3','n_clicks'))
    def elevate_mapp(lat,lng,n):
        
        lat = float(lat)
        lng = float(lng)
        
        map_data = map_data_(lat,lng)
        
        draw = plugins.Draw()
        map_data.add_child(draw)
        
        measure = plugins.MeasureControl()
        map_data.add_child(measure)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        locate = plugins.LocateControl()
        map_data.add_child(locate)
        
        folium.LatLngPopup().add_to(map_data)
        
        client = openrouteservice.Client(key='key')
        
        coordinate = [lng,lat]
    
        elevation = client.elevation_point(
        format_in='point',
        format_out='point',
        geometry=coordinate
        )
    
        elevate = elevation['geometry'][2]
        
        folium.Marker(location = [lat,lng],
                      popup = 'Elevation Point',
                      tooltip = str(elevate) + ' meters').add_to(map_data)
        
        fig = Figure()
        
        fig.add_child(map_data)
        
        fig.save('routes.html')
        
        return open('routes.html','r').read()
    
    # returns  map for distance page
    @app.callback(Output('straight_line_map','srcDoc'),[State('latitude_origin','value'),State('longtude_origin','value'),State('destination_latitude','value'),State('destination_longtude','value'),State('route_profile','value'),State('path_type','value')],Input('change_path_type','n_clicks'))
    def distance_map_(ol1,ol2,dl1,dl2,profile_,path,n):
        
        ol1 = float(ol1)
        ol2 = float(ol2)
        dl1 = float(dl1)
        dl2 = float(dl2)
        
        fig = Figure()
        
        map_data = map_data_(ol1,ol2)
        
        draw = plugins.Draw()
        map_data.add_child(draw)
        
        measure = plugins.MeasureControl()
        map_data.add_child(measure)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        locate = plugins.LocateControl()
        map_data.add_child(locate)
        
        folium.LatLngPopup().add_to(map_data)
        
        folium.Marker(location = [ol1,ol2],
                          popup = '<h5 style = "color:blue"> Lat : {}</h5> <br> <h5 style = "color:blue"> Lng : {}</h5>'.format(ol1,ol2),
                          tooltip = 'Click for coordinate').add_to(map_data)
        
        folium.Marker(location = [dl1,dl2],
                          popup = '<h5 style = "color:blue"> Lat : {}</h5> <br> <h5 style = "color:blue"> Lng : {}</h5>'.format(dl1,dl2),
                          tooltip = 'Click for coordinate').add_to(map_data)
       
        loc = [[ol1,ol2],[dl1,dl2]]
        
        if path == 'straight line':
            
            distance_straight_line = distance([ol1,ol2],[dl1,dl2]).km
            
            plugins.AntPath(locations = loc,popup = '<p style = "color:red;">Distance is {} Km</p>'.format(distance_straight_line)).add_to(map_data)
            #folium.Popup("<p>Distance not known</p>").add_to(map_data)
             
            fig.add_child(map_data)
            
            fig.save('routes.html')
         
            output = open('routes.html','r').read()
            
        elif path == 'route':
            
            client = openrouteservice.Client(key='key')
    
            coordinates = [[ol2,ol1], [dl2,dl1]]
    
            route_ = client.directions(
                coordinates=coordinates,
                profile=profile_,
                format='geojson',
                validate=False
                )
            
            res = client.directions(coordinates,profile = profile_)
            
            distance_txt = "<h4> <b>Distance :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
            duration_txt = "<h4> <b>Duration :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"
            
            plugins.AntPath(locations=[list(reversed(coord)) for coord in route_['features'][0]['geometry']['coordinates']],popup = distance_txt + duration_txt).add_to(map_data)
            
            fig.add_child(map_data)
            
            fig.save('routes.html')
            
            output = open('routes.html','r').read()
            
        return output
        
     # returns map for edit map page   
    @app.callback(Output('map_type_map2','srcDoc'),[State('latitude_map_type2','value'),State('longtude_map_type2','value')],Input('map_search2','n_clicks'))
    def map_explore(lat_,lng_,n):
        
        lat_ = float(lat_)
        lng_ = float(lng_)
        
        map_data = map_data_(lat_,lng_)
        
        draw = plugins.Draw()
        map_data.add_child(draw)
        
        measure = plugins.MeasureControl()
        map_data.add_child(measure)
        
        locate = plugins.LocateControl()
        map_data.add_child(locate)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        folium.LatLngPopup().add_to(map_data)
        
        fig = Figure()   
             
        fig.add_child(map_data)
            
        fig.save('routes.html')
         
        return open('routes.html','r').read()
    
    # returns map for homescreen page
    @app.callback(Output('map_type_map','srcDoc'),[State('latitude_map_type','value'),State('longtude_map_type','value')],Input('map_search','n_clicks'))
    def draw_map(lat_,lng_,n):
        
        lat_ = float(lat_)
        lng_ = float(lng_)
        
        map_data = map_data_(lat_,lng_)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        fig = Figure()   
             
        fig.add_child(map_data)
            
        fig.save('routes.html')
         
        return open('routes.html','r').read()
    
    # returns map for elevation profile page
    @app.callback(Output('map_for_profile','srcDoc'),Input('url','pathname'))
    def map_for_profile(url_):
        
        
        map_data = map_data_(bt.lat,bt.lng)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        folium.LatLngPopup().add_to(map_data)
        
        fig = Figure()   
             
        fig.add_child(map_data)
            
        fig.save('routes.html')
         
        return open('routes.html','r').read()

    # returns terrain 3d model
    @app.callback(Output('terrain','figure'),[State('min_lat','value'),State('max_lat','value'),State('min_lng','value'),State('max_lng','value'),State('points','value')],Input('simulate','n_clicks'))
    def terrain_simulator(min_lat,max_lat,min_lng,max_lng,points,n):
        
        df = create_dataset(float(min_lat),float(max_lat),float(min_lng),float(max_lng),int(points))
        
        d_ar=[{}]*len(list(df.Lat.values))
        for i in range(len(list(df.Lat.values))):
            d_ar[i]={"latitude":list(df.Lat.values)[i],"longitude":list(df.Lng.values)[i]}
        location={"locations":d_ar}
        json_data=json.dumps(location,skipkeys=int).encode('utf8')

        url="https://api.open-elevation.com/api/v1/lookup"
        response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
        fp=urllib.request.urlopen(response)
        
        res_byte=fp.read()
        res_str=res_byte.decode("utf8")
        js_str=json.loads(res_str)
        
        fp.close()

        response_len=len(js_str['results'])
        elev_list=[]
        
        for j in range(response_len):
            elev_list.append(js_str['results'][j]['elevation'])
            
        df['elevation_point'] = elev_list
        
        df.to_csv('terrain2.csv',index = False)
        
        
        #READING AND PARSING THE DATA
        file=open('terrain2.csv','r')
        lines=file.readlines()
        n_line=len(lines)
        x=[]
        y=[]
        z=[]
        
        #3D TERRAIN MODELLING
        #CREATED BY: IDEAGORA GEOMATICS
        #ORIGINAL SOURCE CODE AT WWW.GEODOSE.COM


        for i in range(1,n_line):
            split_line=lines[i].split(",")
            x.append(float(split_line[0].rstrip()))
            y.append(float(split_line[1].rstrip()))
            z.append(float(split_line[2].rstrip()))
    
        #DISTANCE FUNCTION
        def distance(x1,y1,x2,y2):
            d=np.sqrt((x1-x2)**2+(y1-y2)**2)
            return d

        #CREATING IDW FUNCTION
        def idw_npoint(xz,yz,n_point,p):
            r=10 #block radius iteration distance
            nf=0
            while nf<=n_point: #will stop when np reaching at least n_point
                x_block=[]
                y_block=[]
                z_block=[]
                r +=10 # add 10 unit each iteration
                xr_min=xz-r
                xr_max=xz+r
                yr_min=yz-r
                yr_max=yz+r
                for i in range(len(x)):
                    # condition to test if a point is within the block
                    if ((x[i]>=xr_min and x[i]<=xr_max) and (y[i]>=yr_min and y[i]<=yr_max)):
                        x_block.append(x[i])
                        y_block.append(y[i])
                        z_block.append(z[i])
                nf=len(x_block) #calculate number of point in the block
    
                #calculate weight based on distance and p value
            w_list=[]
            for j in range(len(x_block)):
                d=distance(xz,yz,x_block[j],y_block[j])
                if d>0:
                    w=1/(d**p)
                    w_list.append(w)
                else:
                    w_list.append(0) #if meet this condition, it means d<=0, weight is set to 0
    
            #check if there is 0 in weight list
            w_check=0 in w_list
            if w_check==True:
                idx=w_list.index(0) # find index for weight=0
                z_idw=z_block[idx] # set the value to the current sample value
            else:
                wt=np.transpose(w_list)
                z_idw=np.dot(z_block,wt)/sum(w_list) # idw calculation using dot product
            return z_idw

        # POPULATE INTERPOLATION POINTS
        n=100 #number of interpolation point for x and y axis
        x_min=min(x)
        x_max=max(x)
        y_min=min(y)
        y_max=max(y)
        w=x_max-x_min #width
        h=y_max-y_min #length
        wn=w/n #x interval
        hn=h/n #y interval

        #list to store interpolation point and elevation
        y_init=y_min
        x_init=x_min
        x_idw_list=[]
        y_idw_list=[]
        z_head=[]
        for i in range(n):
            xz=x_init+wn*i
            yz=y_init+hn*i
            y_idw_list.append(yz)
            x_idw_list.append(xz)
            z_idw_list=[]
            for j in range(n):
                xz=x_init+wn*j
                z_idw=idw_npoint(xz,yz,5,1.5) #min. point=5, p=1.5
                z_idw_list.append(z_idw)
            z_head.append(z_idw_list)
                
        noaxis=dict(showbackground=True,
                                backgroundcolor='rgb(20, 33, 54)',
                                showline=False,
                                zeroline=False,
                                showgrid=False,
                                showticklabels=False,
                                title='')
                
        layout = go.Layout(
                            title= {"text":"Terrain 3D",'x':0.5,'xanchor':'center'},
                            font = {'color':'white'},
                            width=640, height=394,
                            paper_bgcolor = 'rgb(20, 33, 54)',
                            scene=dict(
                                    xaxis=dict(noaxis), yaxis=dict(noaxis), zaxis=dict(noaxis)
        #                      aspectratio=dict( x=1, y=2, z=0.5)
                         )
                            )

        # CREATING 3D TERRAIN
        fig=go.Figure(layout = layout)
        fig.add_trace(go.Surface(z=z_head,x=x_idw_list,y=y_idw_list))
        fig.update_layout(scene=dict(aspectratio=dict(x=2, y=2, z=0.5),xaxis = dict(range=[x_min,x_max],),yaxis = dict(range=[y_min,y_max])))
    
        
        #figure = dict(data = mesh,layout = layout)

        return fig
        
     # returns terrain 2d model   
    @app.callback(Output('terrain2d','figure'),[State('points2','value'),State('startl','value'),State('startl2','value'),State('endl','value'),State('endl2','value')],Input('simulate22','n_clicks'))
    def terrain_simulator2d(p,sl,sl2,el,el2,n):
        

        P1=[float(sl),float(sl2)]
        P2=[float(el),float(el2)]

        s= int(p)
        interval_lat=(P2[0]-P1[0])/s 
        interval_lon=(P2[1]-P1[1])/s 

        lat0=P1[0]
        lon0=P1[1]

        lat_list=[lat0]
        lon_list=[lon0]

        for i in range(s):
            lat_step=lat0+interval_lat
            lon_step=lon0+interval_lon
            lon0=lon_step
            lat0=lat_step
            lat_list.append(lat_step)
            lon_list.append(lon_step)
            
        
        def haversine(lat1,lon1,lat2,lon2):
            lat1_rad=math.radians(lat1)
            lat2_rad=math.radians(lat2)
            lon1_rad=math.radians(lon1)
            lon2_rad=math.radians(lon2)
            delta_lat=lat2_rad-lat1_rad
            delta_lon=lon2_rad-lon1_rad
            a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
            d=2*6371000*math.asin(a)
            return d

        d_list=[]
        for j in range(len(lat_list)):
            lat_p=lat_list[j]
            lon_p=lon_list[j]
            dp=haversine(lat0,lon0,lat_p,lon_p)/1000 
            d_list.append(dp)
            
        d_list_rev=d_list[::-1] 
        
        d_ar=[{}]*len(lat_list)
        for i in range(len(lat_list)):
            d_ar[i]={"latitude":lat_list[i],"longitude":lon_list[i]}
        location={"locations":d_ar}
        json_data=json.dumps(location,skipkeys=int).encode('utf8')
 
        url="https://api.open-elevation.com/api/v1/lookup"
        response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
        fp=urllib.request.urlopen(response)
        
        res_byte=fp.read()
        res_str=res_byte.decode("utf8")
        js_str=json.loads(res_str)
        fp.close()

        response_len=len(js_str['results'])
        elev_list=[]
        for j in range(response_len):
            elev_list.append(js_str['results'][j]['elevation'])

        mean_elev=round((sum(elev_list)/len(elev_list)),3)
        min_elev=min(elev_list)
        max_elev=max(elev_list)
        
        
        noaxis=dict(showbackground=True,
                        backgroundcolor='rgb(20, 33, 54)',
                        showline=False,
                        zeroline=False,
                        showgrid=False,
                        showticklabels=False,
                        title='')
            
        layout = go.Layout(
                    title= {'text' : 'Terrain 2D','x' : 0.5,'xanchor' : 'center'},
                    xaxis = dict(title = 'Distance (km)',showgrid = False),
                    yaxis = dict(title = "Elevation Point",showgrid = False),
                    font = {'color':'white'},
                    width=640, height=394,
                    paper_bgcolor = 'rgb(20, 33, 54)',
                    plot_bgcolor = 'rgb(20,33,54)',
                    scene=dict(
                            xaxis=dict(noaxis), yaxis=dict(noaxis), zaxis=dict(noaxis)

                 )
                    )
    
            
        sca = [go.Scatter(x = d_list_rev,y = elev_list,name = 'Elevation'),
               go.Scatter(x = d_list_rev,y = np.repeat(mean_elev,len(elev_list)),name = 'Mean Elevation'),
               go.Scatter(x = d_list_rev,y = np.repeat(min_elev,len(elev_list)),name = 'Minimum Elevation'),
               go.Scatter(x = d_list_rev,y = np.repeat(max_elev,len(elev_list)),name = 'Maximum Elevation')]

        figure = dict(data = sca,layout = layout)
        
        return figure
    
    # returns distance model
    @app.callback(Output('map_model','srcDoc'),[State('distance_model','value'),State('startlB','value'),State('startl2B','value'),State('endlB','value'),State('endl2B','value')],Input('simulate3','n_clicks'))
    def distance_model(model,sl,sl2,el,el2,n):
        
        lat_ = float(sl)
        lng_ = float(sl2)
        
        lat_2 = float(el)
        lng_2 = float(el2)
        
        client = openrouteservice.Client(key='key')
        
        coordinates = [[lng_,lat_], [lng_2,lat_2]]

        elevation = client.elevation_line(
            format_in='polyline',  # other options: geojson, encodedpolyline
            format_out='geojson',
            geometry=coordinates,
            )

        df = pd.DataFrame(elevation['geometry']['coordinates'])
        df.columns = ['Lng','Lat','elevation']
        
        distance_straight_line = distance([lat_,lng_],[lat_2,lng_2]).km
        
        loc = [[lat_,lng_],[lat_2,lng_2]]
        
        map_data = map_data_(lat_,lng_)
        
        for i in range(len(df.index)):
            
            folium.Marker(location = [df.Lat[i],df.Lng[i]],
                          popup = '<h5 style = "color:blue"> Lat : {}</h5> <br> <h5 style = "color:blue"> Lng : {}</h5>'.format(df.Lat[i],df.Lng[i]),
                          tooltip = str(df.elevation[i]) + ' meters').add_to(map_data)
        
        draw = plugins.Draw()
        map_data.add_child(draw)
        
        measure = plugins.MeasureControl()
        map_data.add_child(measure)
        
        locate = plugins.LocateControl()
        map_data.add_child(locate)
        
        minimap = plugins.MiniMap(toggle_display=True)
        map_data.add_child(minimap)
        
        folium.LatLngPopup().add_to(map_data)
        
        fig = Figure()
        
        if model == 'straight':
            
            folium.PolyLine(locations = loc,popup = '<p style = "color:red;">Distance is {} Km</p>'.format(distance_straight_line)).add_to(map_data)
        
            fig.add_child(map_data)
            
            fig.save('routes2.html')
         
            return open('routes2.html','r').read()
        
        elif model == 'slope':
            
            height = abs(df.elevation[0] - df.elevation[1])
            base_length = distance_straight_line * 1000
            
            slope = math.hypot(height,base_length)
            
            folium.PolyLine(locations = loc,popup = '<p style = "color:red;">Slope is {} m</p>'.format(slope)).add_to(map_data)
        
            fig.add_child(map_data)
            
            fig.save('routes2.html')
         
            return open('routes2.html','r').read()
    
    # converts eastings and northings to latitude and longtude
    @app.callback([Output('tolat','value'),Output('tolon','value')],[State('Easting','value'),State('Northing','value'),State('Zone Number','value'),State('Zone Letter','value')],Input('calcu','n_clicks'))
    def to_latlon(east,north,zn,zl,n):
        
        coordinates = utm.to_latlon(float(east),float(north),float(zn),zl)
        
        return coordinates[0],coordinates[1]
    
    # converts latitude and longtude to eastings and northings
    @app.callback([Output('east2','value'),Output('north2','value'),Output('Zone Number2','value'),Output('Zone Letter2','value')],[State('lat_2','value'),State('lon_2','value')],Input('calcu2','n_clicks'))
    def from_latlon(lat,lng,n):
        
        coordinates = utm.from_latlon(float(lat),float(lng))
        
        return coordinates[0],coordinates[1],coordinates[2],coordinates[3]
        
     # modal for explore map page to validity of data
    @app.callback(
        [Output("modal2", "is_open"),Output('modal-body2','children')],
        [State('latitude_map_type','value'),State('longtude_map_type','value'),State("modal2", "is_open")],
        [Input("map_search", "n_clicks")],
    )
    def toggle_modal2(lat,lng,is_open,n1):
        
        try:
            
            if n1:
            
                lat = float(lat) # not to be used
                lng = float(lng) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
            
     # modal for edit map page to validity of data
    @app.callback(
        [Output("modal3", "is_open"),Output('modal-body3','children')],
        [State('latitude_map_type2','value'),State('longtude_map_type2','value'),State("modal3", "is_open")],
        [Input("map_search2", "n_clicks")],
    )
    def toggle_modal3(lat,lng,is_open,n1):
        
        try:
            
            if n1:
            
                lat = float(lat) # not to be used
                lng = float(lng) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
            
      # modal for distances page to validity of data       
    @app.callback(
        [Output("modal4", "is_open"),Output('modal-body4','children')],
        [State('latitude_origin','value'),State('longtude_origin','value'),State('destination_latitude','value'),State('destination_longtude','value'),State('route_profile','value'),State('path_type','value'),State("modal4", "is_open")],
        [Input("change_path_type", "n_clicks")],
    )
    def toggle_modal4(ol1,ol2,dl1,dl2,profile_,path,is_open,n1):
        
        try:
            
            if n1:
            
                ol1 = float(ol1)
                ol2 = float(ol2)
                dl1 = float(dl1)
                dl2 = float(dl2)
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body    
            
     # modal for elevation page to validity of data        
    @app.callback(
        [Output("modal5", "is_open"),Output('modal-body5','children')],
        [State('latitude_map_type3','value'),State('longtude_map_type3','value'),State("modal5", "is_open")],
        [Input("map_search3", "n_clicks")],
    )
    def toggle_modal5(lat,lng,is_open,n1):
        
        try:
            
            if n1:
            
                lat = float(lat) # not to be used
                lng = float(lng) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
     
     # modal for geocoding page to validity of data
    @app.callback(
        [Output("modal6", "is_open"),Output('modal-body6','children')],
        [State('place_name','value'),State("modal6", "is_open")],
        [Input("map_search4", "n_clicks")],
    )
    def toggle_modal6(name,is_open,n1):
        
        try:
            
            if n1:
            
                name = float(name) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Located'
            
                return not is_open,body
     
     # modal for 3D model page to validity of data
    @app.callback(
        [Output("modal7", "is_open"),Output('modal-body7','children')],
        [State('min_lat','value'),State('max_lat','value'),State('min_lng','value'),State('max_lng','value'),State('points','value'),State("modal7", "is_open")],
        [Input("simulate", "n_clicks")],
    )
    def toggle_modal7(min_lat,max_lat,min_lng,max_lng,points,is_open,n1):
        
        try:
            
            if n1:
            
                min_lat = float(min_lat) # not to be used
                max_lat = float(max_lat) # not to be used
                min_lng = float(min_lng) # not to be used
                max_lng = float(max_lng) # not to be used
                points = float(points) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
     
     # modal for 2D model page to validity of data
    @app.callback(
        [Output("modal8", "is_open"),Output('modal-body8','children')],
        [State('points2','value'),State('startl','value'),State('startl2','value'),State('endl','value'),State('endl2','value'),State("modal8", "is_open")],
        [Input("simulate22", "n_clicks")],
    )
    def toggle_modal8(p,sl,sl2,el,el2,is_open,n1):
        
        try:
            
            if n1:
            
                sl = float(sl) # not to be used
                sl2 = float(sl2) # not to be used
                el = float(el) # not to be used
                el2 = float(el2) # not to be used
                p = float(p) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
      
     # modal for distance model page to validity of data
    @app.callback(
        [Output("modal9", "is_open"),Output('modal-body9','children')],
        [State('startlB','value'),State('startl2B','value'),State('endlB','value'),State('endl2B','value'),State("modal9", "is_open")],
        [Input("simulate3", "n_clicks")],
    )
    def toggle_modal9(sl,sl2,el,el2,is_open,n1):
        
        try:
            
            if n1:
            
                sl = float(sl) # not to be used
                sl2 = float(sl2) # not to be used
                el = float(el) # not to be used
                el2 = float(el2) # not to be used
                
                body = 'Located'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
            
      # modal for calculator(to lat/lon) page to validity of data       
    @app.callback(
        [Output("modalc", "is_open"),Output('modal-bodyc','children')],
        [State('Easting','value'),State('Northing','value'),State('Zone Number','value'),State("modalc", "is_open")],
        [Input("calcu", "n_clicks")],
    )
    def toggle_modalc(east,north,zn,is_open,n1):
        
        try:
            
            if n1:
            
                east = float(east) # not to be used
                north = float(north) # not to be used
                zn = float(zn) # not to be used
                
                body = 'Computed'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
     
     # modal for calculator(to east/north) page to validity of data
    @app.callback(
        [Output("modalc2", "is_open"),Output('modal-bodyc2','children')],
        [State('lat_2','value'),State('lon_2','value'),State("modalc2", "is_open")],
        [Input("calcu2", "n_clicks")],
    )
    def toggle_modalc2(lat,lon,is_open,n1):
        
        try:
            
            if n1:
            
                lat = float(lat) # not to be used
                lon = float(lon) # not to be used
                
                body = 'Computed'
            
                return not is_open,body
        
            body = ''
        
            return is_open,body
        
        except Exception:
            
            if n1:
            
                body = 'Enter correct details'
            
                return not is_open,body
    
    
    return app
