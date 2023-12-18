import re


def extract_table_aliases(query):
    # Regular expression to find table names and their aliases
    pattern = re.compile(r'\bFROM\s+(\w+)(?:\s+(\w+))?\s+|JOIN\s+(\w+)(?:\s+(\w+))?\s+|\bLEFT(\s+)\s+(\w+)(?:\s+(\w+))?\s+', re.IGNORECASE)

    # Find all matches in the query
    matches = pattern.findall(query)
    # Create a dictionary to store table names and aliases
    table_dict = {}

    # Iterate through the matches and populate the dictionary
    for match in matches:
        table_name = match[0] or match[2]
        alias = match[1] or match[3] or None
        if len(alias) > 1:
            alias = table_name
        table_dict[table_name] = alias

    return table_dict


def replace_aliases_with_table_names(query, alias_to_table_mapping):
    for table, alias in alias_to_table_mapping.items():
        query = query.replace(alias + '.', table + '.')
        query = query.replace(' ' + alias + ' ', ' ' + table + ' ')
    return query

def extract_sql_components(query):
    # Normalize spaces to help regex matching
    query = ' '.join(query.split())


    # Common Patterns
    where_pattern = r'WHERE\s+(.*?)(?=(GROUP BY|ORDER BY|$))'

    # SELECT Patterns
    #select_table_pattern = r'FROM\s+(\w+)|JOIN\s+(\w+)'
    select_table_pattern = r'\$\$[a-zA-Z_]+\.\$\$[a-zA-Z_]+\.[a-zA-Z_]+'
    select_column_pattern = r'SELECT\s+(.*?)\s+FROM'
    #join_pattern = r'JOIN\s+\w+\s+ON\s+(.*?)(?=\s+JOIN|\s+WHERE|\s+GROUP BY|\s+ORDER BY|$)'
    #join_pattern = r'JOIN\s+\w+\s+\w+\s+\w+\s+(.*?)'
    #join_pattern = r'ON\s+(.*)WHERE'
    #join_pattern = re.search(r'ON\.(.*?)WHERE', query).group(1)
    join_pattern = r'ON\s+(.*?)\s+WHERE'

    # UPDATE Patterns
    update_table_pattern = r'UPDATE\s+(\w+)'
    update_set_pattern = r'SET\s+(.*?)(?=(WHERE|$))'

    # DELETE Pattern
    delete_table_pattern = r'DELETE\s+FROM\s+(\w+)'

    # Determining query type and extracting components
    if 'SELECT' in query.upper():
        tables = re.findall(select_table_pattern, query, re.IGNORECASE)
        columns = re.search(select_column_pattern, query, re.IGNORECASE)
        join_conditions = re.findall(join_pattern, query, re.IGNORECASE)
    elif 'UPDATE' in query.upper():
        tables = re.findall(update_table_pattern, query, re.IGNORECASE)
        columns = re.search(update_set_pattern, query, re.IGNORECASE)
        join_conditions = re.findall(join_pattern, query, re.IGNORECASE)
    elif 'DELETE' in query.upper():
        tables = re.findall(delete_table_pattern, query, re.IGNORECASE)
        columns = []
        join_conditions = re.findall(join_pattern, query, re.IGNORECASE)
    else:
        return "Unsupported SQL query type"

    where_clause = re.search(where_pattern, query, re.IGNORECASE)

    # Cleaning and formatting results
    #tables1 = set([t[0] or t[1] for t in tables if t])  # Handling multiple capturing groups
    #tables = list(tables1)
    tables1 = set(tables)
    tables = list(tables1)
    columns = columns.group(1).split(',') if columns else []
    #join_conditions = [j.strip() for j in join_conditions]
    where_clause = where_clause.group(1) if where_clause else ''

    return {
        'tables': tables,
        'columns': columns,
        'join_conditions': join_conditions,
        'where_clause': where_clause
    }

# Example SQL query
sql_query = """
update $$data_project_id.$$OSI_STAGE.BIO_INFO_W
set DW_ACTN_IN = 'I'
where swo_prsn_id not in (select swo_prsn_id from
$$data_project_id.$$OSI_STAGE.BT_ARCH_TRK_T BAT
where BAT.curr_in = 1
) ;

update $$data_project_id.$$OSI_STAGE.BIO_INFO_W
set DW_ACTN_IN = 'U'
where swb_prsn_id in (select ABSP.swB_prsn_id from
$$data_project_id.$$OSI_STAGE.ALL_BT_SWB_PRSN_S ABSP
inner join $$data_project_id.$$OSI_STAGE.BT_ARCH_TRK_T BAT
on ABSP.swb_pran_id = BAT.swb_pran_id
where ABSP.ONL_APPR_TS > BAT.PDF_FIRST_USE_DT
AND BAT.CURR_IN = 1);  
"""

alias_mapping = extract_table_aliases(sql_query)
#print(alias_mapping)
modified_query = replace_aliases_with_table_names(sql_query, alias_mapping)
#print(modified_query)
components = extract_sql_components(modified_query)
print(components)
