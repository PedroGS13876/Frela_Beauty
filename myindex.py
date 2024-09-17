from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Import from folders
from app import app  # Certifique-se de que app.py possui uma instância do Dash chamada 'app'
from components import sidebar, dashboards, extratos

# DataFrames and Dcc.Store
df_receitas = pd.read_csv("df_receitas.csv", index_col=0, parse_dates=True)
df_receitas_aux = df_receitas.to_dict('records')  # Converter para uma lista de registros para dcc.Store

df_despesas = pd.read_csv("df_despesas.csv", index_col=0, parse_dates=True)
df_despesas_aux = df_despesas.to_dict('records')  # Converter para uma lista de registros para dcc.Store

list_receitas = pd.read_csv('df_cat_receita.csv', index_col=0)
list_receitas_aux = list_receitas.to_dict('records')  # Converter para uma lista de registros para dcc.Store

list_despesas = pd.read_csv('df_cat_despesa.csv', index_col=0)
list_despesas_aux = list_despesas.to_dict('records')  # Converter para uma lista de registros para dcc.Store

# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    dcc.Store(id='store-receitas', data=df_receitas_aux),
    dcc.Store(id='store-despesas', data=df_despesas_aux),
    dcc.Store(id='stored-cat-receitas', data=list_receitas_aux),
    dcc.Store(id='stored-cat-despesas', data=list_despesas_aux),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),

        dbc.Col([
            html.Div(id="page-content")
        ], md=10),
    ])

], fluid=True, style={"padding": "0px"}, className="dbc")

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/dashboards":
        return dashboards.layout

    if pathname == "/extratos":
        return extratos.layout

    return html.Div([  # Fornecer um retorno padrão para caminhos desconhecidos
        "404 Page Not Found"
    ])

if __name__ == '__main__':
    app.run_server(debug=True)