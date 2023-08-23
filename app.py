from dash import Dash, dcc, html, Output, Input, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url



# dataset
df = pd.read_csv("data.csv")

df['Mês'] = df['Mês'].replace(['Jan'], 1)
df['Mês'] = df['Mês'].replace(['Fev'], 2)
df['Mês'] = df['Mês'].replace(['Mar'], 3)
df['Mês'] = df['Mês'].replace(['Abr'], 4)
df['Mês'] = df['Mês'].replace(['Mai'], 5)
df['Mês'] = df['Mês'].replace(['Jun'], 6)
df['Mês'] = df['Mês'].replace(['Jul'], 7)
df['Mês'] = df['Mês'].replace(['Ago'], 8)
df['Mês'] = df['Mês'].replace(['Set'], 9)
df['Mês'] = df['Mês'].replace(['Out'], 10)
df['Mês'] = df['Mês'].replace(['Nov'], 11)
df['Mês'] = df['Mês'].replace(['Dez'], 12)



df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')

df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1

df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0


df['Chamadas Realizadas'] = df['Chamadas Realizadas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)
df['Valor Pago'] = df['Valor Pago'].astype(int)
df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)


dbc_css = ("https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.1/dbc.min.css")


tab_card = {'height': '100%'}

themes_options = [
    {'label': 'FLATLY', 'value': dbc.themes.FLATLY},
    {'label': 'DARKLY', 'value': dbc.themes.DARKLY},
    {'label': 'QUARTZ', 'value': dbc.themes.QUARTZ}
]

config_graph = {"displayModeBar": False, "showTips": False}


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


options_team = [
    {"label": "Equipes", "value": "Equipes"},
    {"label": "Equipe 1", "value": "Equipe 1"},
    {"label": "Equipe 2", "value": "Equipe 2"},
    {"label": "Equipe 3", "value": "Equipe 3"},
    {"label": "Equipe 4", "value": "Equipe 4"}
]


def month_filter(month):
    if month == 0:
        mask = df['Mês'].isin(df['Mês'].unique())
    else:
        mask = df['Mês'].isin([month])
    return mask


def team_filter(team):
    if team == 'Equipes':
        mask = df['Equipe'].isin(df['Equipe'].unique())
    else:
        mask = df['Equipe'].isin([team])
    return mask




