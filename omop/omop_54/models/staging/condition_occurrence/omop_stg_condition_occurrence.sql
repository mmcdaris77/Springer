
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_condition_occurrence__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.condition_start_date, a.condition_type_concept_id) as condition_occurrence_id
    ,a.person_id
    ,a.condition_concept_id
    ,a.condition_start_date
    ,a.condition_start_datetime
    ,a.condition_end_date
    ,a.condition_end_datetime
    ,a.condition_type_concept_id
    ,a.condition_status_concept_id
    ,a.stop_reason
    ,a.provider_id
    ,a.visit_occurrence_id
    ,a.visit_detail_id
    ,a.condition_source_value
    ,a.condition_source_concept_id
    ,a.condition_status_source_value
from cte_combined a