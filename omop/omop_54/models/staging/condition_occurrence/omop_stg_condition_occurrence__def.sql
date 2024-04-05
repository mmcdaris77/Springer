
select 
     cast(null as int) as person_id
    ,cast(null as int) as condition_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as condition_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as condition_start_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as condition_end_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as condition_end_datetime
    ,cast(null as int) as condition_type_concept_id
    ,cast(null as int) as condition_status_concept_id
    ,cast(null as varchar(20)) as stop_reason
    ,cast(null as int) as provider_id
    ,cast(null as int) as visit_occurrence_id
    ,cast(null as int) as visit_detail_id
    ,cast(null as varchar(50)) as condition_source_value
    ,cast(null as int) as condition_source_concept_id
    ,cast(null as varchar(50)) as condition_status_source_value
where 1=0


    