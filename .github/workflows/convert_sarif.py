import sys
import os
import json

def convert_sarif_to_html(sarif_file_path):
    # Get the directory of the script
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Build the output file path
    output_file_name = "output.html"
    output_file_path = os.path.join(script_directory, output_file_name)

    # Load SARIF file
    with open(sarif_file_path, 'r') as sarif_file:
        sarif_data = json.load(sarif_file)

    # Extract relevant information from SARIF data
    results = []
    for run in sarif_data['runs']:
        for result in run['results']:
            results.append(result)

    # Generate HTML representation
    html_output = "<html><head><title>SARIF Report</title></head><body>"
    html_output += "<h1>SARIF Report</h1>"
    html_output += "<table>"
    html_output += "<tr><th>Serial Number</th><th>Rule</th><th>Message</th><th>Criticality</th><th>Location</th></tr>"

    for index, result in enumerate(results, start=1):
        rule_id = result['ruleId']
        message = result['message']['text']
        criticality = result.get('properties', {}).get('severity')
        location = result['locations'][0]['physicalLocation']['artifactLocation']['uri']
        line_number = result['locations'][0]['physicalLocation']['region']['startLine']

        html_output += f"<tr><td>{index}</td><td>{rule_id}</td><td>{message}</td><td>{criticality}</td><td>{location}:{line_number}</td></tr>"

    html_output += "</table></body></html>"

    # Write HTML output to file
    with open(output_file_path, 'w') as output_file:
        output_file.write(html_output)

    print(f"Conversion completed successfully. Output file saved as {output_file_path}")

# Usage: python convert_sarif.py <sarif_file_path>
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_sarif.py <sarif_file_path>")
        sys.exit(1)

    sarif_file_path = sys.argv[1]

    convert_sarif_to_html(sarif_file_path)
