from google.cloud import bigquery

def insert_table_aliases_to_bigquery(table_aliases, project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)

    # Define the dataset and table
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    table = client.get_table(table_ref)

    # Create rows to insert into the table
    rows_to_insert = [{'alias_key': key, 'table_alias': value} for key, value in table_aliases.items()]

    # Insert rows into the table
    errors = client.insert_rows(table, rows_to_insert)

    if errors:
        print(f"Errors during insertion: {errors}")
    else:
        print("Data inserted successfully.")

# Replace with your actual Google Cloud project, dataset, and table information
project_id = 'PROJECT_ID'
dataset_id = 'DATASET_ID'
table_id = 'TABLE_ID'

# Example SQL query
sql_query = """
update $$data_project_id.$$OSI_STAGE.BIO_INFO_W
set DW_ACTN_IN = 'U'
where swb_prsn_id in (select ABSP.swB_prsn_id from
$$data_project_id.$$OSI_STAGE.ALL_BT_SWB_PRSN_S ABSP
inner join $$data_project_id.$$OSI_STAGE.BT_ARCH_TRK_T BAT
on ABSP.swb_pran_id = BAT.swb_pran_id
where ABSP.ONL_APPR_TS > BAT.PDF_FIRST_USE_DT
AND BAT.CURR_IN = 1);
"""

table_aliases = extract_table_aliases(sql_query)

# Insert into BigQuery
insert_table_aliases_to_bigquery(table_aliases, project_id, dataset_id, table_id)
