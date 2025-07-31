# Visualisations

This repository contains Python scripts for generating high quality visualisations from real or dummy datasets. The outputs are suitable for scientific papers and teaching material such as Medium posts.

## Structure

```
.
├── datasets/            # Example or user provided data
├── scripts/             # Python scripts generating visualisations
├── Dockerfile           # Container setup
├── requirements.txt     # Python dependencies
├── Makefile             # Utility commands
└── README.md            # Project overview
```

## Getting Started

1. **Install Dependencies**

   ```bash
   make build
   ```

2. **Run an Example**

   ```bash
   python scripts/iris_altair.py
   ```

   The above command creates `iris_scatter.html` using the classic iris dataset.

3. **Using Docker**

   Build and start an interactive container with the required tools installed.

   ```bash
   make docker
   make run
   ```

## Dependencies

Key libraries include:

- `pandas` and `numpy` for data manipulation
- `matplotlib`, `seaborn`, `plotly` and `altair` for visualisations
- `bokeh` and `colorcet` for additional plotting options
- `tqdm` and `rich` for prettier terminal output

Additional tools such as `jupyter` and `scikit-learn` are included to facilitate experimentation and data preparation.

## Contributing

Feel free to add new scripts or notebooks demonstrating interesting visualisation techniques. Keep datasets small or provide download instructions in `datasets/`.

