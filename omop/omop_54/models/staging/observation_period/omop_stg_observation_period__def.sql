
select 
     cast(null as int) as person_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as observation_period_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as observation_period_end_date
    ,cast(null as int) as period_type_concept_id
where 1=0


    