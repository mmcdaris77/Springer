
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_procedure_occurrence__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.procedure_date, a.procedure_type_concept_id) as procedure_occurrence_id
    ,a.person_id
    ,a.procedure_concept_id
    ,a.procedure_date
    ,a.procedure_datetime
    ,a.procedure_end_date
    ,a.procedure_end_datetime
    ,a.procedure_type_concept_id
    ,a.modifier_concept_id
    ,a.quantity
    ,a.provider_id
    ,a.visit_occurrence_id
    ,a.visit_detail_id
    ,a.procedure_source_value
    ,a.procedure_source_concept_id
    ,a.modifier_source_value
from cte_combined a