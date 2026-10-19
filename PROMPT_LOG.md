
# AI Prompt Log

## Initial Prompt

Write a Python script using matplotlib that reads summary.json
and creates a bar chart comparing average_temperature by device_id.
Include a title, axis labels, values above each bar, and save the
result as temperature_chart.png. Handle missing or invalid JSON.

## Code Review

I reviewed the generated code and ran it against the output from
my CSV processing script.

Observed issue: [Write the actual issue you found, if any.]

## Follow-up Prompt

Please fix the layout issue found during review. Ensure the title,
axis labels, and bar-value labels are readable and not clipped.
Use an appropriate figure size and tight_layout(), then save the
chart as a PNG file.

## Verification

- Ran the chart script using summary.json.
- Checked the displayed device names and average temperatures.
- Checked the title and axis labels.
- Confirmed that temperature_chart.png was generated.
