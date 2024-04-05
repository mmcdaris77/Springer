
select 
     cast(null as int) as person_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as payer_plan_period_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as payer_plan_period_end_date
    ,cast(null as int) as payer_concept_id
    ,cast(null as varchar(50)) as payer_source_value
    ,cast(null as int) as payer_source_concept_id
    ,cast(null as int) as plan_concept_id
    ,cast(null as varchar(50)) as plan_source_value
    ,cast(null as int) as plan_source_concept_id
    ,cast(null as int) as sponsor_concept_id
    ,cast(null as varchar(50)) as sponsor_source_value
    ,cast(null as int) as sponsor_source_concept_id
    ,cast(null as varchar(50)) as family_source_value
    ,cast(null as int) as stop_reason_concept_id
    ,cast(null as varchar(50)) as stop_reason_source_value
    ,cast(null as int) as stop_reason_source_concept_id
where 1=0



    
    
    