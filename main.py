import csv
import json
from collections import defaultdict
from pathlib import Path
def clean_readings(values):
    """Convert valid sensor readings to floats and clean invalid values."""
    cleaned_values = []

    for value in values:
        # Ignore None and boolean values
        if value is None or isinstance(value, bool):
            continue

        # Try to convert the value to a float
        try:
            number = float(value)
        except (ValueError, TypeError):
            continue

        # Ignore negative numbers and non-finite values
        if number < 0 or number != number:
            continue

        if number == float("inf") or number == float("-inf"):
            continue

        # Cap readings at 500.0
        number = min(number, 500.0)

        cleaned_values.append(number)

    return cleaned_values


def test_clean_readings():
    # Test 1: Mixed valid and invalid values
    result1 = clean_readings([10, "25.5", None, -4, 700])
    expected1 = [10.0, 25.5, 500.0]
    assert result1 == expected1, f"Test 1 failed: {result1}"

    # Test 2: All values are invalid
    result2 = clean_readings(["hello", None, -10])
    expected2 = []
    assert result2 == expected2, f"Test 2 failed: {result2}"

    # Test 3: Empty input list
    result3 = clean_readings([])
    expected3 = []
    assert result3 == expected3, f"Test 3 failed: {result3}"

    print("All 3 tests passed successfully!")

    
def summarize_devices():
    input_file = Path("device_telemetry.csv")
    output_file = Path("summary.json")

    devices = defaultdict(
        lambda: {
            "total_records": 0,
            "temperature_sum": 0.0,
            "error_count": 0,
        }
    )

    # Step 1: Read the CSV file
    try:
        with input_file.open(
            "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            required_columns = {
                "device_id", "status", "temperature"
            }

            if (
                not reader.fieldnames
                or not required_columns.issubset(reader.fieldnames)
            ):
                print("Error: CSV is missing required columns.")
                return

            # Step 2: Process each row
            for row in reader:
                device_id = (row.get("device_id") or "").strip()
                status = (row.get("status") or "").strip().upper()

                if not device_id:
                    continue

                try:
                    temperature = float(row["temperature"])
                except (ValueError, TypeError, KeyError):
                    print(f"Skipping invalid row: {row}")
                    continue

                # Reject NaN and infinite temperatures
                if not (
                    float("-inf") < temperature < float("inf")
                ):
                    print(f"Skipping invalid temperature: {row}")
                    continue

                device = devices[device_id]
                device["total_records"] += 1
                device["temperature_sum"] += temperature

                if status == "ERROR":
                    device["error_count"] += 1

    except FileNotFoundError:
        print(f"Error: {input_file} was not found.")
        return
    except OSError as error:
        print(f"Error reading CSV: {error}")
        return

    # Step 3: Calculate averages and filter devices
    results = []

    for device_id, data in sorted(devices.items()):
        count = data["total_records"]

        if count == 0:
            continue

        average = data["temperature_sum"] / count

        if average > 80.0:
            continue

        results.append({
            "device_id": device_id,
            "total_records": count,
            "average_temperature": round(average, 2),
            "error_count": data["error_count"],
        })

    # Step 4: Export results to JSON
    try:
        with output_file.open("w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)
            file.write("\n")
    except OSError as error:
        print(f"Error writing JSON: {error}")
        return

    # Step 5: Print a summary table
    print("\nDevice Telemetry Summary")
    print("-" * 48)
    print(
        f"{'DEVICE':<12} {'RECORDS':>8} "
        f"{'AVG TEMP':>12} {'ERRORS':>8}"
    )
    print("-" * 48)

    for item in results:
        print(
            f"{item['device_id']:<12} "
            f"{item['total_records']:>8} "
            f"{item['average_temperature']:>12.2f} "
            f"{item['error_count']:>8}"
        )

    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    summarize_devices()
    

