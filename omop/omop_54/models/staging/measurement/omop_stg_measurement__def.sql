
select 
     cast(null as int) as person_id
    ,cast(null as int) as measurement_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as measurement_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as measurement_datetime
    ,cast(null as varchar(10)) as measurement_time
    ,cast(null as int) as measurement_type_concept_id
    ,cast(null as int) as operator_concept_id
    ,cast(null as float) as value_as_number
    ,cast(null as int) as value_as_concept_id
    ,cast(null as int) as unit_concept_id
    ,cast(null as float) as range_low
    ,cast(null as float) as range_high
    ,cast(null as int) as provider_id
    ,cast(null as int) as visit_occurrence_id
    ,cast(null as int) as visit_detail_id
    ,cast(null as varchar(50)) as unit_source_value
    ,cast(null as int) as unit_source_concept_id
    ,cast(null as varchar(50)) as value_source_value
    ,cast(null as int) as measurement_event_id
    ,cast(null as int) as meas_event_field_concept_id
where 1=0





