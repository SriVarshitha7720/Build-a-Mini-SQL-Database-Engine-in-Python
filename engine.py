import csv
from parser import parse_sql

class QueryExecutionError(Exception):
    pass

# ------------------ CSV Loader ------------------
def load_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
    return rows

# ------------------ WHERE Filtering ------------------
def apply_where(rows, where_clause):
    if where_clause is None:
        return rows

    column = where_clause['column']
    operator = where_clause['op']
    value = where_clause['value']

    filtered_rows = []

    for row in rows:
        if column not in row:
            raise QueryExecutionError(f"Unknown column '{column}'")

        row_value = row[column]

        try:
            row_value = float(row_value)
        except ValueError:
            pass

        if operator == '=' and row_value == value:
            filtered_rows.append(row)
        elif operator == '!=' and row_value != value:
            filtered_rows.append(row)
        elif operator == '>' and row_value > value:
            filtered_rows.append(row)
        elif operator == '<' and row_value < value:
            filtered_rows.append(row)
        elif operator == '>=' and row_value >= value:
            filtered_rows.append(row)
        elif operator == '<=' and row_value <= value:
            filtered_rows.append(row)

    return filtered_rows

# ------------------ SELECT Projection ------------------
def apply_select(rows, columns):
    if columns == ['*']:
        return rows

    result = []
    for row in rows:
        projected_row = {}
        for col in columns:
            if col not in row:
                raise QueryExecutionError(f"Unknown column '{col}'")
            projected_row[col] = row[col]
        result.append(projected_row)
    return result

# ------------------ COUNT ------------------
def apply_count(rows, column):
    if column is None:
        return len(rows)
    count = 0
    for row in rows:
        if column not in row:
            raise QueryExecutionError(f"Unknown column '{column}'")
        if row[column] not in (None, '', 'NULL'):
            count += 1
    return count

# ------------------ Query Execution ------------------
def execute_query(parsed_query, data):
    rows = apply_where(data, parsed_query['where'])

    if parsed_query['type'] == 'count':
        return apply_count(rows, parsed_query['column'])

    return apply_select(rows, parsed_query['columns'])

# ------------------ CLI / REPL ------------------
def repl():
    print("Welcome to In-Memory SQL Engine!")
    print("Type 'exit' or 'quit' to leave.\n")

    file_path = input("Enter CSV file path: ").strip()
    try:
        data = load_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    while True:
        query = input("\nsql> ").strip()
        if query.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        if not query:
            continue
        try:
            parsed_query = parse_sql(query)
            result = execute_query(parsed_query, data)
            print_result(result, parsed_query)
        except Exception as e:
            print(f"Error: {e}")

def print_result(result, parsed_query):
    if parsed_query['type'] == 'count':
        print(result)
    else:
        if not result:
            print("No rows found.")
            return
        cols = result[0].keys()
        header = " | ".join(cols)
        print(header)
        print("-" * len(header))
        for row in result:
            print(" | ".join(str(row[col]) for col in cols))

# ------------------ MAIN ------------------
if __name__ == "__main__":
    repl()
