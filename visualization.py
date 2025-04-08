import streamlit as st
import pandas as pd
import plotly.express as px

# Title for the dashboard
st.title("Battle Simulation Results Dashboard")

# Load the simulation summary CSV file
data = pd.read_csv('simulation_summary.csv')

# Sidebar filter: Select a range of cleric counts
min_count = int(data['num_clerics'].min())
max_count = int(data['num_clerics'].max())
cleric_range = st.sidebar.slider(
    'Select cleric count range',
    min_value=min_count,
    max_value=max_count,
    value=(min_count, max_count)
)
filtered_data = data[(data['num_clerics'] >= cleric_range[0]) & (data['num_clerics'] <= cleric_range[1])]

st.write(f"Showing results for cleric counts between {cleric_range[0]} and {cleric_range[1]}.")

# --- Win Rate Plot ---

# Calculate error values for win rate (plotly expects the error magnitude)
filtered_data['win_err_lower'] = filtered_data['win_rate'] - filtered_data['ci_win_lower']
filtered_data['win_err_upper'] = filtered_data['ci_win_upper'] - filtered_data['win_rate']

fig_win = px.scatter(
    filtered_data,
    x='num_clerics',
    y='win_rate',
    error_y=filtered_data['win_err_upper'],
    error_y_minus=filtered_data['win_err_lower'],
    title='Win Rate vs. Number of Clerics',
    labels={'num_clerics': 'Number of Clerics', 'win_rate': 'Win Rate'},
    template='plotly_white'
)
fig_win.update_traces(mode='lines+markers')
st.plotly_chart(fig_win, use_container_width=True)

# --- Average Rounds Plot ---

# Calculate error values for average rounds
filtered_data['rounds_err_lower'] = filtered_data['avg_rounds'] - filtered_data['ci_rounds_lower']
filtered_data['rounds_err_upper'] = filtered_data['ci_rounds_upper'] - filtered_data['avg_rounds']

fig_rounds = px.scatter(
    filtered_data,
    x='num_clerics',
    y='avg_rounds',
    error_y=filtered_data['rounds_err_upper'],
    error_y_minus=filtered_data['rounds_err_lower'],
    title='Average Rounds vs. Number of Clerics',
    labels={'num_clerics': 'Number of Clerics', 'avg_rounds': 'Average Rounds'},
    template='plotly_white'
)
fig_rounds.update_traces(mode='lines+markers')
st.plotly_chart(fig_rounds, use_container_width=True)
