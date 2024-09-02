import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from queries import top_3_users, average_transaction_amount, users_with_no_transactions, calculate_total_spent_by_user

app = dash.Dash(__name__)

# Prepare Data for Visualization
top_users = top_3_users()
avg_transaction = average_transaction_amount()
users_no_txn = users_with_no_transactions()
total_spent = calculate_total_spent_by_user()

# Define the layout
app.layout = html.Div(children=[
    html.H1(children='Database Interaction and Visualization'),

    html.Div(children='''
        Bar chart of top 3 users by total spent.
    '''),

    dcc.Graph(
        id='bar-chart',
        figure=px.bar(top_users, x='name', y='total_spent', title='Top 3 Users by Total Spent')
    ),

    html.Div(children=f'Average transaction amount: ${avg_transaction:.2f}.'),

    dcc.Graph(
        id='total-spent',
        figure=px.line(total_spent, x='name', y='total_spent', title='Total Spent by Each User')
    ),

    html.Div(children='Users with no transactions:'),

    # Conditional rendering of the table
    html.Div(
        children=[
            html.Table(
                # Header
                [html.Tr([html.Th(col) for col in users_no_txn.columns])] +
                
                # Body
                [html.Tr([html.Td(users_no_txn.iloc[i][col]) for col in users_no_txn.columns])
                 for i in range(len(users_no_txn))]
            )
        ] if not users_no_txn.empty else html.P('No users without transactions.')
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
