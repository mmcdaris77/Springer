

{% set list_of_relations = sqlite_get_tables_by_pattern('main', 'stg_npidata_pfile%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}
