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
    fig.add_trace(go.Scatter(
        x=initial_2d[:, 0], y=initial_2d[:, 1], mode='markers',
        marker=dict(color='blue', size=8, opacity=0.7),
        name=f'Initial Precision ({initial_precision} levels)'
    ))
    # Pick colors for each precision step
    colors = ['red', 'orange', 'green', 'purple', 'brown']
    for i, (prec, points_2d) in enumerate(zip(precisions_list, other_2d)):
        color = colors[i % len(colors)]
        fig.add_trace(go.Scatter(
            x=points_2d[:, 0], y=points_2d[:, 1], mode='markers',
            marker=dict(color=color, size=8, opacity=0.7),
            name=f'Precision {prec} levels'
        ))
        for j in range(n_points):
            fig.add_trace(go.Scatter(
                x=[initial_2d[j, 0], points_2d[j, 0]],
                y=[initial_2d[j, 1], points_2d[j, 1]],
                mode='lines', line=dict(color=color, width=1), showlegend=False
            ))
    fig.update_layout(
        title=f'Parameter Quantization: Initial and Multiple Lower Precisions (n={n_points})',
        xaxis_title='PCA Dimension 1', yaxis_title='PCA Dimension 2', width=900, height=600
    )
    fig.show()

# Example usage:
plot_quantization_multiple_steps(n_points=100, initial_precision=32, precisions_list=[16, 8, 4])
