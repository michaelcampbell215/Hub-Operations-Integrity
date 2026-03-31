import matplotlib.pyplot as plt
import pandas as pd

# Data from your 10-flight simulation
data = {
    'Flight': ['AA1001', 'AA1002', 'AA1003', 'AA1004', 'AA1005', 'AA2001', 'AA2002', 'AA2003', 'AA2004', 'AA2005'],
    'Savings': [7425, 6682, 36272, 4072, 2970, 26188, 2228, 21655, 7425, 7425],
    'Decision': ['PUSH', 'PUSH', 'HOLD', 'HOLD', 'PUSH', 'HOLD', 'PUSH', 'HOLD', 'PUSH', 'PUSH']
}
df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))

# Assign colors: AA Blue for Holds, AA Red for Pushes
colors = ['#003366' if d == 'HOLD' else '#C00000' for d in df['Decision']]

plt.bar(df['Flight'], df['Savings'], color=colors, edgecolor='black', alpha=0.8)

plt.title('Net Savings per Flight: Strategic Hold vs. Regulatory Push', fontsize=14, fontweight='bold')
plt.ylabel('Total Cost Avoidance ($)', fontsize=12)
plt.xlabel('Flight Number', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Adding a legend
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='#003366', lw=4, label='Strategic Hold (High Yield)'),
                   Line2D([0], [0], color='#C00000', lw=4, label='Regulatory Push (Network Integrity)')]
plt.legend(handles=legend_elements)

plt.tight_layout()
plt.savefig('net_savings_per_flight.png')
plt.show()


# Aggregate totals from your summary
ops_metrics = {
    'Metric': ['Expedited Bags', 'Bags Pulled', 'Standbys Cleared'],
    'Count': [370, 93, 43]
}
df_ops = pd.DataFrame(ops_metrics)

plt.figure(figsize=(10, 5))

# Use a professional palette
plt.barh(df_ops['Metric'], df_ops['Count'], color=['#2E8B57', '#C00000', '#ffd299'], edgecolor='black')

plt.title('Hub Operations Recovery: Total Throughput (4-Hour Window)', fontsize=14, fontweight='bold')
plt.xlabel('Total Units Processed', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.5)

# Annotate bars with the actual numbers
for index, value in enumerate(df_ops['Count']):
    plt.text(value + 5, index, str(value), va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('hub_ops_volumes.png')
plt.show()