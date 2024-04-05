{{ 
    config(alias='observation_period') 
}}



select 
    cast(a.observation_period_id as int) as observation_period_id
    ,cast(a.person_id as int) as person_id
    ,{{ dbt.safe_cast("a.observation_period_start_date", api.Column.translate_type("date")) }} as observation_period_start_date
    ,{{ dbt.safe_cast("a.observation_period_end_date", api.Column.translate_type("date")) }} as observation_period_end_date
    ,cast(a.period_type_concept_id as int) as period_type_concept_id
from {{ ref('omop_stg_observation_period') }} a 




