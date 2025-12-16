class SQLParseError(Exception):
    pass

import re

def parse_sql(query):
    query = query.strip().rstrip(';')
    tokens = query.split()

    if tokens[0].upper() != 'SELECT':
        raise SQLParseError("Query must start with SELECT")

    # Find FROM
    if 'FROM' in tokens:
        from_index = tokens.index('FROM')
    elif 'from' in tokens:
        from_index = tokens.index('from')
    else:
        raise SQLParseError("Missing FROM clause")

    parsed_query = {}

    # Parse SELECT columns
    select_part = tokens[1:from_index]
    select_str = ' '.join(select_part)

    # ✅ COUNT handling (FIXED INDENTATION)
    if select_str.upper().startswith('COUNT'):
        parsed_query['type'] = 'count'
        inside = select_str[6:-1]  # inside COUNT(...)
        parsed_query['column'] = None if inside == '*' else inside
        parsed_query['columns'] = None
    else:
        parsed_query['type'] = 'select'
        parsed_query['column'] = None
        if select_str == '*':
            parsed_query['columns'] = ['*']
        else:
            parsed_query['columns'] = [c.strip() for c in select_str.split(',')]

    # Parse table name
    parsed_query['table'] = tokens[from_index + 1]

    # Default WHERE
    parsed_query['where'] = None

    # Parse WHERE if exists
    if 'WHERE' in tokens or 'where' in tokens:
        try:
            where_index = tokens.index('WHERE')
        except ValueError:
            where_index = tokens.index('where')

        condition = ' '.join(tokens[where_index + 1:])

        match = re.match(r"(\w+)\s*(=|!=|>=|<=|>|<)\s*(.+)", condition)
        if not match:
            raise SQLParseError("Invalid WHERE clause")

        column, operator, value = match.groups()

        value = value.strip()
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass

        parsed_query['where'] = {
            'column': column,
            'op': operator,
            'value': value
        }

    return parsed_query


if __name__ == "__main__":
    q1 = "SELECT name, age FROM people WHERE age > 30;"
    print(parse_sql(q1))

    q2 = "SELECT COUNT(*) FROM people WHERE age > 30;"
    print(parse_sql(q2))
