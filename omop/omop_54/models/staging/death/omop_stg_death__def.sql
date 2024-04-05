
select 
     cast(null as int) as person_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as death_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as death_datetime
    ,cast(null as int) as death_type_concept_id
    ,cast(null as int) as cause_concept_id
    ,cast(null as varchar(50)) as cause_source_value
    ,cast(null as int) as cause_source_concept_id
where 1=0


    