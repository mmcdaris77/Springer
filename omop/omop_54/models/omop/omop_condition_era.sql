{{ 
    config(alias='condition_era') 
}}



select 
     cast(a.condition_era_id as int) as condition_era_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.condition_concept_id as int) as condition_concept_id
    ,{{ dbt.safe_cast("a.condition_era_start_date", api.Column.translate_type("date")) }} as condition_era_start_date
    ,{{ dbt.safe_cast("a.condition_era_end_date", api.Column.translate_type("date")) }} as condition_era_end_date
    ,cast(a.condition_occurrence_count as int) as condition_occurrence_count
from {{ ref('omop_stg_condition_era') }} a 




