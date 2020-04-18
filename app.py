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
from plotly.subplots import make_subplots


# In[2]:


extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
govt = 'https://www.mohfw.gov.in/'

response = requests.get(govt).content 
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
df.loc['India']= df.sum()


# In[5]:


n= len(df) - 1
c= df['Confirmed'].tail(1)[0]
d= df['Death'].tail(1)[0]
r= df['Recovery'].tail(1)[0]


# In[6]:


df_a= df.drop(['India']).sort_values(['Confirmed'])
df_d= df.drop(['India']).sort_values(['Confirmed'], ascending= False)


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
hphone.append({'label': 'nb', 'value': '0353 258 5478'})


# In[9]:


hloc= []
hloc.append({'label': 'wb1', 'value': 'None'})
hloc.append({'label': 'wb2', 'value': 'None'})
hloc.append({'label': 'id', 'value': 'Phoolbagan, Kolkata 700010'})
hloc.append({'label': 'pg', 'value': 'AJC Bose Rd, Kolkata 700020'})
hloc.append({'label': 'rg', 'value': 'KB Sarani, Kolkata 700004'})
hloc.append({'label': 'nb', 'value': 'Sushruta Nagar, Siliguri 734012'})


# In[10]:


heading1= 'COVID-19 @ INDIA'
helpp= '+91-11-23978046, 1075'
id_help= ' ID: 033-23032200'
rg_help= ' RG Kar: 033-25557656'
pg_help= ' PG: 033-22041101'
wb_help= ' WB Helpline: 033-24312600'
nb_help= ' NBMC: 0353 258 5478'


# In[11]:


st_ab= {
    'AP': 'Andhra Pradesh',
    'AR': 'Arunachal Pradesh',
    'AS': 'Assam',
    'BR': 'Bihar',
    'CG': 'Chhattisgarh',
    'GA': 'Goa',
    'GJ': 'Gujarat',
    'HR': 'Haryana',
    'HP': 'Himachal Pradesh',
    'JK': 'Jammu and Kashmir',
    'JH': 'Jharkhand',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'OR': 'Orissa',
    'PB': 'Punjab',
    'RJ': 'Rajasthan',
    'SK': 'Sikkim',
    'TN': 'Tamil Nadu',
    'TR': 'Tripura',
    'UK': 'Uttarakhand',
    'UP': 'Uttar Pradesh',
    'WB': 'West Bengal',
    'AN': 'Andaman and Nicobar Islands',
    'CH': 'Chandigarh',
    'DH': 'Dadra and Nagar Haveli',
    'DD': 'Daman and Diu',
    'DL': 'Delhi',
    'LD': 'Lakshadweep',
    'PY': 'Pondicherry',
    'TG': 'Telengana',
    'UT': 'Uttarakhand',
    'LA': 'Ladakh',
    'DN': 'Dadra and Nagar Haveli',
}


# In[12]:


updt= 'updated on ' + str(date.today())
states= []
for i in df.index.tolist():
    states.append({'label': i, 'value': i})


# 
# #############################################################################
# def form_pie(state):
#     figp1= go.Figure(data= [go.Pie(labels= ['Active', 'Recoveries', 'Deaths'], pull=[0, 0, 0.4],
#                               values= [df.loc[state]['Confirmed']-df.loc[state]['Recovery']-df.loc[state]['Death'],
#                                        df.loc[state]['Recovery'], df.loc[state]['Death']],
#                               textinfo= 'value', hoverinfo='percent', insidetextorientation='radial',
#                               marker= {'colors': ['rgba(0, 74, 140, 0.4)', 'rgba(0, 74, 140, 0.7)','rgba(0, 74, 140, 1)'],
#                                       'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}}                            
#                               ),               
#                         ],
#                      layout= go.Layout(yaxis= {'dtick': 1, 'showgrid': True}, paper_bgcolor='rgba(0,0,0,0)',
#                                   barmode= 'stack', plot_bgcolor='rgba(0,0,0,0)',
#                                   xaxis =  {'showgrid': True},
#                                       ))
#     figp1.update_layout(margin= dict(t=0, b=0, l=0, r=0), #legend= dict(x=.08, y=1.7),
#                        legend_orientation="h")
#     return figp1

# In[13]:


