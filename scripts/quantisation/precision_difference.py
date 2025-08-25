import numpy as np
from sklearn.decomposition import PCA
import plotly.graph_objects as go

def plot_quantization_multiple_steps(n_points, initial_precision, precisions_list):
    np.random.seed(42)
    dim = 10
    data = np.random.uniform(low=-1, high=1, size=(n_points, dim))

    def quantize(arr, levels):
        min_val, max_val = arr.min(), arr.max()
        bins = np.linspace(min_val, max_val, levels)
        inds = np.digitize(arr, bins, right=True) - 1
        quantized = bins[np.clip(inds, 0, levels - 1)]
        return quantized

    # Initial precision data
    data_initial = quantize(data, initial_precision)

    # Quantize to each lower precision in the list
    quantized_sets = []
    for prec in precisions_list:
        quantized_sets.append(quantize(data, prec))

    # Concatenate for PCA
    data_concat = np.concatenate([data_initial] + quantized_sets)
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(data_concat)

    # Recover locations for each set
    initial_2d = pca_result[:n_points]
    other_2d = []
    start_idx = n_points
    for _ in precisions_list:
        other_2d.append(pca_result[start_idx:start_idx + n_points])
        start_idx += n_points

    fig = go.Figure()
    # Pick colors for each precision step
    colors = ['red', 'orange', 'green', 'purple', 'brown']

    # Draw all lines first (so they appear behind points)
    for i, (prec, points_2d) in enumerate(zip(precisions_list, other_2d)):
        color = colors[i % len(colors)]
        for j in range(n_points):
            fig.add_trace(go.Scatter(
                x=[initial_2d[j, 0], points_2d[j, 0]],
                y=[initial_2d[j, 1], points_2d[j, 1]],
                mode='lines', line=dict(color=color, width=4), showlegend=False
            ))

    # Draw initial precision points
    fig.add_trace(go.Scatter(
        x=initial_2d[:, 0], y=initial_2d[:, 1], mode='markers',
        marker=dict(color='blue', size=10, opacity=0.85, line=dict(width=3, color='black')),
        name=f'Initial Precision ({initial_precision} bits)'
    ))

    # Draw quantized points for each precision
    for i, (prec, points_2d) in enumerate(zip(precisions_list, other_2d)):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=points_2d[:, 0], y=points_2d[:, 1], mode='markers',
            marker=dict(color=color, size=10, opacity=0.85, line=dict(width=3, color='black')),
            name=f'Precision {prec} bits'
        ))

    fig.update_layout(
        title=dict(
            text=f'<b>Parameter Quantization: Initial and Multiple Lower Precisions',
            font=dict(size=38, family='Arial', color='black'),
            x=0.5,
            xanchor='center',
            yanchor='top',
        ),
        xaxis=dict(
            title=dict(
                text='<b>PCA Dimension 1</b>',
                font=dict(size=32, family='Arial', color='black')
            ),
            tickfont=dict(size=20)
        ),
        yaxis=dict(
            title=dict(
                text='<b>PCA Dimension 2</b>',
                font=dict(size=32, family='Arial', color='black')
            ),
            tickfont=dict(size=20)
        ),
        width=1920,
        height=1080,
        legend=dict(
            font=dict(size=28, family='Arial', color='black', weight='bold'),
            bgcolor='rgba(255,255,255,0.7)',
            bordercolor='black',
            borderwidth=2,
            x=0.02,
            y=0.98,
            xanchor='left',
            yanchor='top',
            orientation='v',
            title_font=dict(size=30, family='Arial', color='black', weight='bold')
        )
    )
    # Make legend text bold using HTML tags
    for trace in fig.data:
        if hasattr(trace, 'name') and trace.name:
            trace.name = f'<b>{trace.name}</b>'
    fig.write_html("quantization_plot.html")

# Example usage:
plot_quantization_multiple_steps(n_points=4, initial_precision=64, precisions_list=[32, 16, 8, 4])
