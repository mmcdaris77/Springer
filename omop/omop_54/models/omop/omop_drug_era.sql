{{ 
    config(alias='drug_era') 
}}



select 
     cast(a.drug_era_id as int) as drug_era_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.drug_concept_id as int) as drug_concept_id
    ,{{ dbt.safe_cast("a.drug_era_start_date", api.Column.translate_type("date")) }} as drug_era_start_date
    ,{{ dbt.safe_cast("a.drug_era_end_date", api.Column.translate_type("date")) }} as drug_era_end_date
    ,cast(a.drug_exposure_count as int) as drug_exposure_count
    ,cast(a.gap_days as int) as gap_days
from {{ ref('omop_stg_drug_era') }} a 




