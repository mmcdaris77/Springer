
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_death__def')
            ]
        )
    }}
)

select 
     a.person_id
    ,a.death_date
    ,a.death_datetime
    ,a.death_type_concept_id
    ,a.cause_concept_id
    ,a.cause_source_value
    ,a.cause_source_concept_id
from cte_combined a