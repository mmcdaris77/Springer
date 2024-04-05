{{ 
    config(alias='note') 
}}



select 
     cast(a.note_id as int) as note_id
    ,cast(a.person_id as int) as person_id
    ,{{ dbt.safe_cast("a.note_date", api.Column.translate_type("date")) }} as note_date
    ,{{ dbt.safe_cast("a.note_datetime", api.Column.translate_type("timestamp")) }} as note_datetime
    ,cast(a.note_type_concept_id as int) as note_type_concept_id
    ,cast(a.note_class_concept_id as int) as note_class_concept_id
    ,cast(a.note_title as varchar(250)) as note_title
    ,cast(a.note_text as text) as note_text
    ,cast(a.encoding_concept_id as int) as encoding_concept_id
    ,cast(a.language_concept_id as int) as language_concept_id
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
    ,cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.note_source_value as varchar(50)) as note_source_value
    ,cast(a.note_event_id as int) as note_event_id
    ,cast(a.note_event_field_concept_id as int) as note_event_field_concept_id
from {{ ref('omop_stg_note') }} a 




