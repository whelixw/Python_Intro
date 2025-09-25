import os
from pathlib import Path

#TODO: message when overwriting existing file, file perms
#impute missing id from line number change sign for negative purchase amounts, handle duplicates
#validate email better.


def clean_path(s: str) -> Path: #clean up the path string a bit
    s = s.strip().strip('"').strip("'")
    return Path(os.path.expanduser(os.path.expandvars(s)))


def get_file_paths(): #get source and destination paths from user
    print("Current working directory:", os.getcwd())
    src_input = input("Enter source file path: ")
    dst_input = input("Enter destination path (dir or file): ")

    src = clean_path(src_input)
    dst = clean_path(dst_input)

    # Validate paths
    if not src.exists():
        print(f"Source does not exist: {src}")
        return False
    if not src.is_file():
        print(f"Source is not a file: {src}")
        return False

    if dst.exists() and dst.is_dir():
        dst = dst / src.name # if dst is a directory, append source filename
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
    paths = get_file_paths()
    if not paths:
        print("Invalid paths. Exiting.")
        return 1

    source_path, destination_path = paths

    customers = {}



    def correct_cells_in_row(row): #correct some common issues in the cells
        if len(row) != 4:
            return False
        customer_id, name, email, purchase_amount = row
        if not customer_id.isdigit():
            print("Invalid customer ID {} on row {}. Inputing the ID".format(customer_id, row))
            customer_id = str(index)
        elif int(customer_id) < 0:
            print("Negative customer ID {} on row {}. Inputing the ID".format(customer_id, row))
            customer_id = str(index)
        #name needs to be without numbers
        if set(name) & set("0123456789"):
            print("Invalid name {} on row {}.".format(name, row))
            return False
        #email needs to be split into local and domain parts. Domain part needs a dot
        email_parts = email.split("@")
        if len(email_parts) != 2 or not email_parts[0] or not email_parts[1]:
            print("Invalid email address {} on row {}.".format(email, row))
            return False
        if "." not in email_parts[1]:
            print("Invalid email domain {} on row {}.".format(email_parts[1], row))
            return False
        #purchase amount needs to be a float, if negative, make positive
        try:
            amount = float(purchase_amount)
            if amount < 0:
                print("Negative purchase amount {} on row {}. Making positive.".format(purchase_amount, row))
                amount = abs(amount)
            purchase_amount = str(amount)
        except ValueError:
            print("Invalid purchase amount {} on row {}.".format(purchase_amount, row))
            return False
        return [customer_id, name, email, purchase_amount]





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
        if len(row_buffer) == target_len-1:
            #if id is missing, it can be imputed.
            print("Missing customer ID, imputing from line number: ", index)
            row_buffer.insert(0, str(index))
        if len(row_buffer) == target_len:
            if skip:
                return row_buffer
            corrected_row_buffer = correct_cells_in_row(row_buffer)
            if corrected_row_buffer:
                print("Corrected row: ", corrected_row_buffer)
                return corrected_row_buffer
        else:
          # error handling for malformed lines
          print(
            f"Malformed line (expected {target_len} columns, got {len(row)}): {line}"
          )
          return None
      except Exception as e:
        print(f"Error parsing line: {line}. Error: {e}")
        return None


    index = 0 #line index

    try:
      with open(source_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

      line = lines[index]
      row = safe_line_parse(line, skip=True) #parse the header row without validation
      header = row
      index += 1
      while index < len(lines): #process each line
        line = lines[index]
        parsed_line = safe_line_parse(line)
        if parsed_line is not None:
          # get the values from the parsed line
          customer_id, name, email, purchase_amount = parsed_line
          customers[customer_id] = {
            "name": name,
            "email": email,
            "purchase_amount": purchase_amount,
          }
        else:
          print("Skipping malformed line:, ", index)
        #print(index)
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