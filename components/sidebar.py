import os
import dash
import json
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime, date

import pdb
from dash_bootstrap_templates import ThemeChangerAIO

# ========= DataFrames ========= #
import numpy as np
import pandas as pd
from globals import *

# ========= Layout ========= #
layout = dbc.Card([
    # Adicionando a imagem no lugar do título e descrição
    html.Div([
        html.Img(src="https://beauty-intelligence-admin-web.netlify.app/assets/layout/images/logo.png", 
            style={"width": "100%", "height": "auto", "margin-bottom": "20px"})  # Original
    ], style={"text-align": "center"}),  # Original

    # Continuando com o restante do layout
    # Seção PERFIL ------------------------
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Selecionar Perfil")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="https://beauty-intelligence-admin-web.netlify.app/assets/layout/images/logo.png", 
                                    className='perfil_avatar', top=True),
                        dbc.CardBody([
                            html.H4("Perfil Homem", className="card-title"),
                            html.P(
                                "Um Card com exemplo do perfil Homem. Texto para preencher o espaço",
                                className="card-text",
                            ),
                            dbc.Button("Acessar", color="warning"),
                        ]),
                    ]),
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="https://beauty-intelligence-admin-web.netlify.app/assets/layout/images/logo.png", 
                                    top=True, className='perfil_avatar'),
                        dbc.CardBody([
                            html.H4("Perfil Mulher", className="card-title"),
                            html.P(
                                "Um Card com exemplo do perfil Mulher. Texto para preencher o espaço",
                                className="card-text",
                            ),
                            dbc.Button("Acessar", color="warning"),
                        ]),
                    ]),
                ], width=6),
            ], style={"padding": "5px"}),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="https://beauty-intelligence-admin-web.netlify.app/assets/layout/images/logo.png", 
                                    top=True, className='perfil_avatar'),
                        dbc.CardBody([
                            html.H4("Perfil Casa", className="card-title"),
                            html.P(
                                "Um Card com exemplo do perfil Casa. Texto para preencher o espaço",
                                className="card-text",
                            ),
                            dbc.Button("Acessar", color="warning"),
                        ]),
                    ]),
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardImg(src="https://beauty-intelligence-admin-web.netlify.app/assets/layout/images/logo.png", 
                                    top=True, className='perfil_avatar'),
                        dbc.CardBody([
                            html.H4("Adicionar Novo Perfil", className="card-title"),
                            html.P(
                                "Esse projeto é um protótipo, o botão de adicionar um novo perfil está desativado momentaneamente!",
                                className="card-text",
                            ),
                            dbc.Button("Adicionar", color="success"),
                        ]),
                    ]),
                ], width=6),
            ], style={"padding": "5px"}),
        ]),
    ],
    style={"background-color": "rgba(0, 0, 0, 0.5)"},  # Original
    id="modal-perfil",
    size="lg",
    is_open=False,
    centered=True,
    backdrop=True),

    # Seção NAV ------------------------
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
            dbc.NavLink("Relatório", href="/relatorio", active="exact"),
        ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),  # Original

    ThemeChangerAIO(aio_id="theme", radio_props={"value": dbc.themes.QUARTZ})
], id='sidebar_completa')

# ========= Callbacks ========= #
# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("botao_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal_perfil(n1, is_open):
    if n1:
        return not is_open
