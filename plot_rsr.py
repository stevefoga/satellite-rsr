import os
import sys
import json
import base64
#import time

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
#import plotly.io as pio
import pandas as pd


# defaults
REPO_URL = "https://github.com/stevefoga/satellite-rsr"
REPO_IMG = "assets/GitHub-Mark-32px.png"
SATELLITE_SPECTRA = "data/rsr_ALL.csv"
ENVIRONMENT_SPECTRA = "data/env_spectra_ALL.csv"
#HTML_FILE_OUT = "html_out/html_out_{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
X_AXIS_LABEL = "Wavelength (\u03bcm)"
Y_AXIS_LABEL = "Relative Spectral Response (W)"

# example modified from https://dash.plotly.com/interactive-graphing
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# display github logo with repo link
data_uri = base64.b64encode(open(REPO_IMG, 'rb').read()).decode('utf-8')

# Open data
base_dir = os.path.dirname(os.path.realpath(__file__))
csv_in = os.path.join(base_dir, SATELLITE_SPECTRA)
env_in = os.path.join(base_dir, ENVIRONMENT_SPECTRA)
_df = pd.read_csv(csv_in)
_edf = pd.read_csv(env_in)
# filter data frames for very low RSR values
df = _df[_df["rsr_watts"] > 0.001]
e_df = _edf[_edf["rsr_watts"] > 0.001]

sensor_column = "sensor"
unique_sensors = pd.unique(df[sensor_column])

# initial plot
fig = px.line(df, x="wavelength_um", y="rsr_watts", color="band",
              labels={"wavelength_um": X_AXIS_LABEL,
                      "rsr_watts": Y_AXIS_LABEL
                      }
              )

fig.update_layout(clickmode='event+select')
fig.update_traces(marker_size=20, mode="markers+lines", hovertemplate=None)

app.layout = html.Div([

    # sensor-specific checklist
    # ref: https://plotly.com/python/line-charts/
    dcc.Checklist(
            id="checklist",
            options=[{"label": x, "value": x} for x in unique_sensors],
            value=["l8_oli"],
            labelStyle={'display': 'inline-block'}
        ),

    # color graphs by unique sensor
    dcc.Checklist(
        id="checklist-sensor",
        options=[{"label": "Color by sensor", "value": sensor_column
                 }],
        value=[],
        labelStyle={'display': 'inline-block'}
    ),

    # display github logo with repo link
    html.A(html.Img(src="data:image/png;base64,{0}".format(data_uri)),
           href=REPO_URL,
           target="_blank"
           ),

    #html.P("Hovermode"),
    #dcc.RadioItems(
    #    id='hovermode',
    #    labelStyle={'display': 'inline-block'},
    #    options=[{'label': x, 'value': x}
    #             for x in ['x', 'x unified', 'closest']],
    #    value='closest'
    #),
    #dcc.Graph(id="graph", figure=fig),

    # render graph
    dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),

    html.Div(className='row', children=[

        # basic hover tool
        html.Div([
            dcc.Markdown("""
                **Hover Data**
                
                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])

# write out HTML file
#pio.write_html(fig, file=HTML_FILE_OUT, auto_open=True)
#print("HTML file written to {}".format(HTML_FILE_OUT))

# basic hover tool
@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)

'''
@app.callback(
    Output("graph", "figure"),
    [Input("hovermode", "value")],
    [State('graph', 'figure')])
def update_hovermode(mode, fig_json):
    fig = go.Figure(fig_json)
    fig.update_layout(hovermode=mode)
    return fig
'''

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    Input('basic-interactions', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


@app.callback(
    Output("basic-interactions", "figure"),
    [Input("checklist", "value"),
     Input("checklist-sensor", "value")])


def update_line_chart(unique_sensors, color_type):
    if not color_type:
        color_type = "band"
    if type(color_type) == list:
        color_type = color_type[0]
    mask = df.sensor.isin(unique_sensors)
    fig = go.Figure()

    if not df[mask].empty:  # otherwise JS throws error if all boxes unchecked
        # Plotly express (px) works for simple plots, but does not support multiple layers
        #   Use graph_objects (go) instead, which is the lower-level function under px
        #fig = px.line(df[mask], x="wavelength_um", y="rsr_watts", color=color_type,
                        #labels = {"wavelength_um": "Wavelength (\u03bcm)",
                        #"rsr_watts": "Relative Spectral Response (W)"},
                        # hover_name="band",
                        # hover_data=["sensor", "wavelength_um", "rsr_watts"]
        # )

        # make plot object for each environmental RSR
        for ect in e_df["spectra_type"].unique():
            edf_ct = e_df[e_df["spectra_type"] == ect]
            fig.add_trace(go.Scatter(x=edf_ct["wavelength_um"],
                                     y=edf_ct["rsr_watts"],
                                     fill='tozeroy',
                                     name=ect)
                          )
        # make plot object for each sensor RSR
        for ct in df[mask][color_type].unique():
            # apply mask
            ct_mask = (df[color_type] == ct) & mask
            df_ct = df[ct_mask]

            # do plot
            fig.add_trace(go.Scatter(x=df_ct["wavelength_um"],
                                     y=df_ct["rsr_watts"],
                                     name=ct)
                          )

        # add labels to final figure
        fig.update_layout(
            #title="Plot Title",
            xaxis_title=X_AXIS_LABEL,
            yaxis_title=Y_AXIS_LABEL,
            #legend_title="",
            #font=dict(
            #    family="Courier New, monospace",
            #    size=18,
            #    color="RebeccaPurple"
            #)
        )

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
