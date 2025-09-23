import os
from pathlib import Path

def clean_path(s: str) -> Path:
    s = s.strip().strip('"').strip("'")
    return Path(os.path.expanduser(os.path.expandvars(s)))


def get_file_paths():
    print("Current working directory:", os.getcwd())
    src_input = input("Enter source file path: ")
    dst_input = input("Enter destination path (dir or file): ")

    src = clean_path(src_input)
    dst = clean_path(dst_input)

    if not src.exists():
        print(f"Source does not exist: {src}")
        return False
    if not src.is_file():
        print(f"Source is not a file: {src}")
        return False

    if dst.exists() and dst.is_dir():
        dst = dst / src.name
    else:
        parent = dst.parent
        if not parent.exists():
            # Create destination directories if needed
            parent.mkdir(parents=True, exist_ok=True)

    if dst.exists():
        print(f"Destination already exists: {dst}")
        return False

    return str(src), str(dst)

def main():

    source_path, destination_path = get_file_paths()

    customers = {}


    def check_cells_in_row(row): #simple validation for the 4 columns we expect
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
        #splits the line up and ensures it has the right number of columns
        #if skip is True, it will not validate the contents of the cells, useful for header row
      try:
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
      with open(source_path, "r", encoding="utf-8") as f:
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
      print(f"Error: The file at {source_path} was not found. {e}")

    try:
        with open(destination_path, "w", encoding="utf-8") as out:
            out.write(",".join(header) + "\n")
            for customer_id, data in customers.items():
                #print (customer_id, data)
                out.write(
                    f"{customer_id},{data['name']},{data['email']},{data['purchase_amount']}\n"
                )
    except Exception as e:
        print(f"Error writing to file at {destination_path}. {e}")

if __name__ == "__main__":
    raise SystemExit(main())