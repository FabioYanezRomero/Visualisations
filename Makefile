.PHONY: build docker run clean

build:
pip install -r requirements.txt

docker:
docker build -t visualisations:latest .

run:
docker run --rm -it -v $(PWD):/app visualisations:latest

clean:
rm -rf __pycache__
