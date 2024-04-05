
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_note__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.note_date, a.note_type_concept_id) as note_id
    ,a.person_id
    ,a.note_date
    ,a.note_datetime
    ,a.note_type_concept_id
    ,a.note_class_concept_id
    ,a.note_title
    ,a.note_text
    ,a.encoding_concept_id
    ,a.language_concept_id
    ,a.provider_id
    ,a.visit_occurrence_id
    ,a.visit_detail_id
    ,a.note_source_value
    ,a.note_event_id
    ,a.note_event_field_concept_id
from cte_combined a