import numpy as np
import plotly.graph_objects as go

def plot_loss_likelihood():
    # Define probability range from epsilon to 1
    # We avoid 0 exactly to avoid log(0) which is undefined (-inf)
    epsilon = 1e-10
    p = np.linspace(epsilon, 1.0, 1000)
    
    # Calculate Negative Log-Likelihood (NLL)
    # Loss = -log(p)
    nll = -np.log(p)
    
    # Create the plot
    fig = go.Figure()
    
    # Add the main curve
    fig.add_trace(go.Scatter(
        x=p,
        y=nll,
        mode='lines',
        name='Negative Log-Likelihood',
        line=dict(color='red', width=4)
    ))

    # Highlight the "Sweet Spot" (Diminishing Returns)
    # Let's say p from 0.7 to 0.95 is where the curve flattens but is high enough
    fig.add_shape(
        type="rect",
        x0=0.7, y0=0, x1=0.95, y1=10,
        fillcolor="green", opacity=0.1,
        layer="below", line_width=0,
    )

    # Highlight the "Infinite Penalty" Region (Rare Grammar)
    # Low probability region where penalty is high
    fig.add_shape(
        type="rect",
        x0=0, y0=0, x1=0.2, y1=10,
        fillcolor="orange", opacity=0.1,
        layer="below", line_width=0,
    )

    # Add annotation for the infinite penalty/rare grammar
    fig.add_annotation(
        x=0.15,
        y=4,
        text="<b>High Penalty Region:<br>Learns Rare Grammar</b><br>(Forces model to remember<br>specific examples)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        ax=60,
        ay=-40,
        font=dict(size=14, color="darkorange")
    )

    # Add annotation for diminish returns/sweet spot
    fig.add_annotation(
        x=0.825,
        y=0.5,
        text="<b>Sweet Spot:<br>Diminishing Returns</b><br>(Correct but not Overconfident)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        ax=0,
        ay=-60,
        font=dict(size=14, color="darkgreen")
    )
    
    # Update layout with bold fonts
    fig.update_layout(
        title=dict(
            text='<b>Negative Log-Likelihood (Loss) vs. Probability (p)</b>',
            font=dict(size=24)
        ),
        xaxis_title=dict(
            text='<b>Probability of Correct Class (p)</b>',
            font=dict(size=18)
        ),
        yaxis_title=dict(
            text='<b>Loss (-log(p))</b>',
            font=dict(size=18)
        ),
        template='plotly_white',
        xaxis=dict(
            range=[0, 1.05],
            showgrid=True,
            tickfont=dict(size=14, family='Arial Black')
        ),
        yaxis=dict(
            range=[0, 8], # Cap y at 8 to focus on relevant area
            showgrid=True,
            tickfont=dict(size=14, family='Arial Black')
        ),
        showlegend=True,
        legend=dict(font=dict(size=14))
    )
    
    # Show the plot
    # fig.show()
    output_file = "loss_likelihood.html"
    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")

if __name__ == "__main__":
    plot_loss_likelihood()
