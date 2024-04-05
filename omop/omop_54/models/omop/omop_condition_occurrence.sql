{{ 
    config(alias='condition_occurrence') 
}}



select 
     cast(a.condition_occurrence_id as int) as condition_occurrence_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.condition_concept_id as int) as condition_concept_id
    ,{{ dbt.safe_cast("a.condition_start_date", api.Column.translate_type("date")) }} as condition_start_date
    ,{{ dbt.safe_cast("a.condition_start_datetime", api.Column.translate_type("timestamp")) }} as condition_start_datetime
    ,{{ dbt.safe_cast("a.condition_end_date", api.Column.translate_type("date")) }} as condition_end_date
    ,{{ dbt.safe_cast("a.condition_end_datetime", api.Column.translate_type("timestamp")) }} as condition_end_datetime
    ,cast(a.condition_type_concept_id as int) as condition_type_concept_id
    ,cast(a.condition_status_concept_id as int) as condition_status_concept_id
    ,cast(a.stop_reason as varchar(20)) as stop_reason
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
    ,cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.condition_source_value as varchar(50)) as condition_source_value
    ,cast(a.condition_source_concept_id as int) as condition_source_concept_id
    ,cast(a.condition_status_source_value as varchar(50)) as condition_status_source_value
from {{ ref('omop_stg_condition_occurrence') }} a 




