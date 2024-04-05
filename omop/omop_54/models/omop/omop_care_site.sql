{{ 
    config(alias='care_site') 
}}



select 
     cast(a.care_site_id as int) as care_site_id
    ,cast(a.care_site_name as varchar(255)) as care_site_name
    ,cast(a.place_of_service_concept_id as int) as place_of_service_concept_id
    ,cast(a.location_id as int) as location_id
    ,cast(a.care_site_source_value as varchar(50)) as care_site_source_value
    ,cast(a.place_of_service_source_value as varchar(50)) as place_of_service_source_value
from {{ ref('omop_stg_care_site') }} a 




