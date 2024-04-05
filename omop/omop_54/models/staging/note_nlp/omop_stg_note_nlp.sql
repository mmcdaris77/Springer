
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_note_nlp__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.note_id, a.section_concept_id) as note_nlp_id
    ,a.note_id
    ,a.section_concept_id
    ,a.snippet
    ,a.offset
    ,a.lexical_variant
    ,a.note_nlp_concept_id
    ,a.note_nlp_source_concept_id
    ,a.nlp_system
    ,a.nlp_date
    ,a.nlp_datetime
    ,a.term_exists
    ,a.term_temporal
    ,a.term_modifiers
from cte_combined a