from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin = dict(l=25, r=25, t=25, b=0)

# =========  Layout  =========== #
layout = dbc.Row([
    # Primeira Linha de Cards
    dbc.Row([
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Produtos Indicados"),
                    html.H5("Últimas 24h", id="p-saldo-dashboards", style={}),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
            ])
        ], width=3),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Produtos Indicados"),
                    html.H5("Últimas semanas", id="p-receita-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
            ])
        ], width=3),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Clientes"),
                    html.H5("Últimas 24 horas", id="p-receita-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
            ])
        ], width=3),
        dbc.Col([
            dbc.CardGroup([
                dbc.Card([
                    html.Legend("Clientes"),
                    html.H5("Últimas semanas", id="p-despesa-dashboards"),
                ], style={"padding-left": "20px", "padding-top": "10px"}),
            ])
        ], width=3),
    ], style={"margin": "10px"}),

    # Segunda Linha - Filtros e Gráfico
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend("Filtrar lançamentos", className="card-title"),
                html.Label("Categorias das receitas"),
                html.Div(
                    dcc.Dropdown(
                        id="dropdown-receita",
                        clearable=False,
                        style={"width": "100%"},
                        persistence=True,
                        persistence_type="session",
                        multi=True
                    )
                ),
                html.Label("Categorias das despesas", style={"margin-top": "10px"}),
                dcc.Dropdown(
                    id="dropdown-despesa",
                    clearable=False,
                    style={"width": "100%"},
                    persistence=True,
                    persistence_type="session",
                    multi=True
                ),
                html.Legend("Período de Análise", style={"margin-top": "10px"}),
                dcc.DatePickerRange(
                    month_format='Do MMM, YY',
                    end_date_placeholder_text='Data...',
                    start_date=datetime.today(),
                    end_date=datetime.today() + timedelta(days=31),
                    id='date-picker-config',
                    style={'z-index': '100'}
                ),
            ], style={"height": "100%", "padding": "20px"}),
        ], width=4),

        dbc.Col([
            dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}),
        ], width=8),
    ], style={"margin": "10px"}),

    # Terceira Linha - Gráficos
    dbc.Row([
        dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
        dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}), width=3),
        dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=3),
    ], style={"margin": "10px"})
])

# =========  Callbacks  =========== #
# Dropdown Receita
@app.callback(
    [Output("dropdown-receita", "options"),
     Output("dropdown-receita", "value"),
     Output("p-receita-dashboards", "children")],
    Input("store-receitas", "data")
)
def populate_dropdown_receitas(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    return [{"label": x, "value": x} for x in df.Categoria.unique()], val, f"R$ {valor}"

# Dropdown Despesa
@app.callback(
    [Output("dropdown-despesa", "options"),
     Output("dropdown-despesa", "value"),
     Output("p-despesa-dashboards", "children")],
    Input("store-despesas", "data")
)
def populate_dropdown_despesas(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    val = df.Categoria.unique().tolist()
    return [{"label": x, "value": x} for x in df.Categoria.unique()], val, f"R$ {valor}"

# VALOR - saldo
@app.callback(
    Output("p-saldo-dashboards", "children"),
    [Input("store-despesas", "data"),
     Input("store-receitas", "data")]
)
def saldo_total(despesas, receitas):
    df_despesas = pd.DataFrame(despesas)
    df_receitas = pd.DataFrame(receitas)
    valor = df_receitas['Valor'].sum() - df_despesas['Valor'].sum()
    return f"R$ {valor}"

# Gráfico 1
@app.callback(
    Output('graph1', 'figure'),
    [Input('store-despesas', 'data'),
     Input('store-receitas', 'data'),
     Input("dropdown-despesa", "value"),
     Input("dropdown-receita", "value"),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def update_output(data_despesa, data_receita, despesa, receita, theme):
    df_ds = pd.DataFrame(data_despesa).sort_values(by='Data', ascending=True)
    df_rc = pd.DataFrame(data_receita).sort_values(by='Data', ascending=True)

    dfs = [df_ds, df_rc]
    for df in dfs:
        df['Acumulo'] = df['Valor'].cumsum()
        df["Data"] = pd.to_datetime(df["Data"])
        df["Mes"] = df["Data"].dt.month

    df_receitas_mes = df_rc.groupby("Mes")["Valor"].sum()
    df_despesas_mes = df_ds.groupby("Mes")["Valor"].sum()
    df_saldo_mes = df_receitas_mes - df_despesas_mes
    df_saldo_mes = df_saldo_mes.reset_index()
    df_saldo_mes['Acumulado'] = df_saldo_mes['Valor'].cumsum()
    df_saldo_mes['Mes'] = df_saldo_mes['Mes'].apply(lambda x: calendar.month_abbr[x])

    df_ds = df_ds[df_ds['Categoria'].isin(despesa)]
    df_rc = df_rc[df_rc['Categoria'].isin(receita)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Receitas', x=df_rc['Data'], y=df_rc['Acumulo'], fill='tonextx', mode='lines'))

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Gráfico 2
@app.callback(
    Output('graph2', 'figure'),
    [Input('store-receitas', 'data'),
     Input('store-despesas', 'data'),
     Input('dropdown-receita', 'value'),
     Input('dropdown-despesa', 'value'),
     Input('date-picker-config', 'start_date'),
     Input('date-picker-config', 'end_date'),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def graph2_show(data_receita, data_despesa, receita, despesa, start_date, end_date, theme):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)

    dfs = [df_ds, df_rc]
    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df_final['Data'] = pd.to_datetime(df_final['Data'])
    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date)
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Categoria'].isin(receita) | df_final['Categoria'].isin(despesa)]

    fig = px.bar(df_final, x="Data", y="Valor", color='Output', barmode="group")
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig

# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-receitas', 'data'),
     Input('dropdown-receita', 'value'),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_receita(data_receita, receita, theme):
    df = pd.DataFrame(data_receita)
    df = df[df['Categoria'].isin(receita)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Receitas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig

# Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [Input('store-despesas', 'data'),
     Input('dropdown-despesa', 'value'),
     Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_despesa(data_despesa, despesa, theme):
    df = pd.DataFrame(data_despesa)
    df = df[df['Categoria'].isin(despesa)]

    fig = px.pie(df, values=df.Valor, names=df.Categoria, hole=.2)
    fig.update_layout(title={'text': "Despesas"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig