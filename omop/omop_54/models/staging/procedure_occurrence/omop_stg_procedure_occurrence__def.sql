
select 
     cast(null as int) as person_id
    ,cast(null as int) as procedure_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as procedure_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as procedure_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as procedure_end_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as procedure_end_datetime
    ,cast(null as int) as procedure_type_concept_id
    ,cast(null as int) as modifier_concept_id
    ,cast(null as int) as quantity
    ,cast(null as int) as provider_id
    ,cast(null as int) as visit_occurrence_id
    ,cast(null as int) as visit_detail_id
    ,cast(null as varchar(50)) as procedure_source_value
    ,cast(null as int) as procedure_source_concept_id
    ,cast(null as varchar(50)) as modifier_source_value
where 1=0





