{{ 
    config(alias='payer_plan_period') 
}}



select 
     cast(a.payer_plan_period_id as int) as payer_plan_period_id
    ,cast(a.person_id as int) as person_id
    ,{{ dbt.safe_cast("a.payer_plan_period_start_date", api.Column.translate_type("date")) }} as payer_plan_period_start_date
    ,{{ dbt.safe_cast("a.payer_plan_period_end_date", api.Column.translate_type("date")) }} as payer_plan_period_end_date
    ,cast(a.payer_concept_id as int) as payer_concept_id
    ,cast(a.payer_source_value as varchar(50)) as payer_source_value
    ,cast(a.payer_source_concept_id as int) as payer_source_concept_id
    ,cast(a.plan_concept_id as int) as plan_concept_id
    ,cast(a.plan_source_value as varchar(50)) as plan_source_value
    ,cast(a.plan_source_concept_id as int) as plan_source_concept_id
    ,cast(a.sponsor_concept_id as int) as sponsor_concept_id
    ,cast(a.sponsor_source_value as varchar(50)) as sponsor_source_value
    ,cast(a.sponsor_source_concept_id as int) as sponsor_source_concept_id
    ,cast(a.family_source_value as varchar(50)) as family_source_value
    ,cast(a.stop_reason_concept_id as int) as stop_reason_concept_id
    ,cast(a.stop_reason_source_value as varchar(50)) as stop_reason_source_value
    ,cast(a.stop_reason_source_concept_id as int) as stop_reason_source_concept_id
from {{ ref('omop_stg_payer_plan_period') }} a 




