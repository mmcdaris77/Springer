{{ 
    config(alias='death') 
}}



select 
     cast(person_id as int) as person_id
    ,{{ dbt.safe_cast("death_date", api.Column.translate_type("date")) }} as death_date
    ,{{ dbt.safe_cast("death_datetime", api.Column.translate_type("timestamp")) }} as death_datetime
    ,cast(death_type_concept_id as int) as death_type_concept_id
    ,cast(cause_concept_id as int) as cause_concept_id
    ,cast(cause_source_value as varchar(50)) as cause_source_value
    ,cast(cause_source_concept_id as int) as cause_source_concept_id
from {{ ref('omop_stg_death') }} a 




