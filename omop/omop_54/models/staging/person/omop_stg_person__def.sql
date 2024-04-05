

select 
    cast(null as int) as person_id
    ,cast(null as int) as gender_concept_id
    ,cast(null as int) as year_of_birth
    ,cast(null as int) as month_of_birth
    ,cast(null as int) as day_of_birth
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as birth_datetime
    ,cast(null as int) as race_concept_id
    ,cast(null as int) as ethnicity_concept_id
    ,cast(null as int) as location_id
    ,cast(null as int) as provider_id
    ,cast(null as int) as care_site_id
    ,cast(null as varchar(50)) as person_source_value
    ,cast(null as varchar(50)) as gender_source_value
    ,cast(null as int) as gender_source_concept_id
    ,cast(null as varchar(50)) as race_source_value
    ,cast(null as int) as race_source_concept_id
    ,cast(null as varchar(50)) as ethnicity_source_value
    ,cast(null as int) as ethnicity_source_concept_id
where 1=0
