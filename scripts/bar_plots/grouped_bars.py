import plotly.graph_objects as go
import numpy as np

settings = ["Comp. Setting 1", "Comp. Setting 2", "Comp. Setting 3", "Comp. Setting 4", "Comp. Setting 5", "Comp. Setting 6", "Comp. Setting 7"]
skill_A_names = ["Skill A: Gcd", "Skill A: Polygon Rotation", "Skill A: Circle", "Skill A: Prob No Fixed", "Skill A: Prob No Fixed", "Skill A: Polygon Color", "Skill A: Grid Chip"]
skill_B_names = ["Skill B: Polynomial Roots", "Skill B: Pattern Matching", "Skill B: Func Intersection", "Skill B: Func Intersection", "Skill B: Matrix Rank", "Skill B: Prob No Fixed", "Skill B: Prob No Fixed"]
zero_shot_A = [33, 6, 13, 5, 5, 24, 4]
finetuned_A = [61, 22, 39, 22, 25, 50, 48]
zero_shot_B = [5, 13, 21, 20, 19, 5, 18]
finetuned_B = [37, 82, 70, 68, 75, 25, 22]
zero_shot_AB = [10, 5, 30, 6, 30, 0, 1]
finetuned_AB = [10, 20, 30, 6, 38, 0, 3]

x_offsets = [-0.15, 0, 0.15]  # Skill A, B, A+B at each setting
x_base = np.arange(len(settings)) * 0.6  # Reduce spacing between settings

fig = go.Figure()

# Draw bars in order for legend grouping
fig.add_bar(x=x_base + x_offsets[0], y=zero_shot_A, name='Before RL - Skill A (ID)', marker_color='blue', width=0.15, legendgroup='Before RL')
fig.add_bar(x=x_base + x_offsets[1], y=zero_shot_B, name='Before RL - Skill B (ID)', marker_color='green', width=0.15, legendgroup='Before RL')
fig.add_bar(x=x_base + x_offsets[2], y=zero_shot_AB, name='Before RL - Skill A+B (OOD)', marker_color='orange', width=0.15, legendgroup='Before RL')

fig.add_bar(x=x_base + x_offsets[0], y=finetuned_A, name='After RL - Skill A (ID)', marker_color='lightblue', opacity=0.5, width=0.15, legendgroup='After RL')
fig.add_bar(x=x_base + x_offsets[1], y=finetuned_B, name='After RL - Skill B (ID)', marker_color='lightgreen', opacity=0.5, width=0.15, legendgroup='After RL')
fig.add_bar(x=x_base + x_offsets[2], y=finetuned_AB, name='After RL - Skill A+B (OOD)', marker_color='lightsalmon', opacity=0.5, width=0.15, legendgroup='After RL')

# Annotate improvements
for i in range(len(settings)):
    # Annotations for zero-shot values (below the bars)
    fig.add_annotation(x=x_base[i] + x_offsets[0], y=zero_shot_A[i] - 5, text=f'{zero_shot_A[i]}', font=dict(color='blue', size=10, weight='bold'), showarrow=False)
    fig.add_annotation(x=x_base[i] + x_offsets[1], y=zero_shot_B[i] - 5, text=f'{zero_shot_B[i]}', font=dict(color='green', size=10, weight='bold'), showarrow=False)
    fig.add_annotation(x=x_base[i] + x_offsets[2], y=zero_shot_AB[i] - 5, text=f'{zero_shot_AB[i]}', font=dict(color='orange', size=10, weight='bold'), showarrow=False)
    
    # Annotations for finetuned values (above the bars)
    fig.add_annotation(x=x_base[i] + x_offsets[0], y=finetuned_A[i] + 3, text=f'{finetuned_A[i]} (+{finetuned_A[i]-zero_shot_A[i]})', font=dict(color='black', size=10, weight='bold'), showarrow=False)
    fig.add_annotation(x=x_base[i] + x_offsets[1], y=finetuned_B[i] + 3, text=f'{finetuned_B[i]} (+{finetuned_B[i]-zero_shot_B[i]})', font=dict(color='black', size=10, weight='bold'), showarrow=False)
    fig.add_annotation(x=x_base[i] + x_offsets[2], y=finetuned_AB[i] + 3, text=f'{finetuned_AB[i]} (+{finetuned_AB[i]-zero_shot_AB[i]})', font=dict(color='black', size=10, weight='bold'), showarrow=False)

fig.update_layout(
    barmode='overlay',  # Overlay bars of the same skill
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        tickmode='array',
        tickvals=x_base,
        ticktext=[f"{settings[i]}<br>{skill_A_names[i]}<br>{skill_B_names[i]}" for i in range(len(settings))],
        tickangle=-45,
        tickfont=dict(weight='bold')
    ),
    yaxis=dict(
        title=dict(text='Accuracy (%)', font=dict(weight='bold')), 
        range=[0, 100],
        tickfont=dict(weight='bold')
    ),
    legend=dict(
        orientation='h', 
        y=0.95, 
        x=0.5, 
        xanchor='center', 
        yanchor='top',
        font=dict(weight='bold'),
        groupclick='toggleitem',
        itemsizing='constant',
        itemwidth=30,
        tracegroupgap=5,
        traceorder='grouped',
        bordercolor='black',
        borderwidth=1,
        bgcolor='rgba(255,255,255,0.9)',
        yref='paper',
        xref='paper'
    )
)

fig.write_html("grouped_bars.html")
