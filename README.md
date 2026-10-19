# Device Log Summarizer CLI

A Python command-line tool that processes device telemetry from a CSV file,
summarizes records by device, counts errors, filters high average temperatures,
exports results to JSON, and generates a temperature chart.

## Requirements
Python 3 and matplotlib

## Run
python -m pip install -r requirements.txt
python -m unittest test_main -v
python main.py
python chart.py
