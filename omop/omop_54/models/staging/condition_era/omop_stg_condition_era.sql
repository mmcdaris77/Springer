
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_condition_era__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.condition_era_start_date, a.condition_concept_id) as condition_era_id
    ,a.person_id
    ,a.condition_concept_id
    ,a.condition_era_start_date
    ,a.condition_era_end_date
    ,a.condition_occurrence_count
from cte_combined a