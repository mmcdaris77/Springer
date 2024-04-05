
select 
     cast(null as int) as person_id
    ,cast(null as int) as specimen_concept_id
    ,cast(null as int) as specimen_type_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as specimen_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as specimen_datetime
    ,cast(null as float) as quantity
    ,cast(null as int) as unit_concept_id
    ,cast(null as int) as anatomic_site_concept_id
    ,cast(null as int) as disease_status_concept_id
    ,cast(null as int) as specimen_source_id
    ,cast(null as varchar(50)) as specimen_source_value
    ,cast(null as varchar(50)) as unit_source_value
    ,cast(null as varchar(50)) as anatomic_site_source_value
    ,cast(null as varchar(50)) as disease_status_source_value
where 1=0


    