indiats= 'https://raw.githubusercontent.com/covid19india/api/master/csv/latest/case_time_series.csv'
dfts= pd.read_csv(indiats)
dfts['Date']= dfts['Date'].str[0:6]
#############################################################################
dates= []
for i, j in enumerate(dfts['Date'].tolist()):
    dates.append({'label': j, 'value': i})
#############################################################################    
def get_ts(dt1, dt2):
    df= dfts[dfts.index.to_series().between(dt1, dt2)]
    cnfrm= go.Scatter(x= df['Date'], y= df['Total Confirmed'], line= {'color': 'rgb(0, 74, 140)'},
                      mode= 'lines+markers', name= 'Confirmed')
    rcvr= go.Scatter(x= df['Date'], y= df['Total Recovered'], line= {'color': 'rgb(0, 74, 140)'},
                     mode= 'lines+markers', name= 'Recovered')
    dth= go.Scatter(x= df['Date'], y= df['Total Deceased'], line= {'color': 'rgb(0, 74, 140)'},
                                   mode= 'lines+markers', name= 'Deceased')

    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.03,
                       row_titles=("Confirmed", "Recovered", "Deceased"))
    fig.append_trace(cnfrm, 1, 1)
    fig.append_trace(rcvr, 2, 1)
    fig.append_trace(dth, 3, 1)
    fig.update_layout(plot_bgcolor= 'rgba(0,0,0,0)', margin= {'t':0, 'b':0, 'l':0, 'r':50},
                      showlegend= False, height=350, width=1000, paper_bgcolor='rgba(0,0,0,0)')
    
    return fig


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
                                 orientation= 'h', width= 0.3, name= 'Confirmed',
                                 text= temp.iloc[-sn:]['Confirmed'], textposition='auto',
                                 marker= {'color': 'rgba(0, 74, 140, 0.4)',
                                         'line': {'color': 'rgba(0, 74, 140, 1)', 'width': 2}},
                                  ),
                            go.Bar(x= temp.iloc[-sn:]['Recovery'], y= temp.iloc[-sn:].index,
                                   orientation= 'h', width= 0.4, name= 'Recovered',
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
    figb1.update_layout(margin= dict(t=0, b=0, l=0, r=50), legend= dict(x=.2, y=1.2),
                       legend_orientation="h")
    return figb1
#fig.update_layout(barmode='stack')


# In[15]:


tabs_style = {'height': '44px'}
tab_style = {'padding': '8px', 'color': 'rgb(0, 74, 140)', 'fontFamily': 'Helvetica'}
tab_selected_style = {
    'borderTop': '2px solid #004a8c',
    'borderBottom': '2px solid #004a8c',
    'backgroundColor': 'rgba(0,0,0,0)',
    'color': 'rgb(0, 74, 140)',
    'padding': '8px',
    'fontWeight': 'bold',
    'fontFamily': 'Helvetica'
}


# In[ ]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
               meta_tags= [{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1'}])
app.title = 'COVID-19@INDIA'
server= app.server
##################################################################################
##################################################################################
app.layout= html.Div([
    html.Div([
        ##########################################################################
        ###################### temp header ######################
        ##########################################################################
        html.Div([], className= ''),
        html.Div([
            html.H3(html.B('COVID-19')),
            dcc.Dropdown(id= 'state', options= states, clearable= False,
                        value= states[n]['value'], optionHeight= 50),
            
        ], className='d-none d-sm-block', style= {'width': '16%', 'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)', 'padding-left': '2%'}),
        html.Div([
            html.H3(html.B('COVID-19@INDIA'))
        ], className= 'col-12 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(id= 'cnfr')),
            html.H5('confirmed')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(id= 'cnfrm')),
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
            html.H3(html.B(id= 'rcvr')),
            html.H5('recovered')
        ], className='d-none d-sm-block', style= {'width': '12%', 'display': 'inline-block',
                   'text-align': 'right', 'color': 'rgb(0, 74, 140)'}),
        ##########################################################################
        html.Div([
            html.H3(html.B(id= 'dth1')),
            html.H5('deceased')
        ], className='col-md-2 col-6 d-block d-sm-none', style= {'display': 'inline-block',
                   'text-align': 'left', 'color': 'rgb(0, 74, 140)'}),
        html.Div([
            html.H3(html.B(id= 'dth')),
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
            html.H3(html.B(id= 'stts')),            
            html.H5(id= 'stt')
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
    html.Div([
        html.Div([
            dcc.Tabs(value='tab1', children=[              
                                
                dcc.Tab(label='figures', value='tab1', children= [
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([                
                                dcc.Dropdown(id= 'tb', options= tb, value= 'Top',
                                             clearable= False, style= {'width': '100%'})
                                ], style= {'display': 'inline-block'}),
                                html.Div([
                                dcc.Dropdown(id= 'sn', options= nos, value= 3,
                                             clearable= False, )
                                ], style= {'display': 'inline-block'})
                            ], style= {'display': 'inline-block', 'padding-left': '10%'}),  
                            html.Div([html.H4('states affected',
                                              style= {'padding-bottom': '3%', 'color': 'rgb(0, 74, 140)'})],
                                     style= {'display': 'inline-block', 'padding-left': '3%'})
                        ], style= {'padding-left': '25%'}),
                        dcc.Graph(id= 'Bar1', config= {'displayModeBar': False})
                    ], style= {'padding-top': '1%', 'width': '100%', 
                               'padding-left': '5%'},)
                ], style=tab_style, selected_style=tab_selected_style),
                
                dcc.Tab(label='trends', value='tab2', children= [
                    html.Div([
                        html.Div([
                            html.Div([
                                html.Div([html.H4('epidemic curve between',
                                              style= {'color': 'rgb(0, 74, 140)'})],
                                     style= {'display': 'inline-block',
                                             'padding-left': '3%'}),
                                html.Div([                
                                dcc.Dropdown(id= 'dt1', options= dates,
                                             value= dates[0]['value'], clearable= False)
                                ], style= {'display': 'inline-block', 'padding-left': '3%',
                                          'width': '15%'}),
                                html.Div([html.H4('and',
                                              style= {'padding-bottom': '3%',
                                                      'color': 'rgb(0, 74, 140)'})],
                                     style= {'display': 'inline-block',
                                             'padding-left': '3%'}),
                                
                                html.Div([
                                dcc.Dropdown(id= 'dt2', options= dates,
                                             value= dates[-1]['value'], clearable= False)
                                ], style= {'display': 'inline-block', 'padding-left': '3%',
                                          'width': '15%'})
                            ]),                              
                        ], style= {'padding-left': '20%', }),
                        dcc.Graph(id= 'Line1', config= {'displayModeBar': False})
                    ], style= {'padding-top': '1%', 'width': '100%'}, )
                ], style=tab_style, selected_style=tab_selected_style),
                
            ], style= tabs_style,
               colors={ 'border': 'rgba(0, 74, 140, 0)', 'primary': 'rgba(0, 74, 140, 1)',
                       "background": "rgba(0,0,0,0)"},),
        ]),       
    ], style= {'width': '95%', 'padding-left': '5%', 'padding-top': '02%'})    
], style= {'fontFamily': 'Helvetica',
           'background': 'linear-gradient(to right, rgba(0, 135, 255, 0) 0%, rgba(0, 135, 255, 0.4) 100%)'})
