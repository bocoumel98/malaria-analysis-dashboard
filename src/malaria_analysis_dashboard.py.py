#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 01:49:13 2023

@author: abdoul dibavata bocoum
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import dash
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from jupyter_dash import JupyterDash
from dash.dependencies import Input, Output





df = pd.read_csv('reported_numbers.csv')

df.dropna(inplace=True)

df=df[(df['No. of cases']!=0) & (df['No. of cases']>=df['No. of deaths'])]

df['Rapport']=df['No. of deaths']/df['No. of cases']
df.head(10)

df.shape

def fig_bar(data, x1, title1):
    
    fig=px.bar(data, x=x1, y=data.index, title='Top 10 Nombre de pays avec plus de cas', height=400)
    fig.update_traces(marker_line_color='blue', marker_line_width=2)
    return fig


def fig_line(data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=data.index, y=data['No. of cases'], name="Cases")
    )
    
    fig.add_trace(
        go.Scatter(x=data.index, y=data['No. of deaths'], name="deaths", yaxis='y2'),
    )
    
    fig.add_trace(
        go.Scatter(x=data.index, y=data['Rapport'], name="rapport", yaxis='y3')
    )
    
    fig.update_layout(
        xaxis=dict(
            domain=[0.5, 0.3]
        ),
        yaxis=dict(
            title="yaxis cas",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            ),
            position= 0.05
        ),
        yaxis2=dict(
            title="yaxis mort",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            anchor="free",
            overlaying="y",
            side="left",
            position= 0.01
        ),
        yaxis3=dict(
            title="yaxis rapport",
            titlefont=dict(
                color="#d62728"
            ),
            tickfont=dict(
                color="#d62728"
            ),
            anchor="x",
            overlaying="y",
            side="right",
            
        ),
        
    )
    
    return fig




    
    
    

top10_plus_cas=df.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=False).head(10)
fig_plus_cas=fig_bar(top10_plus_cas, 'No. of cases', 'Top 10 Nombre de pays avec plus de cas')


top10_plus_mort=df.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=False).head(10)
fig_plus_mort=fig_bar(top10_plus_mort, 'No. of deaths', 'Top 10 Nombre de pays avec plus de mort')

top10_moins_cas=df.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=True).head(10)
fig_moins_cas=fig_bar(top10_moins_cas, 'No. of cases', 'Top 10 Nombre de pays avec moins de cas')


top10_moins_mort=df.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=True).head(10)
fig_moins_mort=fig_bar(top10_moins_mort, 'No. of deaths', 'Top 10 Nombre de pays avec moins de mort')


data_groupby_region=df.groupby('WHO Region').sum()
pie1 = px.pie(data_groupby_region, values='No. of cases' , names =data_groupby_region.index, title='diagramme en camember cas total par région')
pie2 = px.pie(data_groupby_region, values='No. of deaths' , names =data_groupby_region.index, title='diagramme en camembert mort total par région')


data_line= df.groupby('Year').sum()

fig_line_plot= fig_line(data_line)



App = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

