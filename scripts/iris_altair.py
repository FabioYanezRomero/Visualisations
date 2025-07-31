import altair as alt
from vega_datasets import data

def main(output_path="iris_scatter.html"):
    iris = data.iris()
    chart = (
        alt.Chart(iris)
        .mark_circle(size=60)
        .encode(
            x="sepalLength",
            y="sepalWidth",
            color="species",
            tooltip=["sepalLength", "sepalWidth", "species"],
        )
        .interactive()
    )
    chart.save(output_path)
    print(f"Saved plot to {output_path}")

if __name__ == "__main__":
    main()
