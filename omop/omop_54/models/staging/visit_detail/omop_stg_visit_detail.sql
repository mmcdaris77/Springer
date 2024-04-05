
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_visit_detail__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.visit_detail_start_date, a.visit_detail_type_concept_id) as visit_detail_id
    ,a.person_id
    ,a.visit_detail_concept_id
    ,a.visit_detail_start_date
    ,a.visit_detail_start_datetime
    ,a.visit_detail_end_date
    ,a.visit_detail_end_datetime
    ,a.visit_detail_type_concept_id
    ,a.provider_id
    ,a.care_site_id
    ,a.visit_detail_source_value
    ,a.visit_detail_source_concept_id
    ,a.admitted_from_concept_id
    ,a.admitted_from_source_value
    ,a.discharged_to_source_value
    ,a.discharged_to_concept_id
    ,a.preceding_visit_detail_id
    ,a.parent_visit_detail_id
    ,a.visit_occurrence_id
from cte_combined a