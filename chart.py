
import json
from pathlib import Path

import matplotlib.pyplot as plt

INPUT_FILE = Path("summary.json")
OUTPUT_FILE = Path("temperature_chart.png")


def generate_chart():
    try:
        with INPUT_FILE.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: summary.json not found. Run main.py first.")
        return
    except (OSError, json.JSONDecodeError) as error:
        print(f"Error reading JSON: {error}")
        return

    if not isinstance(data, list):
        print("Error: Expected a list of device summaries.")
        return

    devices = []
    temperatures = []

    for item in data:
        if not isinstance(item, dict):
            continue

        device_id = item.get("device_id")
        temperature = item.get("average_temperature")

        if (
            isinstance(device_id, str)
            and isinstance(temperature, (int, float))
            and not isinstance(temperature, bool)
        ):
            devices.append(device_id)
            temperatures.append(temperature)

    if not devices:
        print("No valid data available to plot.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(devices, temperatures)

    ax.set_title("Average Temperature per Device", pad=15)
    ax.set_xlabel("Device ID")
    ax.set_ylabel("Average Temperature")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)
    ax.bar_label(bars, fmt="%.2f", padding=4)
    ax.margins(y=0.15)

    fig.tight_layout()

    try:
        fig.savefig(OUTPUT_FILE, dpi=150, bbox_inches="tight")
        print(f"Chart saved to {OUTPUT_FILE}")
    except OSError as error:
        print(f"Could not save chart: {error}")
    finally:
        plt.close(fig)


if __name__ == "__main__":
    generate_chart()