App.layout = html.Div([
    
        html.H1('Dashboard Etude sur la Malaria entre 2000 et 2017',className="bg-primary text-white p-4 mb-2 text-center",style={'textAlign':'Center','color':'red','font-size':40}),
        
        html.Br(style={'height':'30px'}),
        html.Br(style={'height':'30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='region_or_country',options=sorted([{'label':x, 'value':x} for x in df['WHO Region'].unique()]+[{'label':x, 'value':x} for x in df['Country'].unique()], key=lambda d: d['label']),
                                placeholder='Filtrer sur un continent or Country',
                                style={'width':'300px'})
                                ], width={'size':30, 'offset':4}),
            
           
            
            ]),
        
     

       
        
        dbc.Row([
            
            dbc.Col(dbc.Card(
                
                dbc.CardBody([
                    html.H4(children= 'Total case since 2000', style={ 'textAlign': 'center','color': 'white'}),
                    
                    html.P(id='totcas',children=f"{df['No. of cases'].sum()} ",style = {'textAlign': 'center', 'color': 'black','fontSize':20})
                    
                    ])
                
                , color = 'info',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 0.5, xl = 4, style = {'padding':'12px 12px 12px 14px'}),
            
            
            dbc.Col(dbc.Card(
                
                dbc.CardBody([
                    html.H4(children= 'Total mort since 2000', style={ 'textAlign': 'center','color': 'white'}),
                    
                    html.P(id='totmort',children=f"{df['No. of deaths'].sum()} ",style = {'textAlign': 'center', 'color': 'black','fontSize':20})
                    
                    ])
                
                , color = 'danger',style = {'text-align':'center'}, inverse = True),xs = 12, sm = 12, md = 4, lg = 0.5, xl = 4, style = {'padding':'12px 12px 12px 12px'}),
            
            


            
             ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='line1',figure=fig_line_plot)
            ],width={'size':6, 'offset':3}),
            
            ])
        
             ,

        
        html.Br(style={'height':'30px'}),
        html.Br(style={'height':'30px'}),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='WHO Region1',options=[{'label':x, 'value':x} for x in df['WHO Region'].unique()]+[{'label':x, 'value':x} for x in df['Country'].unique()],
                                placeholder='Filtrer sur un continent',
                                style={'width':'300px'})
                                ], width={'size':3, 'offset':1}),
            
            
            dbc.Col([
                dcc.Dropdown(id='Year1',options=[{'label':x, 'value':x} for x in df['Year'].unique()],
                                placeholder='Filter Year',
                                style={'width':'300px'})
                                ], width={'size':3, 'offset':1})
            
            ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='bar1',figure=fig_plus_cas)
            ],width={'size':3}),
            dbc.Col([
                dcc.Graph(id='bar2',figure=fig_plus_mort)
            ],width={'size':3}),
            
            dbc.Col([
                dcc.Graph(id='bar3',figure=fig_moins_cas)
            ],width={'size':3}),
            
            dbc.Col([
                dcc.Graph(id='bar4',figure=fig_moins_mort)
            ],width={'size':3}),
            
        ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id='region_pie',options=[{'label':x, 'value':x} for x in df['Year'].unique()],
                                placeholder='Filtrer sur par annee les diaggarmmes en cammenbert',
                                style={'width':'300px'})
                                ], width={'size':3, 'offset':3}),
            
           
            
            ]),
        
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='pie1',figure=pie1)
            ],width={'size':3}),
            dbc.Col([
                dcc.Graph(id='pie2',figure=pie2)
            ],width={'size':3}),
            
            
            ])
        
    ])
        
        
        
        


@App.callback(
    Output('totcas', 'children'),
    Output('totmort', 'children'),
    Input('region_or_country', 'value'),
    
    
    )

def update1(region_or_country):
    if region_or_country :
        data = df[(df['WHO Region'] == region_or_country) | (df['Country'] == region_or_country)]
        return data['No. of cases'].sum(), data['No. of deaths'].sum()
    
    else:
        return df['No. of cases'].sum(), df['No. of deaths'].sum()



@App.callback(
    
    Output('bar1', 'figure'),
    Output('bar2', 'figure'),
    Output('bar3', 'figure'),
    Output('bar4', 'figure'),
    Input('WHO Region1', 'value'),
    Input('Year1', 'value'),
    prevent_initial_call=True
    
    )

