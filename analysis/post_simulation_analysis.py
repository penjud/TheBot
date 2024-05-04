import pandas as pd

results = pd.read_csv('simulation_results.csv')
results['cumulative_profit'] = results['profit'].cumsum()
analysis = results.groupby('strategy').agg({'cumulative_profit': 'max'})
print(analysis)
