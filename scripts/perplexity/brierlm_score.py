import plotly.graph_objects as go
import numpy as np

def plot_brierlm_long_run():
    """
    Visualizes the expected BrierLM score in the long run.
    
    BrierLM aggregates Brier scores across n-grams (n=1,2,3,4) using
    geometric average, and is scaled to 0-100 for readability.
    
    Per-token Brier score ranges from -1 to +1.
    BrierLM scales this to 0-100 where:
    - 0 = worst (all confident errors)
    - 50 = random guessing baseline
    - 100 = perfect predictions
    """
    
    fig = go.Figure()
    
    # Probability range
    probs = np.linspace(0.001, 0.999, 200)
    
    # ==========================================
    # Expected Brier Scores (per token, -1 to +1)
    # ==========================================
    # Diverse Errors: E[Score] = 2p - p²
    diverse_brier = 2*probs - probs**2
    
    # Concentrated Errors: E[Score] = 2p - (p² + (1-p)²)
    concentrated_brier = 2*probs - (probs**2 + (1-probs)**2)

    # ==========================================
    # Scale to BrierLM (0-100)
    # ==========================================
    # Original Brier: [-1, +1] → BrierLM: [0, 100]
    # Formula: BrierLM = (Brier + 1) * 50
    diverse_brierlm = (diverse_brier + 1) * 50
    concentrated_brierlm = (concentrated_brier + 1) * 50

    # ==========================================
    # Add Fill Between (Overconfidence Penalty Region)
    # ==========================================
    fig.add_trace(
        go.Scatter(
            x=np.concatenate([probs, probs[::-1]]),
            y=np.concatenate([diverse_brierlm, concentrated_brierlm[::-1]]),
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
            y=diverse_brierlm,
            mode='lines',
            name='<b>Diverse Errors</b><br>(Uniform over wrong tokens)',
            line=dict(color='#2ecc71', width=4),
            hovertemplate="p = %{x:.2f}<br>BrierLM = %{y:.1f}<extra></extra>"
        )
    )

    # ==========================================
    # Concentrated Errors Line (Worst Case)
    # ==========================================
    fig.add_trace(
        go.Scatter(
            x=probs, 
            y=concentrated_brierlm,
            mode='lines',
            name='<b>Concentrated Errors</b><br>(All mass on one wrong token)',
            line=dict(color='#e74c3c', width=4, dash='dash'),
            hovertemplate="p = %{x:.2f}<br>BrierLM = %{y:.1f}<extra></extra>"
        )
    )

    # ==========================================
    # Reference Lines
    # ==========================================
    # Random baseline (p=0.5 for binary, but for LM it's vocab-dependent)
    fig.add_hline(
        y=50, 
        line_width=2, 
        line_color="gray", 
        line_dash="dot",
        opacity=0.7,
        annotation_text="Random Baseline",
        annotation_position="right"
    )

    # ==========================================
    # Annotations
    # ==========================================
    fig.add_annotation(
        x=0.5,
        y=65,
        text="<b>Overconfidence<br>Penalty</b>",
        showarrow=False,
        font=dict(size=14, color='#c0392b'),
        bgcolor='rgba(255,255,255,0.8)'
    )
    
    fig.add_annotation(
        x=0.15,
        y=30,
        text="<b>Confident errors<br>penalized here</b>",
        showarrow=True,
        arrowhead=2,
        ax=40,
        ay=-30,
        font=dict(size=12, color='#e74c3c')
    )
    
    fig.add_annotation(
        x=0.9,
        y=95,
        text="<b>High accuracy<br>region</b>",
        showarrow=True,
        arrowhead=2,
        ax=-40,
        ay=30,
        font=dict(size=12, color='#27ae60')
    )

    # ==========================================
    # Layout
    # ==========================================
    fig.update_layout(
        title=dict(
            text="<b>Expected BrierLM Score (0-100 Scale)</b>",
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
            title="<b>BrierLM Score</b>",
            range=[0, 105],
            tickvals=[0, 25, 50, 75, 100],
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

    # Save output
    output_file = "brierlm_score.html"
    fig.write_html(output_file)
    print(f"Plot saved to {output_file}")
    
    print("\n--- Caption for Blog ---")
    print("""
Expected BrierLM score as a function of probability p assigned to the correct token, 
scaled to 0-100 (higher is better). The green curve represents the best case where 
errors are uniformly distributed across wrong tokens. The red dashed curve shows 
the worst case where all error probability mass is concentrated on a single wrong 
token. The shaded region illustrates the penalty for overconfidence on wrong predictions.
""")

if __name__ == "__main__":
    plot_brierlm_long_run()
