import pandas as pd
import plotly.graph_objects as go

file_path = "../02_Code/05_Quantitative/Outputs/max_merged_df.csv"
df = pd.read_csv(file_path)
df = df.iloc[141:]


df.dropna(subset=['Proton_class', 'Flare_Class', 'Kp_Class'], inplace=True)

#convert classes from floats to ints
df['Proton_class'] = df['Proton_class'].astype(int)
df['Flare_Class'] = df['Flare_Class'].astype(int)
df['Kp_Class'] = df['Kp_Class'].astype(int)

#Grouping by the three columns and counting the occurrences
flows = df.groupby(['Proton_class', 'Flare_Class', 'Kp_Class']).size().reset_index(name='count')

#Define custom labels, (S, R, G)
custom_labels = {
    'Proton_class - 0': 'Custom Proton 0',
    'Proton_class - 1': 'S1',
    'Proton_class - 2': 'S2',
    'Proton_class - 3': 'S3',
    'Proton_class - 4': 'S4',
    'Proton_class - 5': 'S5',

    'Flare_Class - 0': 'R0',
    'Flare_Class - 1': 'R1',
    'Flare_Class - 2': 'R2',
    'Flare_Class - 3': 'R3',
    'Flare_Class - 4': 'R4',
    'Flare_Class - 5': 'R5',

    'Kp_Class - 0': 'G0',
    'Kp_Class - 1': 'G1',
    'Kp_Class - 2': 'G2',
    'Kp_Class - 3': 'G3',
    'Kp_Class - 4': 'G4',
    'Kp_Class - 5': 'G5'
}

#Generate new labels
labels = []
for col in ['Proton_class', 'Flare_Class', 'Kp_Class']:
    for i in range(6):  #values range from 0 to 5
        original_label = f"{col} - {i}"
        labels.append(custom_labels[original_label])

#source-target pairs for Sankey diagram
source = []
target = []
value = []
flow_colors = []  # List to store flow (link) colors

#Custom color list for each individual node on graph
node_colors = [
    '#92d051',
    '#f6eb13',
    '#ffc800',
    '#ff9600',
    '#ff0000',
    '#c70100',
    '#92d051',
    '#f6eb13',
    '#ffc800',
    '#ff9600',
    '#ff0000',
    '#c70100',
    '#92d051',
    '#f6eb13',
    '#ffc800',
    '#ff9600',
    '#ff0000',
    '#c70100',
]

def hex_to_rgba(hex_color, alpha=0.3):
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    return f"rgba({r}, {g}, {b}, {alpha})"


for _, row in flows.iterrows():
    #Flare_Class -> Proton_class
    source_idx = labels.index(custom_labels[f"Flare_Class - {int(row['Flare_Class'])}"])
    target_idx = labels.index(custom_labels[f"Proton_class - {int(row['Proton_class'])}"])
    source.append(source_idx)
    target.append(target_idx)
    value.append(row['count'])
    #Assign color of the flow to the source node's color with transparency
    flow_colors.append(hex_to_rgba(node_colors[source_idx], 0.5))

    #Proton_class -> Kp_Class
    source_idx = labels.index(custom_labels[f"Proton_class - {int(row['Proton_class'])}"])
    target_idx = labels.index(custom_labels[f"Kp_Class - {int(row['Kp_Class'])}"])
    source.append(source_idx)
    target.append(target_idx)
    value.append(row['count'])
    #Assign color of the flow to the source node's color with transparency
    flow_colors.append(hex_to_rgba(node_colors[source_idx], 0.5))

#Ensure the node_colors list has enough colors to cover all the labels
node_colors = node_colors[:len(labels)]  # Trim or extend the color list to match the number of nodes

#Create Sankey diagram using Plotly with custom node colors
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,
        color=node_colors  # Apply custom color list for nodes
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=flow_colors  # Use the list of flow colors to match the source node's color
    ))])

#Create custom labels for columns
fig.update_layout(
    annotations=[
        #Add label for Flare_class column
        dict(
            x=0.1, y=1.05,
            xref='paper', yref='paper',
            text='Radio Blackout',
            showarrow=False,
            font=dict(size=12, color='black'),
        ),
        #Add label for Proton_class column
        dict(
            x=0.5, y=1.05,
            xref='paper', yref='paper',
            text='Solar Radiation Storm',
            showarrow=False,
            font=dict(size=12, color='black'),
        ),
        #Add label for Kp_class column
        dict(
            x=0.9, y=1.05,
            xref='paper', yref='paper',
            text='Geomagnetic Storm',
            showarrow=False,
            font=dict(size=12, color='black'),
        ),
    ]
)
fig.update_layout(title_text="Alluvial Diagram of  R, S, and G Warnings, 1994 Onwards", font_size=12)
fig.show()