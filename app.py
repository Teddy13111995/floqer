import pandas as pd
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

csv_file_path = 'salaries.csv'
salaries_df = pd.read_csv(csv_file_path)

salaries_df['work_year'] = salaries_df['work_year'].astype(int)

summary_df = salaries_df.groupby('work_year').agg(
    total_jobs=('job_title', 'count'),
    average_salary_usd=('salary_in_usd', 'mean')
).reset_index()

app = Dash(__name__)


app.layout = html.Div([
    html.H1("Machine Learning Engineer Salaries"),

    html.H2("Summary Table"),
    dash_table.DataTable(
        id='summary-table',
        columns=[{"name": i, "id": i} for i in summary_df.columns],
        data=summary_df.to_dict('records'),
        sort_action='native',
        row_selectable='single',
        selected_rows=[],
        style_cell={
            'textAlign': 'left',
            'whiteSpace': 'normal',
        },
        style_data={
            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
    ),

    html.H2("Total Jobs Over Years"),
    dcc.Graph(id='line-graph'),

    html.Div(id='job-details')
])



@app.callback(
    Output('line-graph', 'figure'),
    Input('summary-table', 'data')
)
def update_line_graph(data):
    df = pd.DataFrame(data)
    fig = px.line(df, x='work_year', y='total_jobs', title='Total Jobs Over Years')
    fig.update_xaxes(type='category')
    fig.update_yaxes(tickformat='d')
    return fig



@app.callback(
    Output('job-details', 'children'),
    [Input('summary-table', 'selected_rows')],
    [Input('summary-table', 'data')]
)
def display_job_details(selected_rows, rows):
    if selected_rows:
        selected_year = rows[selected_rows[0]]['work_year']
        year_df = salaries_df[salaries_df['work_year'] == selected_year]
        job_counts = year_df['job_title'].value_counts().reset_index()
        job_counts.columns = ['job_title', 'count']

        return html.Div([
            html.H3(f"Job Titles for {selected_year}"),
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in job_counts.columns],
                data=job_counts.to_dict('records'),
                style_cell={
                    'textAlign': 'center',
                    'whiteSpace': 'normal',
                },
                style_data={
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },
            )
        ])
    return html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)
