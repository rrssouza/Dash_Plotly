from dash import Dash, dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url

#>Bibliotecas
        #>pip install pandas==2.0.3 - ok
        #>pip install dash==2.11.1 - ok
        #>pip install plotly==5.16.0 - ok
        #>pip install dash-bootstrap-components==1.4.1 - ok
        #>pip install dash-bootstrap-templates==1.0.8 - ok
        #>pip install numpy==1.25.2 - ok

dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css")

# variável para o tamanho do dbc.Card()
tab_card = {'height': '100%'}

# variável de temas bootstrap
themes_options = [
    {'label': 'FLATLY', 'value': dbc.themes.FLATLY},
    {'label': 'DARKLY', 'value': dbc.themes.DARKLY},
    {'label': 'QUARTZ', 'value': dbc.themes.QUARTZ}
]

# Variável de configurar o gráfico
# https://dash.plotly.com/dash-core-components/graph
# displayModeBar (um valor igual a: true, false ou 'hover'; opcional): Exibe a barra de modo (True, False ou 'hover')
# showTips (boolean; opcional): Novos usuários veem algumas dicas sobre interatividade.
config_graph = {"displayModeBar": False, "showTips": False}

# Variável de configuração principal de layout dos gráficos
main_config = {
    "hovermode": "x unified",
    "legend":{"yanchor": "top", 
              "y": 0.6, "xanchor": "left", 
              "x": 0.0,
              "title": {"text": None},
              "font": {"color": "white"},
              "bgcolor": "rgba(0,0,0,0.5)"},
    "margin":{"l": 10, "r": 10, "t": 10, "b": 10}

}

# Variável mês
select_month = [
    {"label": "Ano", "value": 0},
    {"label": "Jan", "value": 1},
    {"label": "Fev", "value": 2},
    {"label": "Mar", "value": 3},
    {"label": "Abr", "value": 4},
    {"label": "Mai", "value": 5},
    {"label": "Jun", "value": 6},
    {"label": "Jul", "value": 7},
    {"label": "Ago", "value": 8},
    {"label": "Set", "value": 9},
    {"label": "Out", "value": 10},
    {"label": "Nov", "value": 11},
    {"label": "Dez", "value": 12}
]

# Variável equipes
options_team = [
    {"label": "Equipes", "value": "Equipes"},
    {"label": "Equipe 1", "value": "Equipe 1"},
    {"label": "Equipe 2", "value": "Equipe 2"},
    {"label": "Equipe 3", "value": "Equipe 3"},
    {"label": "Equipe 4", "value": "Equipe 4"}
]



# inicialize o app com os temas de bootstrap e variável dbc_css
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# layout do app
app.layout = dbc.Container(children=[
    
    #Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Sales Analytcs')
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale', style={'font-size': '300%'})
                        ], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeChangerAIO(aio_id='theme', radio_props={'value': dbc.themes.DARKLY, 'options': themes_options}),

                            html.Legend('Academy')
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o site", href="https://google.com/", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ],sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Top Consultores por Equipe')
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(config=config_graph) ##################
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(config=config_graph) ###################
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(id="box-month", options=select_month, value=0,inline=True),
                            html.H1(id='escolhames', style={"text-align": "center", "margin-top": "30px"})
                        ])
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    #Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            #1ª indicator
                            dcc.Graph(config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            #2ª indicator
                            dcc.Graph(config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([dbc.Col([
                dbc.Card([
                    dcc.Graph(config=config_graph)
                ], style=tab_card)
            ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Valor Por Propaganda Mensal'),
                    dcc.Graph(config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([dbc.CardBody([
                dcc.Graph(config=config_graph)
            ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escola a Equipe'),
                    dbc.RadioItems(id="radio_team", options=options_team, value="Equipes", inline=True),
                    html.H1(id="escolhaequipe", style={"text-align": "center", "margin-top": "60px"})
                ])
            ], style=tab_card)
        ], sm=12, lg=2)
    ], className='g-2 my-auto', style={'margin-top': '7px'})
], fluid=True, className="dbc")


if __name__ == '__main__':
    app.run(debug=True)