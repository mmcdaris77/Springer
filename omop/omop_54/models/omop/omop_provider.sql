{{ 
    config(alias='provider') 
}}


select 
     cast(provider_id as int) as provider_id
    ,cast(provider_name as varchar(255)) as provider_name
    ,cast(npi as varchar(20)) as npi
    ,cast(dea as varchar(20)) as dea
    ,cast(specialty_concept_id as int) as specialty_concept_id
    ,cast(care_site_id as int) as care_site_id
    ,cast(year_of_birth as int) as year_of_birth
    ,cast(gender_concept_id as int) as gender_concept_id
    ,cast(provider_source_value as varchar(50)) as provider_source_value
    ,cast(specialty_source_value as varchar(50)) as specialty_source_value
    ,cast(specialty_source_concept_id as int) as specialty_source_concept_id
    ,cast(gender_source_value as varchar(50)) as gender_source_value
    ,cast(gender_source_concept_id as int) as gender_source_concept_id
from {{ ref('omop_stg_provider') }} a