##################################################################################
@app.callback(Output('cnfrm', 'children'),
             [Input('state', 'value')])
def get_confirm(val):
    return df.loc[val]['Confirmed']
##########################################
@app.callback(Output('rcvr', 'children'),
             [Input('state', 'value')])
def get_confirm(val):
    return df.loc[val]['Recovery']
##########################################
@app.callback(Output('dth', 'children'),
             [Input('state', 'value')])
def get_confirm(val):
    return df.loc[val]['Death']
##########################################
@app.callback(Output('stts', 'children'),
             [Input('state', 'value')])
def get_confirm(val):
    if val=='India':
        return n
    pos= '#' + str(df_d.index.get_loc(val) + 1)
    return pos
##########################################
@app.callback(Output('stt', 'children'),
             [Input('state', 'value')])
def get_confirm(val):
    if val=='India':
        return 'states'
    return 'State'
##########################################
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
#@app.callback(Output('Pie1', 'figure'),
#             [Input('statep', 'value')])
#def update_pie(state):
#    return form_pie(state)
##########################################
@app.callback(Output('Bar1', 'figure'),
             [Input('tb', 'value'), Input('sn', 'value')])
def update_bar(tb, sn):
    return form_bar(tb, sn)
##########################################
@app.callback(Output('Line1', 'figure'),
             [Input('dt1', 'value'), Input('dt2', 'value')])
def update_bar(dt1, dt2):
    return get_ts(dt1, dt2)
##################################################################################
if __name__=='__main__':
    app.run_server()


# In[ ]:




