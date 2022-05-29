{{
    config(
        alias='hrr_xwalk'
    )
}}

{% set list_of_relations = sqlite_get_tables_by_pattern('main', 'stg_ZipHsaHrr%') %}

with cte_data as (
    {{
        dbt_utils.union_relations(list_of_relations)
    }}
)

select 
     substr('00000' || zipcode19, -5, 5) as zipcode
    ,hsanum
    ,hsacity
    ,hsastate
    ,hrrnum
    ,hrrcity
    ,hrrstate
from cte_data
