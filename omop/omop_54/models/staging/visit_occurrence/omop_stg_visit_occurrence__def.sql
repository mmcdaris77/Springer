
select 
     cast(null as int) as visit_concept_id
    ,cast(null as int) as person_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as visit_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as visit_start_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as visit_end_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as visit_end_datetime
    ,cast(null as int) as visit_type_concept_id
    ,cast(null as int) as provider_id
    ,cast(null as int) as care_site_id
    ,cast(null as varchar(50)) as visit_source_value
    ,cast(null as int) as visit_source_concept_id
    ,cast(null as int) as admitted_from_concept_id
    ,cast(null as varchar(50)) as admitted_from_source_value
    ,cast(null as int) as discharged_to_concept_id
    ,cast(null as varchar(50)) as discharged_to_source_value
    ,cast(null as int) as preceding_visit_occurrence_id
where 1=0


    
    









