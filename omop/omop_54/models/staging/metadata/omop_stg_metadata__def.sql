
select 
     cast(null as int) as metadata_concept_id
    ,cast(null as int) as metadata_type_concept_id
    ,cast(null as varchar(250)) as name
    ,cast(null as varchar(250)) as value_as_string
    ,cast(null as int) as value_as_concept_id
    ,cast(null as float) as value_as_number
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as metadata_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as metadata_datetime
where 1=0


    