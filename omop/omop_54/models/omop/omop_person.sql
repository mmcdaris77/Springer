{{ 
    config(alias='person') 
}}


select 
     cast(a.person_id as int) as person_id
    ,cast(a.gender_concept_id as int) as gender_concept_id
    ,cast(a.year_of_birth as int) as year_of_birth
    ,cast(a.month_of_birth as int) as month_of_birth
    ,cast(a.day_of_birth as int) as day_of_birth
    ,{{ dbt.safe_cast("a.birth_datetime", api.Column.translate_type("timestamp")) }} as birth_datetime
    ,cast(a.race_concept_id as int) as race_concept_id
    ,cast(a.ethnicity_concept_id as int) as ethnicity_concept_id
    ,cast(a.location_id as int) as location_id
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.care_site_id as int) as care_site_id
    ,cast(a.person_source_value as varchar(50)) as person_source_value
    ,cast(a.gender_source_value as varchar(50)) as gender_source_value
    ,cast(a.gender_source_concept_id as int) as gender_source_concept_id
    ,cast(a.race_source_value as varchar(50)) as race_source_value
    ,cast(a.race_source_concept_id as int) as race_source_concept_id
    ,cast(a.ethnicity_source_value as varchar(50)) as ethnicity_source_value
    ,cast(a.ethnicity_source_concept_id as int) as ethnicity_source_concept_id
from {{ ref('omop_stg_person') }} a