def update2(region, annee):
    if region and not annee:
        
        data = df[df['WHO Region'] == region]
        
        top10_plus_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=False).head(10)
        fig_plus_cas=fig_bar(top10_plus_cas, 'No. of cases', 'Top 10 Nombre de pays avec plus de cas')
        
        top10_plus_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=False).head(10)
        fig_plus_mort=fig_bar(top10_plus_mort, 'No. of deaths', 'Top 10 Nombre de pays avec plus de mort')
        
        top10_moins_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=True).head(10)
        fig_moins_cas=fig_bar(top10_moins_cas, 'No. of cases', 'Top 10 Nombre de pays avec moins de cas')
        
        top10_moins_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=True).head(10)
        fig_moins_mort=fig_bar(top10_moins_mort, 'No. of deaths', 'Top 10 Nombre de pays avec moins de mort')
        
        
        
        return fig_plus_cas, fig_plus_mort, fig_moins_cas, fig_moins_mort
    elif not region and annee:
        data = df[df['Year'] == annee]
        
        top10_plus_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=False).head(10)
        fig_plus_cas=fig_bar(top10_plus_cas, 'No. of cases', 'Top 10 Nombre de pays avec plus de cas')
        
        top10_plus_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=False).head(10)
        fig_plus_mort=fig_bar(top10_plus_mort, 'No. of deaths', 'Top 10 Nombre de pays avec plus de mort')
        
        top10_moins_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=True).head(10)
        fig_moins_cas=fig_bar(top10_moins_cas, 'No. of cases', 'Top 10 Nombre de pays avec moins de cas')
        
        top10_moins_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=True).head(10)
        fig_moins_mort=fig_bar(top10_moins_mort, 'No. of deaths', 'Top 10 Nombre de pays avec moins de mort')
        
        
        
        return fig_plus_cas, fig_plus_mort, fig_moins_cas, fig_moins_mort
    
    elif region and annee:
        data = df[(df['WHO Region'] == region) & (df['Year'] == annee)]
        
        top10_plus_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=False).head(10)
        fig_plus_cas=fig_bar(top10_plus_cas, 'No. of cases', 'Top 10 Nombre de pays avec plus de cas')
        
        top10_plus_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=False).head(10)
        fig_plus_mort=fig_bar(top10_plus_mort, 'No. of deaths', 'Top 10 Nombre de pays avec plus de mort')
        
        top10_moins_cas=data.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=True).head(10)
        fig_moins_cas=fig_bar(top10_moins_cas, 'No. of cases', 'Top 10 Nombre de pays avec moins de cas')
        
        top10_moins_mort=data.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=True).head(10)
        fig_moins_mort=fig_bar(top10_moins_mort, 'No. of deaths', 'Top 10 Nombre de pays avec moins de mort')
        
        
        
        return fig_plus_cas, fig_plus_mort, fig_moins_cas, fig_moins_mort
        
    else:
        top10_plus_cas=df.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=False).head(10)
        fig_plus_cas=fig_bar(top10_plus_cas, 'No. of cases', 'Top 10 Nombre de pays avec plus de cas')


        top10_plus_mort=df.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=False).head(10)
        fig_plus_mort=fig_bar(top10_plus_mort, 'No. of deaths', 'Top 10 Nombre de pays avec plus de mort')

        top10_moins_cas=df.groupby('Country').sum().sort_values(by = 'No. of cases', ascending=True).head(10)
        fig_moins_cas=fig_bar(top10_moins_cas, 'No. of cases', 'Top 10 Nombre de pays avec moins de cas')


        top10_moins_mort=df.groupby('Country').sum().sort_values(by = 'No. of deaths', ascending=True).head(10)
        fig_moins_mort=fig_bar(top10_moins_mort, 'No. of deaths', 'Top 10 Nombre de pays avec moins de mort')
        
        return fig_plus_cas, fig_plus_mort, fig_moins_cas, fig_moins_mort
    
    
@App.callback(
    Output('pie1', 'figure'),
    Output('pie2', 'figure'),
    Input('region_pie', 'value')
    
    )
def update3(year):
    if year:
        data = df[df['Year']==year]
        data_groupby_region=data.groupby('WHO Region').sum()
        pie1 = px.pie(data_groupby_region, values='No. of cases' , names =data_groupby_region.index, title='diagramme en camember cas total par région')
        pie2 = px.pie(data_groupby_region, values='No. of deaths' , names =data_groupby_region.index, title='diagramme en camembert mort total par région')
        
    

    else:
        data_groupby_region=df.groupby('WHO Region').sum()
        pie1 = px.pie(data_groupby_region, values='No. of cases' , names =data_groupby_region.index, title='diagramme en camember cas total par région')
        pie2 = px.pie(data_groupby_region, values='No. of deaths' , names =data_groupby_region.index, title='diagramme en camembert mort total par région')
        
    return pie1, pie2

if __name__ == '__main__':
  App.run_server(debug=True)
