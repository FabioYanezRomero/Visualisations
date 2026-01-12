import plotly.graph_objects as go
import numpy as np

def plot_brier_long_run():
    """
    Creates a visualization of the expected Brier score in the long run,
    showing the difference between diverse and concentrated error strategies.
    
    For your blog post, use this table to explain the discrete scenarios:
    
    | Scenario          | I(x₁=y) | I(x₂=y) | I(x₁=x₂) | Score |
    |-------------------|---------|---------|----------|-------|
    | Both Correct      | 1       | 1       | 1        | **1** |
    | Partial Correct   | 1       | 0       | 0        | **1** |
    | Diverse Error     | 0       | 0       | 0        | **0** |
    | Confident Error   | 0       | 0       | 1        | **-1**|
    """
    
    fig = go.Figure()
    
    # Probability range
    probs = np.linspace(0.001, 1, 200)
    
    # ==========================================
    # Expected Scores for Two Strategies
    # ==========================================
    # Diverse Errors: E[Score] = 2p - p² (collision only when correct)
    diverse_score = 2*probs - probs**2
    
    # Concentrated Errors: E[Score] = 2p - (p² + (1-p)²) (collision on wrong too)
    concentrated_score = 2*probs - (probs**2 + (1-probs)**2)

    # ==========================================
    # Add Fill Between (Overconfidence Penalty)
    # ==========================================
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([probs, probs[::-1]]),
            y=np.concatenate([diverse_score, concentrated_score[::-1]]),
            fill='toself',
            fillcolor='rgba(231, 76, 60, 0.15)',
            line=dict(color='rgba(255,255,255,0)'),
            name='<b>Overconfidence Penalty</b>',
            showlegend=True,
            hoverinfo='skip'
        )
    )

    # ==========================================
    # Diverse Errors Line (Best Case)
    # ==========================================
    fig.add_trace(
        go.Scatter(
            x=probs, 
            y=diverse_score,
            mode='lines',
            name='<b>Diverse Errors</b><br>(Uniform over wrong tokens)',
            line=dict(color='#2ecc71', width=4),
            hovertemplate="p = %{x:.2f}<br>E[Score] = %{y:.3f}<extra></extra>"
        )
    )

    # ==========================================
    # Concentrated Errors Line (Worst Case)
    # ==========================================
    fig.add_trace(
        go.Scatter(
            x=probs, 
            y=concentrated_score,
            mode='lines',
            name='<b>Concentrated Errors</b><br>(All mass on one wrong token)',
            line=dict(color='#e74c3c', width=4, dash='dash'),
            hovertemplate="p = %{x:.2f}<br>E[Score] = %{y:.3f}<extra></extra>"
        )
    )

    # ==========================================
    # Annotations
    # ==========================================
    # Annotation for the penalty region
    fig.add_annotation(
        x=0.5,
        y=0.25,
        text="<b>Overconfidence<br>Penalty</b>",
        showarrow=False,
        font=dict(size=14, color='#c0392b'),
        bgcolor='rgba(255,255,255,0.8)'
    )
    
    # Annotation for key insight
    fig.add_annotation(
        x=0.15,
        y=-0.3,
        text="<b>Confident errors<br>are penalized</b>",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-40,
        font=dict(size=12, color='#e74c3c')
    )

    # ==========================================
    # Layout
    # ==========================================
    fig.update_layout(
        title=dict(
            text="<b>Expected Brier Score: Diverse vs Concentrated Errors</b>",
            font=dict(size=22),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="<b>Probability Assigned to Correct Token (p)</b>",
            range=[0, 1],
            tickfont=dict(size=13),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            title="<b>Expected Score</b>",
            range=[-0.6, 1.1],
            tickfont=dict(size=13),
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        height=550,
        width=900,
        template="plotly_white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5,
            font=dict(size=13)
        ),
        font=dict(family="Arial, sans-serif", size=14),
        margin=dict(t=80, b=100)
    )
    
    # Zero line for reference
    fig.add_hline(y=0, line_width=1.5, line_color="gray", opacity=0.7)

    # Save output
    output_file = "brier_score.html"
    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")
    
    # Print the markdown table for the blog
    print("\n--- Markdown Table for Blog ---")
    print("""
| Scenario | I(x₁=y) | I(x₂=y) | I(x₁=x₂) | Score |
|----------|---------|---------|----------|-------|
| Both Correct | 1 | 1 | 1 | **1** |
| Partial Correct | 1 | 0 | 0 | **1** |
| Diverse Error | 0 | 0 | 0 | **0** |
| Confident Error | 0 | 0 | 1 | **-1** |
""")

if __name__ == "__main__":
    plot_brier_long_run()
