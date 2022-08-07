{{
    config(
        alias='hrr_xwalk'
    )
}}

{% set v_schema = this.schema %}

{% set list_of_relations = dbt_utils.get_relations_by_pattern(v_schema, 'stg_ZipHsaHrr%') %}

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
