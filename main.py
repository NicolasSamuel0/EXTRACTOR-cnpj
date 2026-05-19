import  requests
import json
import csv

#==============================================================================
# SECTION 1: Fetch API Data and Save as JSON Lines
#==============================================================================

# Define input and output file paths and API base URL
input_file = "input.txt"         # File containing strings, one per line
output_file = "output.jsonl"       # JSON Lines output file
api_base_url = "https://minhareceita.org/"

# Read strings from the input file
with open(input_file, "r") as f:
    strings = [line.strip() for line in f if line.strip()]
                
# Fetch data for each string and write each JSON response as a new line
with open(output_file, "w") as f_out:
    for string in strings:
        url = f"{api_base_url}{string}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise error for HTTP failures
            json_response = response.json()  # Parse response as JSON
            f_out.write(json.dumps(json_response) + "\n")
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except json.JSONDecodeError:
            print(f"Invalid JSON response from {url}")

#==============================================================================
# SECTION 2: Process numbers.txt and Compare with JSON Data
#==============================================================================

# Load numbers from numbers.txt into a set (ignoring empty lines)
with open("numbers.txt", "r") as f:
    numbers_set = {line.strip() for line in f if line.strip()}

# Print a few sample numbers from numbers.txt
print("Sample numbers from numbers.txt:", list(numbers_set)[:5])

# Create a set for cnpj values from the JSON file
json_cnpj_set = set()

# Process the JSON file to extract cnpj values
with open("output.jsonl", "r") as f:
    for line in f:
        try:
            data = json.loads(line)
            # Convert the cnpj to a string and strip spaces
            cnpj = str(data.get("cnpj", "")).strip()
            if cnpj:
                json_cnpj_set.add(cnpj)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
            continue

# Print a few sample cnpj values from the JSON file
print("Sample cnpj from JSON file:", list(json_cnpj_set)[:5])

# Compute matched and unmatched numbers
matched_numbers = numbers_set.intersection(json_cnpj_set)
unmatched_numbers = numbers_set - matched_numbers

print(f"Total numbers in numbers.txt: {len(numbers_set)}")
print(f"Total cnpj in JSON file: {len(json_cnpj_set)}")
print(f"Total matched numbers: {len(matched_numbers)}")
print(f"Total unmatched numbers: {len(unmatched_numbers)}")

# Save unmatched numbers to a file named unmatched.txt
with open("unmatched.txt", "w") as f:
    for num in unmatched_numbers:
        f.write(num + "\n")

print("Unmatched numbers have been saved to 'unmatched.txt'.")

#==============================================================================
# SECTION 3: Filter JSON Data Keeping Only Desired Keys
#==============================================================================

# List of keys to keep in the filtered output
desired_keys = [
    "uf", "cep", "cnpj", "porte", "bairro", "numero", "municipio",
    "logradouro", "cnae_fiscal", "complemento", "razao_social",
    "nome_fantasia", "capital_social", "cnae_fiscal_descricao",
    "descricao_situacao_cadastral", "descricao_tipo_de_logradouro"
]

# Open the input (output.jsonl) and output (filtered.jsonl) files
with open('output.jsonl', 'r', encoding='utf-8') as infile, \
     open('filtered.jsonl', 'w', encoding='utf-8') as outfile:
    # Process each line (each is a valid JSON object)
    for line in infile:
        try:
            data = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"Error decoding line: {line}\nError: {e}")
            continue

        # Create a new dictionary with only the desired keys
        filtered_data = {key: data.get(key) for key in desired_keys}

        # Write the filtered dictionary as a JSON line to the output file
        outfile.write(json.dumps(filtered_data, ensure_ascii=False) + "\n")

#==============================================================================
# SECTION 4: Convert Filtered JSONL Data to CSV
#==============================================================================

# Define the expected keys (fields) for each CSV record
expected_keys = [
    'uf', 'cep', 'cnpj', 'porte', 'bairro', 'numero', 
    'municipio', 'logradouro', 'cnae_fiscal', 'complemento', 
    'razao_social', 'nome_fantasia', 'capital_social', 
    'cnae_fiscal_descricao', 'descricao_situacao_cadastral', 
    'descricao_tipo_de_logradouro'
]

def convert_jsonl_to_csv(input_file, output_file):
    """
    Convert a JSON Lines file to a CSV file ensuring that each record has the expected keys.
    Missing or empty values are replaced with an empty string.
    Large number fields are converted to strings to preserve formatting.
    """
    with open(input_file, "r", encoding="utf-8") as jsonl_file, \
         open(output_file, "w", newline="", encoding="utf-8") as csv_file:

        # Initialize CSV writer using the expected keys as header
        writer = csv.DictWriter(csv_file, fieldnames=expected_keys)
        writer.writeheader()

        # Process each line (each is a JSON object)
        for line_number, line in enumerate(jsonl_file, start=1):
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Skipping line {line_number} due to JSON decode error: {e}")
                continue  # Skip lines that aren't valid JSON

            # Ensure each record contains every expected key.
            for key in expected_keys:
                if key not in record or record[key] is None or record[key] == '':
                    record[key] = ''
                # Convert large number fields to strings to preserve formatting
                if key in ['cnpj', 'capital_social']:
                    if key == 'cnpj':
                        record[key] = "'" + str(record[key]) # Adds ' for excel use
                    else:
                        record[key] = str(record[key])
            
            writer.writerow(record)
    print(f"Conversion complete. CSV file created as '{output_file}'.")

# Convert the filtered JSON Lines file to CSV
input_filename = "filtered.jsonl"
output_filename = "finalresult.csv"
convert_jsonl_to_csv(input_filename, output_filename)
