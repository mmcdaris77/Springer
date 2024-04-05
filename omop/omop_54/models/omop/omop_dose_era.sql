{{ 
    config(alias='dose_era') 
}}



select 
     cast(a.dose_era_id as int) as dose_era_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.drug_concept_id as int) as drug_concept_id
    ,cast(a.unit_concept_id as int) as unit_concept_id
    ,cast(a.dose_value as float) as dose_value
    ,{{ dbt.safe_cast("a.dose_era_start_date", api.Column.translate_type("date")) }} as dose_era_start_date
    ,{{ dbt.safe_cast("a.dose_era_end_date", api.Column.translate_type("date")) }} as dose_era_end_date
from {{ ref('omop_stg_dose_era') }} a 




