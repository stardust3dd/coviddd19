#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import date 

# Scraping
import requests 
from bs4 import BeautifulSoup 
import numpy as np 

# Dashboarding
import dash
import plotly.graph_objects as go
import plotly.express as px
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output


# In[2]:


extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'

response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 

stats = [] 
all_rows = soup.find_all('tr') 

for row in all_rows:
    stat= extract_contents(row.find_all('td'))
    if len(stat)==5:
        stats.append(stat)


# In[3]:


headers= ['Sno', 'State', 'Confirmed', 'Recovery', 'Death']


# In[4]:


df= pd.DataFrame(stats, columns= headers).set_index('State')
df.drop(['Sno'], axis= 1, inplace= True)
df= df.astype(int)
#df.rename({2: "Confirmed", 3: "Recovery", 4: "Death"}, axis= 1, inplace= True)
#df.loc['Total']= df.sum()
df


# In[5]:


n= len(df)
c= df['Confirmed'].sum()
d= df['Death'].sum()
r= df['Recovery'].sum()


# In[6]:


df_a= df.sort_values(['Confirmed'])
df_d= df.sort_values(['Confirmed'], ascending= False)


# In[7]:


hnames= []
hnames.append({'label': 'WB helpline 1', 'value': 'wb1'})
hnames.append({'label': 'WB helpline 2', 'value': 'wb2'})
hnames.append({'label': 'Beliaghata ID', 'value': 'id'})
hnames.append({'label': 'PG Hospital', 'value': 'pg'})
hnames.append({'label': 'R G Kar', 'value': 'rg'})


# In[8]:


hphone= []
hphone.append({'label': 'wb1', 'value': '033-24312600'})
hphone.append({'label': 'wb2', 'value': '1800313444222'})
hphone.append({'label': 'id', 'value': '033-23032200'})
hphone.append({'label': 'pg', 'value': '033-22041101'})
hphone.append({'label': 'rg', 'value': '033-25557656'})


# In[9]:


hloc= []
hloc.append({'label': 'wb1', 'value': 'None'})
hloc.append({'label': 'wb2', 'value': 'None'})
hloc.append({'label': 'id', 'value': 'Phoolbagan, Kol 10'})
hloc.append({'label': 'pg', 'value': 'AJC Bose Rd, Kol 20'})
hloc.append({'label': 'rg', 'value': 'KB Sarani, Kol 04'})


# In[10]:


heading1= 'COVID-19 @ INDIA'
helpp= '+91-11-23978046, 1075'
id_help= ' ID: 033-23032200'
rg_help= ' RG Kar: 033-25557656'
pg_help= ' PG: 033-22041101'
wb_help= ' WB Helpline: 033-24312600'


# In[11]:


updt= 'Updated on ' + str(date.today())


# In[12]:


updt


# In[13]:


states= []
for i in df.index.tolist():
    states.append({'label': i, 'value': i})
