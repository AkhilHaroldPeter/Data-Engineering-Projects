def read_sql_file(filename):
    with open(filename, 'r') as file:
        sql_query = file.read()
        return sql_query