
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_observation_period__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.observation_period_start_date, a.period_type_concept_id) as observation_period_id
    ,a.person_id
    ,a.observation_period_start_date
    ,a.observation_period_end_date
    ,a.period_type_concept_id
from cte_combined a