def convert_text(month):
    match month:
        case 0:
            x = 'Ano'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x



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
                            dcc.Graph(id='graph1', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', config=config_graph)
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
                            dcc.Graph(id='graph3', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', config=config_graph)
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
                            dcc.Graph(id='graph7', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            #2ª indicator
                            dcc.Graph(id='graph8', config=config_graph)
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([dbc.Col([
                dbc.Card([
                    dcc.Graph(id='graph5', config=config_graph)
                ], style=tab_card)
            ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                dcc.Graph(id='graph15', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    #Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Valor Por Propaganda Mensal'),
                    dcc.Graph(id='graph10', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([dbc.CardBody([
                dcc.Graph(id='graph14', config=config_graph)
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


@callback(
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='escolhames', component_property='children'),
    Input(component_id='box-month', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph1(month, theme):
    
    mask = month_filter(month)
    df_1 = df.loc[mask]
    
    df_1 = df_1.groupby(['Equipe', 'Consultor'])['Valor Pago'].sum()
    df_1 = df_1.sort_values(ascending=False)
    df_1 = df_1.groupby('Equipe').head(1).reset_index()

    fig2 = go.Figure(go.Pie(labels=df_1['Consultor'] + ' - ' + df_1['Equipe'], values=df_1['Valor Pago'], hole=.7))

    fig1 = go.Figure(go.Bar(x=df_1['Consultor'], y=df_1['Valor Pago'], textposition='auto', text=df_1['Valor Pago']))

    fig1.update_layout(main_config, height=200,
                       template=template_from_url(theme))
    fig2.update_layout(main_config, height=200,
                       template=template_from_url(theme))

    select = html.H1(convert_text(month))

    return fig1, fig2, select



@callback(
    Output(component_id='graph3', component_property='figure'),
    Output(component_id='escolhaequipe', component_property='children'),
    Input(component_id='radio_team', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph3(team, theme):
    
    mask = team_filter(team)
    df_3 = df.loc[mask]
    
    df_3 = df_3.groupby('Dia')['Chamadas Realizadas'].sum().reset_index()

    fig3 = go.Figure(
                 go.Scatter(x=df_3['Dia'],
                            y=df_3['Chamadas Realizadas'],
                            mode='lines',
                            fill='tonexty'
                           ))
    fig3.add_annotation(text='Chamadas Médias por dia do Mês',
                    xref='paper',
                    yref='paper',
                    font=dict(size=17, color='gray'),
                    align='center',
                    bgcolor='rgba(0,0,0,0.8)',
                    x=0.50,
                    y=0.99,
                    showarrow=False
                   )
    fig3.add_annotation(text=f'Média:{round(df_3["Chamadas Realizadas"].mean(), 2)}',
                    xref='paper',
                    yref='paper',
                    font=dict(size=17, color='gray'), 
                    align='center', 
                    bgcolor='rgba(0,0,0,0.8)', 
                    x=0.50, 
                    y=0.79,
                    showarrow=False
                   )
    fig3.update_layout(main_config, height=180, template=template_from_url(theme))
    
    selequipe = html.H1((team))
    return fig3, selequipe


@callback(
    Output(component_id='graph4', component_property='figure'),
    Input(component_id='radio_team', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph4(team, theme):
    
    mask = team_filter(team)
    df_4 = df.loc[mask]
    
    df_4 = df_4.groupby('Mês')['Chamadas Realizadas'].sum().reset_index()
    
    fig4 = go.Figure(go.Scatter(
        y=df_4['Chamadas Realizadas'],
        x=df_4['Mês'],
        mode='lines',
        fill='tonexty'))

    fig4.add_annotation(text='Chamadas Médias Por Mês',
                        xref='paper',
                        yref='paper',
                        font=dict(size=17, color='gray'),
                        align='center',
                        bgcolor='rgba(0,0,0,0.8)',
                        x=0.05,
                        y=0.85,
                        showarrow=False)
    fig4.add_annotation(text=f"Média:{round(df_4['Chamadas Realizadas'].mean(), 2)}",
                        xref='paper',
                        yref='paper',
                        font=dict(size=17, color='gray'),
                        align='center',
                        bgcolor='rgba(0,0,0,0.8)',
                        x=0.05,
                        y=0.55,
                        showarrow=False
                        )
    fig4.update_layout(main_config, height=180,
                       template=template_from_url(theme))
    
    return fig4

 
@callback(
        Output(component_id='graph5', component_property='figure'),
        Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
    )
def graph5(theme):
    df5 = df.groupby(['Mês', 'Equipe'])['Valor Pago'].sum().reset_index()
    df5_group = df.groupby('Mês')['Valor Pago'].sum().reset_index()

    fig5 = px.line(df5, y='Valor Pago', x='Mês', color='Equipe')
    fig5.add_trace(go.Scatter(y=df5_group['Valor Pago'], x=df5_group['Mês'], mode='lines+markers',
                   fill='tonexty', name='Vendas Mensal', fillcolor='rgba(255, 0, 0, 0.2 )'))

    fig5.update_layout(main_config, height=190,
                       template=template_from_url(theme))
    return fig5
    

@callback(
    Output(component_id='graph7', component_property='figure'),
    Input(component_id='box-month', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph7(month, theme):
    
    mask = month_filter(month)
    df_7 = df.loc[mask]
    
    df_7 = df_7.groupby(['Consultor', 'Equipe'])['Valor Pago'].sum()
    df_7 = df_7.sort_values(ascending=False).reset_index()
    df_7['Part%'] = df_7['Valor Pago'] / df_7['Valor Pago'].sum() * 100
    df_7['Part%'] = df_7['Part%'].astype(int)
    df_7['Part%'] = df_7['Part%'].astype(float)

    fig7 = go.Figure()
    fig7.add_trace(
        go.Indicator(mode='number',
            value=df_7['Valor Pago'].iloc[0],
            title={"text": f"1ª <span style='font-size:100%'>{df_7['Consultor'].iloc[0]}</span> <span style='font-size100%'>{df_7['Equipe'].iloc[0]}</span><br><span style='font-size:0.9em'; color: blue>{df_7['Part%'].iloc[0]}% Part</span>"},
            number={'prefix': 'R$ '},
                                ))

    fig7.update_layout(main_config, height=180,
                       template=template_from_url(theme))
    fig7.update_layout({"margin": {"l": 0, "r": 0, "t": 20, "b": 0}})
    
    return fig7


@callback(
    Output(component_id='graph8', component_property='figure'),
    Input(component_id='box-month', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph(month,theme):
    
    mask = month_filter(month)
    df_8 = df.loc[mask]
    
    df_8 = df_8.groupby('Equipe')['Valor Pago'].sum()
    df_8 = df_8.sort_values(ascending=False).reset_index()
    df_8['Part%'] = df_8['Valor Pago'] / df_8['Valor Pago'].sum() * 100

    fig8 = go.Figure()
    fig8.add_trace(go.Indicator(mode='number+delta',
                                value=df_8['Valor Pago'].iloc[0],
                                title={"text": f"1ª <span style='font-size:100%'>{df_8['Equipe'].iloc[0]}</span><br>"},
                                number={'prefix': 'R$ '},
                                delta={'relative': True, 'valueformat': '.2%', 'reference': df_8['Valor Pago'].mean()}
                                ))
    fig8.update_layout(main_config, height=200,
                       template=template_from_url(theme))
    fig8.update_layout({"margin": {"l": 0, "r": 0, "t": 30, "b": 0}})
    
    return fig8
    

@callback(
    Output(component_id='graph15', component_property='figure'),
    Input(component_id='box-month', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph15(month, theme):
    
    mask = month_filter(month)
    df_15 = df.loc[mask]
    
    df_15 = df_15.groupby('Equipe')['Valor Pago'].sum().reset_index()
    df_15 = df_15.sort_values('Equipe', ascending=True)

    fig15 = go.Figure(go.Bar(y=df_15['Equipe'],
                             x=df_15['Valor Pago'],
                             orientation='h',
                             textposition='auto',
                             text=df_15['Valor Pago'],
                             insidetextfont=dict(family='Times', size=12)))

    fig15.update_layout(main_config, height=350,
                        template=template_from_url(theme))
    return fig15
    
 

@callback(
    Output(component_id='graph9', component_property='figure'),
    Input(component_id='box-month', component_property='value'),
    Input(component_id='radio_team', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph9(month, team, theme):
    
    mask = month_filter(month)
    df_9 = df.loc[mask]
    
    mask = team_filter(team)
    df_9 = df_9.loc[mask]
    
    df_9 = df_9.groupby('Meio de Propaganda')['Valor Pago'].sum().reset_index()
    
    
    fig9 = go.Figure()
    fig9.add_trace(
        go.Pie(labels=df_9['Meio de Propaganda'], values=df_9['Valor Pago'], hole=.7))

    fig9.update_layout(main_config, height=200,
                       template=template_from_url(theme))
    
    return fig9



@callback(
    Output(component_id='graph10', component_property='figure'),
    Input(component_id='radio_team', component_property='value'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph10(team, theme):
    
    mask = team_filter(team)
    df_10 = df.loc[mask]
    
    df_10 = df_10.groupby(['Meio de Propaganda', 'Mês'])['Valor Pago'].sum().reset_index()
    
    fig10 = px.line(df_10, y='Valor Pago', x='Mês', color='Meio de Propaganda')

    fig10.update_layout(main_config, height=200, template=template_from_url(theme))
    
    return fig10



@callback(
    Output(component_id='graph14', component_property='figure'),
    Input(ThemeChangerAIO.ids.radio('theme'), component_property='value')
)
def graph14(theme):
    
    fig14 = go.Figure()
    fig14.add_trace(go.Indicator(mode='number',
                                 value=df['Valor Pago'].sum(),
                                 title={"text": f"<span style='font-size:150%'>Valor Total</span><br><span style='font-size:70%'></span><br>"},
                                 number={'prefix': 'R$'}))

    fig14.update_layout(main_config, height=200, template=template_from_url(theme))
    
    return fig14


if __name__ == '__main__':
    app.run(debug=True)