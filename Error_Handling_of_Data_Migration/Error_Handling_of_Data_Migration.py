import os

filepath = os.path.join(
  os.getcwd(),
  "Data",
  "source_data.csv",
)
outpath = os.path.join(
  os.getcwd(),
  "Error_Handling_of_Data_Migration",
  "Output",
  "migrated_data.csv",
)

customers = {}


def check_cells_in_row(row):
    if len(row) != 4:
        return False
    customer_id, name, email, purchase_amount = row
    if not customer_id.isdigit():
        return False
    if "@" not in email or "." not in email:
        return False
    try:
        float(purchase_amount)
    except ValueError:
        return False
    return True

def safe_line_parse(line, target_len=4, skip = False):
  try:
    # CHANGED: Parse as CSV by splitting on commas (was whitespace split)
    # CHANGED: Do not drop empty columns; preserve all columns
    row_buffer = []
    clean_line = line.strip()
    cols = clean_line.split(",")
    for row in cols:
        if row.strip() != "":
            row_buffer.append(row.strip())

    if len(row_buffer) == target_len:
        if skip or check_cells_in_row(row_buffer):
            return row_buffer
    else:
      # CHANGED: Report the actual row length being validated
      print(
        f"Malformed line (expected {target_len} columns, got {len(row)}): {line}"
      )
      return None
  except Exception as e:
    print(f"Error parsing line: {line}. Error: {e}")
    return None


index = 0

try:
  with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

  line = lines[index]
  row = safe_line_parse(line, skip=True)
  header = row
  index += 1
  while index < len(lines):
    line = lines[index]
    parsed_line = safe_line_parse(line)
    if parsed_line is not None:
      # CHANGED: Reuse parsed_line instead of parsing the same line again
      customer_id, name, email, purchase_amount = parsed_line
      customers[customer_id] = {
        "name": name,
        "email": email,
        "purchase_amount": purchase_amount,
      }
    else:
      print("Skipping malformed line:, ", index)
    print(index)
    index += 1

except FileNotFoundError as e:
  print(f"Error: The file at {filepath} was not found. {e}")

try:
    with open(outpath, "w", encoding="utf-8") as out:
        out.write(",".join(header) + "\n")
        for customer_id, data in customers.items():
            #print (customer_id, data)
            out.write(
                f"{customer_id},{data['name']},{data['email']},{data['purchase_amount']}\n"
            )
except Exception as e:
    print(f"Error writing to file at {outpath}. {e}")