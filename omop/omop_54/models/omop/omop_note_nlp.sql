{{ 
    config(alias='note_nlp') 
}}



select 
     cast(a.note_nlp_id as int) as note_nlp_id
    ,cast(a.note_id as int) as note_id
    ,cast(a.section_concept_id as int) as section_concept_id
    ,cast(a.snippet as varchar(250)) as snippet
    ,cast(a.offset as varchar(50)) as offset
    ,cast(a.lexical_variant as varchar(250)) as lexical_variant
    ,cast(a.note_nlp_concept_id as int) as note_nlp_concept_id
    ,cast(a.note_nlp_source_concept_id as int) as note_nlp_source_concept_id
    ,cast(a.nlp_system as varchar(250)) as nlp_system
    ,{{ dbt.safe_cast("a.nlp_date", api.Column.translate_type("date")) }} as nlp_date
    ,{{ dbt.safe_cast("a.nlp_datetime", api.Column.translate_type("timestamp")) }} as nlp_datetime
    ,cast(a.term_exists as varchar(1)) as term_exists
    ,cast(a.term_temporal as varchar(50)) as term_temporal
    ,cast(a.term_modifiers as varchar(2000)) as term_modifiers
from {{ ref('omop_stg_note_nlp') }} a 




