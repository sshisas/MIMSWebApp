
import numpy
import pandas as pd
import glob
import plotly
import chart_studio.plotly as py
import plotly.graph_objs as go
import chart_studio
import plotly.io as pio
from outliers import smirnov_grubbs as grubbs

path = 'C:\\Users\\User\\Dropbox\\MIMS_Data'  # use your path
all_files = glob.glob(path + "/*.lvm")

JULIAN_DATE_IDX = 1
TEMP_IDX = 2
WATER_IDX = 3
N2_IDX = 4
O2_IDX = 5
Ar_IDX = 6
O2_Ar_IDX = 7
N2_Ar_IDX = 8
TOTAL_IDX = 9
DMS_62_IDX = 10
DMS_47_IDX = 11
BROMOFORM_173_IDX = 12
BROMOFORM_171_IDX = 13
BROMOFORM_175_IDX = 14
ISOPRENE_67_IDX = 15
ISOPRENE_68_IDX = 16
ISOPRENE_53_IDX = 17


col_str = ["zero", "Julian-Date", "Temperature", "Water", "N2", "O2", "Ar", "O2-Ar", "N2-Ar", "Total", "DMS-62",
           "DMS-47", "Bromoform-173", "Bromoform-171", "Bromoform-175", "Isoprene-67", "Isoprene-68", "Isoprene-53"]

li = []

for filename in all_files:
    df = pd.read_csv(filename, sep='\t', skiprows=21, header=0)
    li.append(df)


frame = pd.concat(li, axis=0, ignore_index=True)


sort = frame.sort_values('Untitled', ascending=True)

chart_studio.tools.set_credentials_file(
    username='retirotigre', api_key='1CRlTIJ3MQwnaossRixV')

for col in range(2, 18):
    trace1 = go.Scatter(
        x=sort.iloc[:, JULIAN_DATE_IDX].to_list(),
        y=grubbs.test((sort.iloc[:, col]).to_list(), alpha=0.99),
        xaxis='x1',
        yaxis='y1',
        marker=go.scatter.Marker(
            color='rgb(26, 118, 255)'
        ),
        line_shape='spline',
        line_smoothing=1.3,
    )

    data = [trace1]

    layout = go.Layout(
        plot_bgcolor='#f6f7f8',
        paper_bgcolor='#f6f7f8',
        title=go.layout.Title(
            text=col_str[col],
            xref='paper',
            font=dict(
                family='Open Sans, sans-serif',
                size=22, 
                color='#000000'
            )
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Julian Date',
                font=dict(
                    family='Open Sans, sans-serif',
                    size=18,
                    color='#000000'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            showexponent='all',
            exponentformat='e',
            title=go.layout.yaxis.Title(
                text=col_str[col],
                font=dict(
                    family='Open Sans, sans-serif',
                    size=18,
                    color='#000000'
                )
            )
        )
    )

    fig = go.Figure(data=data, layout=layout)
    #py.plot(fig, filename='Ar')
    pio.write_html(fig, file= col_str[col] + ".html", auto_open=True)

