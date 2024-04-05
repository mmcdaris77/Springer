
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_visit_occurrence__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.visit_start_date, a.visit_type_concept_id) as visit_occurrence_id
    ,a.person_id
    ,a.visit_concept_id
    ,a.visit_start_date
    ,a.visit_start_datetime
    ,a.visit_end_date
    ,a.visit_end_datetime
    ,a.visit_type_concept_id
    ,a.provider_id
    ,a.care_site_id
    ,a.visit_source_value
    ,a.visit_source_concept_id
    ,a.admitted_from_concept_id
    ,a.admitted_from_source_value
    ,a.discharged_to_concept_id
    ,a.discharged_to_source_value
    ,a.preceding_visit_occurrence_id
from cte_combined a