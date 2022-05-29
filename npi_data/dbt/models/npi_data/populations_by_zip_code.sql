{{
    config(
        alias='populations_by_zip_code'
    )
}}

{% set list_of_relations = sqlite_get_tables_by_pattern('main', 'stg__Census_Populations_by_Zip_Code%') %}


{{
    dbt_utils.union_relations(list_of_relations)
}}


