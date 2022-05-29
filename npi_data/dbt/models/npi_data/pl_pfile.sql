{{
    config(
        alias='npi_pl_pfile'
    )
}}

{% set list_of_relations = sqlite_get_tables_by_pattern('main', 'stg_pl_pfile%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}