#############################################################################
def form_pie(state):
    figp1= go.Figure(data= [go.Pie(labels= ['Active', 'Recoveries', 'Deaths'], pull=[0, 0, 0.4],
                              values= [df.loc[state]['Confirmed']-df.loc[state]['Recovery']-df.loc[state]['Death'],
                                       df.loc[state]['Recovery'], df.loc[state]['Death']],
                              textinfo= 'value', hoverinfo='percent', insidetextorientation='radial',
                              marker= {'colors': ['rgba(0, 74, 140, 0.4)', 'rgba(0, 74, 140, 0.7)','rgba(0, 74, 140, 1)'],
                                      'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}}                            
                              ),               
                        ],
                     layout= go.Layout(yaxis= {'dtick': 1, 'showgrid': True}, paper_bgcolor='rgba(0,0,0,0)',
                                  barmode= 'stack', plot_bgcolor='rgba(0,0,0,0)',
                                  xaxis =  {'showgrid': True},
                                      ))
    figp1.update_layout(margin= dict(t=0, b=0, l=0, r=0), #legend= dict(x=.08, y=1.7),
                       legend_orientation="h")
    return figp1


# In[14]:


nos= []
for i in [3, 5, 7, 10]:
    nos.append({'label': i, 'value': i})
#############################################################################
tb= []
tb.append({'label': 'Top', 'value': 'Top'})
tb.append({'label': 'Bottom', 'value': 'Bottom'})
############################################################################# 
def form_bar(tb, sn):
    if tb=='Top':
        temp= df_a
    else:
        temp= df_d
    figb1= go.Figure(data= [go.Bar(x= temp.iloc[-sn:]['Confirmed'], y= temp.iloc[-sn:].index,
                                 orientation= 'h', width= 0.5, name= 'Confirmed',
                                 text= temp.iloc[-sn:]['Confirmed'], textposition='auto',
                                 marker= {'color': 'rgba(0, 74, 140, 0.4)',
                                         'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}},
                                  ),
                            go.Bar(x= temp.iloc[-sn:]['Recovery'], y= temp.iloc[-sn:].index,
                                   orientation= 'h', width= 0.5, name= 'Recovered',
                                   text= temp.iloc[-sn:]['Recovery'], textposition='auto',
                                   marker= {'color': 'rgba(0, 74, 140, 0.7)',
                                           'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}},
                                  ),
                            go.Bar(x= temp.iloc[-sn:]['Death'], y= temp.iloc[-sn:].index,
                                   orientation= 'h', width= 0.5, name= 'Deceased',
                                   text= temp.iloc[-sn:]['Death'], textposition='auto',
                                   marker= {'color': 'rgba(0, 74, 140, 1)',
                                           'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}}),
                            ],
                    layout= go.Layout(yaxis= {'dtick': 1, 'showgrid': True}, paper_bgcolor='rgba(0,0,0,0)',
                                      barmode= 'stack', plot_bgcolor='rgba(0,0,0,0)',
                                      xaxis =  {'showgrid': True},
    ))
    figb1.update_layout(margin= dict(t=0, b=50, l=0, r=50), #legend= dict(x=.2, y=1.2),
                       legend_orientation="h")
    return figb1
#fig.update_layout(barmode='stack')


# In[15]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
               meta_tags= [{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1'}])
app.title = 'COVID-19@INDIA'
server= app.server
##################################################################################
##################################################################################
app.layout= html.Div([
    html.Div([
        html.Div([
            html.H3(html.B('COVID-19')),
            html.H5('@INDIA')
        ], className='d-none d-sm-block', style= {'width': '16%', 'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)', 'padding-left': '2%'}),
        html.Div([
            html.H3(html.B('COVID-19@INDIA'))
        ], className= 'col-12 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(c)),
            html.H5('confirmed')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(c)),
            html.H5('confirmed')
        ], className='d-none d-sm-block', style= {'width': '11%', 'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(r)),
            html.H5('recovered')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(r)),
            html.H5('recovered')
        ], className='d-none d-sm-block', style= {'width': '12%', 'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(d)),
            html.H5('deceased')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(d)),
            html.H5('deceased')
        ], className='d-none d-sm-block', style= {'width': '12%', 'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(n)),
            html.H5('states')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(n)),
            html.H5('states')
        ], className='d-none d-sm-block', style= {'width': '8%', 'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################        
        html.Div([
            html.Div([
                dcc.Dropdown(id= 'helpdd1', options= hnames, clearable= False,
                             value= hnames[0]['value'], )
            ], style= {'width': '45%', 'display': 'inline-block', 'padding-bottom': '2%'}),
            html.Div([                
                html.H3(html.B(id= 'hname1', className= 'd-none d-sm-block')),
                html.H6(updt),
            ], style= {'width': '55%', 'padding-left': '6%',
                       'display': 'inline-block', 'text-align': 'left'})
        ], className='d-none d-sm-block', style= {'width': '40%', 'display': 'inline-block', 'padding-left': '2%',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.Div([dcc.Dropdown(id= 'helpdd2', options= hnames, 
                                   value= hnames[0]['value'], clearable= False)],
                     className='col-6 d-block d-sm-none',
                style= {'display': 'flex', 'align-items': 'right',
                        'justify-content': 'right', 'display': 'inline-block'}),
            html.Div([html.H3(html.B(id= 'hname2'))], className='col-md-2 col-6 d-block d-sm-none',
                style= {'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'})           
        ], className= 'row', style= {'padding-left': '5%', 'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
    ], className= 'row',
        style= {'padding-left': '3%', 'width': '100%', 'padding-top': '1%'}),   
    ########################## Header ends here ##########################
    html.Hr(style= {'border-top': '10px dotted rgb(0, 74, 140)', 'width': '95%'}),
    html.Div([
        html.Div([
            dcc.Dropdown(id= 'statep', options= states, value= df.index[0], clearable= False,
                         style= {'width': '90%', 
                                 'padding-left': '25%', 'padding-right': '10%'}),
            dcc.Graph(id= 'Pie1', config= {'displayModeBar': False})
        ], style= {'padding-top': '1%', 'width': '41%'}, className='col-md-5 col-12'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([                
                    dcc.Dropdown(id= 'tb', options= tb, value= 'Top', clearable= False,
                                style= {'width': '100%'})
                    ], style= {'display': 'inline-block'}),
                    html.Div([
                    dcc.Dropdown(id= 'sn', options= nos, value= 3, clearable= False,
                                style= {'width': '100%'})
                    ], style= {'display': 'inline-block'})
                ], style= {'display': 'inline-block'}),  
                html.Div([html.H4('states affected',
                                  style= {'padding-bottom': '3%', 'color': 'rgb(0, 74, 140)'})],
                         style= {'display': 'inline-block', 'padding-left': '3%'})
            ], style= {'padding-left': '25%'}),
            dcc.Graph(id= 'Bar1', config= {'displayModeBar': False})
        ], style= {'padding-top': '1%', 'width': '58%', 'padding-left': '5%'}, className='col-md-7 col-12')
    ], className='row')    
], style= {'fontFamily': 'Helvetica',
           'background': 'linear-gradient(to right, rgba(0, 135, 255, 0) 0%, rgba(0, 135, 255, 0.4) 100%)'})
##################################################################################
@app.callback(Output('hname1', 'children'),
             [Input('helpdd1', 'value')])
def update_hname(val):
    for i in range(len(hphone)):
        if hphone[i]['label']==val:
            return hphone[i]['value']  
##########################################        
@app.callback(Output('hname2', 'children'),
             [Input('helpdd2', 'value')])
def update_hname(val):
    for i in range(len(hphone)):
        if hphone[i]['label']==val:
            return hphone[i]['value']          
##########################################
#@app.callback(Output('hmail', 'children'),
#             [Input('helpdd1', 'value')])
#def update_hmail(val):
#    for i in range(len(hloc)):
#        if hloc[i]['label']==val:
#            return hloc[i]['value']     
##########################################
@app.callback(Output('Pie1', 'figure'),
             [Input('statep', 'value')])
def update_pie(state):
    return form_pie(state)
##########################################
@app.callback(Output('Bar1', 'figure'),
             [Input('tb', 'value'), Input('sn', 'value')])
def update_bar(tb, sn):
    return form_bar(tb, sn)
##################################################################################
if __name__=='__main__':
    app.run_server()


# In[ ]:




