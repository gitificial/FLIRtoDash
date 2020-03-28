import base64
import io

import pandas as pd
import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'FLIR Thermoscan'

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app.layout = html.Div([

    dcc.Store(id='memory', storage_type='session'),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([
            dbc.Form([
                dbc.FormGroup([
                    dcc.Upload(id='upload-csv', multiple=False, children=html.Div([ dbc.Button("Select CSV", outline=True, color="secondary")]), className="mr-4"),
                    dbc.Label("Selected CSV: ", className="mr-2"),
                    dbc.Label("none selected", id='csv-filename'),
                ],className="mr-3",),
            ],inline=True,),
        ], md=10),
        dbc.Col(md=1),
    ]),
        
    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div([dcc.Graph(id='heatmap'),], style={'display': 'inline-block', 'width': '100%'})], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='x-range')], md=1),
        dbc.Col([
                
            html.Div([
                dcc.RangeSlider(
                    id='x-range-slider',
                    min=0,
                    max=0,
                    step=1.0,
                    value=[0, 140],
                    
                    marks={
                        0: {'label': '0'},
                        20: {'label': '20'},
                        40: {'label': '40'},
                        60: {'label': '60'},
                        80: {'label': '80'},
                        100: {'label': '100'},
                        120: {'label': '120'},
                        140: {'label': '140'}
                    }
                    
            )]

        )], md=9),

        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='y-range')], md=1),
        dbc.Col([
                
            html.Div([
                dcc.RangeSlider(
                    id='y-range-slider',
                    min=0,
                    max=0,
                    step=1.0,
                    value=[0, 140],
                    
                    marks={
                        0: {'label': '0'},
                        20: {'label': '20'},
                        40: {'label': '40'},
                        60: {'label': '60'},
                        80: {'label': '80'},
                        100: {'label': '100'},
                        120: {'label': '120'},
                        140: {'label': '140'}
                    }
            )]

        )], md=9),

        dbc.Col(md=1),
    ]),
         
    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='temp-range')], md=1),
        dbc.Col([
                
            html.Div([
                dcc.RangeSlider(
                    id='temp-range-slider',
                    min=0,
                    max=140,
                    step=0.1,
                    value=[0, 140],
            )]

        )], md=9),

        dbc.Col(md=1),
    ]),
            
    html.Br(),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='mean')], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='min')], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='max')], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='stddev')], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='delta_min_max')], md=10),
        dbc.Col(md=1),
    ]),

    dbc.Row([
        dbc.Col(md=1),
        dbc.Col([html.Div(id='cv')], md=10),
        dbc.Col(md=1),
    ]),

    html.Div(id='output-data-upload'),

])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
        elif 'xls' in filename:
            # assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        else:
            # when no upload is available use random pattern
            df = pd.DataFrame(np.random.randint(0,100,size=(140, 140)))
            return df
        
    except Exception as e:
        print(e)
        return html.Div(['There was an error processing this file.'])

@app.callback([Output('memory', 'data'), 
               Output('csv-filename', 'children')],
              [Input('upload-csv', 'contents')],
              [State('upload-csv', 'filename'),
               State('upload-csv', 'last_modified')])
def load_heatmap(content, filename, date):
    if content is not None:
        data = parse_contents(content, filename, date)
        return data.to_json(orient='split'), [filename]
    else:
        data = pd.DataFrame(np.random.randint(0,100,size=(140, 140)))
        return data.to_json(orient='split'), 'none selected'

def create_heatmap(df, x_left, x_right, y_lower, y_upper, temp_slider_lower, temp_slider_upper):
    return {'data': [go.Heatmap(
                              z= df,
                              hovertemplate = 'x: %{x}<br>' + 'y: %{y}<br>' + 'Temp.: <b>%{z}</b><br>' + "<extra></extra>",
                              
                              # zmin = temp_lower,
                              # zmid = (temp_upper - temp_lower) / 2,
                              # zmax = temp_upper,
                              
                              zmin = temp_slider_lower,
                              zmax = temp_slider_upper, 
                              
                              # colorbar=dict(
                              #  title="Temperature"
                              #   )
                              # colorscale="Cividis",
                              # hoverongaps = False
                                )],
                'layout': go.Layout(
                                # title='Heatmap',
                                xaxis=dict(side="top", automargin = True),
                                yaxis=dict(autorange="reversed"),
                                # yaxis=dict(autorange="reversed", scaleanchor="x"),
                                showlegend=True,

                                shapes=[dict(
                                type='line',
                                x0 = x_left,
                                x1 = x_left,
                                y0 = '0',
                                y1 = '1',
                                xref = 'x',
                                yref = 'paper',
                                # line=dict(width=1,color= 'rgb(0, 255, 0)')
                                line=dict(width=1,color= 'rgb(0, 0, 0)')
                                ),
    
                                dict(
                                type='line',
                                x0 = x_right,
                                x1 = x_right,
                                y0 = '0',
                                y1 = '1',
                                xref = 'x',
                                yref = 'paper',
                                # line=dict(width=1,color= 'rgb(0, 255, 0)')
                                line=dict(width=1,color= 'rgb(0, 0, 0)')
                                ),
                                
                                dict(
                                type='line',
                                x0 = '0',
                                x1 = '1',
                                y0 = y_lower,
                                y1 = y_lower,
                                xref = 'paper',
                                yref = 'y',
                                # line=dict(width=1,color= 'rgb(0, 255, 0)')
                                line=dict(width=1,color= 'rgb(0, 0, 0)')
                                ),
                                
                                dict(
                                type='line',
                                x0 = '0',
                                x1 = '1',
                                y0 = y_upper,
                                y1 = y_upper,
                                xref = 'paper',
                                yref = 'y',
                                # line=dict(width=1,color= 'rgb(0, 255, 0)')
                                line=dict(width=1,color= 'rgb(0, 0, 0)')
                                )
    
    ],
    
                                )
                }

@app.callback(
    [Output('heatmap', 'figure'),
    Output('x-range', 'children'),
    Output('y-range', 'children'),
    Output('x-range-slider', 'max'),
    Output('y-range-slider', 'max'),
    Output('temp-range', 'children'),
    Output('temp-range-slider', 'min'),
    Output('temp-range-slider', 'max'),
    Output('temp-range-slider', 'marks'),
    Output('mean', 'children'),
    Output('min', 'children'),
    Output('max', 'children'),
    Output('stddev', 'children'),
    Output('delta_min_max', 'children'),
    Output('cv', 'children')],
    [Input('x-range-slider', 'value'),
     Input('y-range-slider', 'value'),
     Input('temp-range-slider', 'value'),
     Input('memory', 'data')])
def update_heatmap(x_range_values, y_range_values, temp_range_values, data):
    df = pd.read_json(data, orient='split')
    df_roi = df.copy()
    
    print(df_roi.values)

    df_roi.iloc[:, :x_range_values[0]] = np.nan
    df_roi.iloc[:, x_range_values[1]:] = np.nan
    
    df_roi.iloc[:y_range_values[0], :] = np.nan
    df_roi.iloc[y_range_values[1]:, :] = np.nan
    
    # set max value of range sliders
    x_range_slider = df.shape[1]
    y_range_slider = df.shape[0]
    
    # convert dataframe to numpy array
    na = df_roi.to_numpy()
    print(na)

    mean_val = np.round(np.nanmean(na), decimals = 1)
    min_val = np.round(np.nanmin(na), decimals = 1)
    max_val =  np.round(np.nanmax(na), decimals = 1)
    delta_min_max = np.round(max_val - min_val, decimals = 3)
    stddev = np.round(np.nanstd(na), decimals = 1)
    
    cv = np.round(stddev / mean_val, decimals = 1) * 100
    
    x_left = x_range_values[1]
    x_right = x_range_values[0]
    y_lower = y_range_values[1]
    y_upper = y_range_values[0]
    
    temp_slider_lower = temp_range_values[0]
    temp_slider_upper = temp_range_values[1]
    
    marks={

        60: {'label': '60'},
        80: {'label': '80'},
        100: {'label': '100'},
        120: {'label': '120'},
        140: {'label': '140'}
    }
    
    marks = {}
    for i in range(int(min_val - 1), int(max_val + 1), 1):
        marks.update({i: {'label': str(i)}})
    
    return create_heatmap(df, x_left, x_right, y_lower, y_upper, temp_slider_lower, temp_slider_upper), 'ROI x-range: {}'.format(x_range_values), 'ROI y-range: {}'.format(y_range_values), x_range_slider, y_range_slider, 'Temp-range: {}'.format(temp_range_values), min_val - 1, max_val + 1, marks, 'mean: {}°C'.format(mean_val), 'min: {}°C'.format(min_val), 'max: {}°C'.format(max_val), 'Δ min,max: {}°C'.format(delta_min_max), 'Stdev: {}°C'.format(stddev), 'CV: {}%'.format(cv) 


if __name__ == '__main__':
    # app.run_server(debug=True)
    # app.run_server(debug=False)
    
    # app.run_server(debug=True, host='0.0.0.0')
    # app.run_server(debug=False, host='0.0.0.0')
    app.run_server(debug=False, host='0.0.0.0', port=80)
