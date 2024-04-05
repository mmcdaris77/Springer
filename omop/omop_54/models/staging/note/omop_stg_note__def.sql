
select 
     cast(null as int) as person_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as note_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as note_datetime
    ,cast(null as int) as note_type_concept_id
    ,cast(null as int) as note_class_concept_id
    ,cast(null as varchar(250)) as note_title
    ,cast(null as text) as note_text
    ,cast(null as int) as encoding_concept_id
    ,cast(null as int) as language_concept_id
    ,cast(null as int) as provider_id
    ,cast(null as int) as visit_occurrence_id
    ,cast(null as int) as visit_detail_id
    ,cast(null as varchar(50)) as note_source_value
    ,cast(null as int) as note_event_id
    ,cast(null as int) as note_event_field_concept_id
where 1=0


    