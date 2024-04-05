{{ 
    config(alias='location') 
}}

select 
     cast(a.location_id as int) as location_id
    ,cast(a.address_1 as varchar(50)) as address_1
    ,cast(a.address_2 as varchar(50)) as address_2
    ,cast(a.city as varchar(50)) as city
    ,cast(a.state as varchar(2)) as state
    ,cast(a.zip as varchar(9)) as zip
    ,cast(a.county as varchar(20)) as county
    ,cast(a.location_source_value as varchar(50)) as location_source_value
    ,cast(a.country_concept_id as int) as country_concept_id
    ,cast(a.country_source_value as varchar(80)) as country_source_value
    ,cast(a.latitude as float) as latitude    -- Must be between -90 and 90
    ,cast(a.longitude as float) as longitude   -- Must be between -180 and 180
from {{ ref('omop_stg_location') }} a 





