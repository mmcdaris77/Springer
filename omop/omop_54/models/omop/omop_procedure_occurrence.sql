{{ 
    config(alias='procedure_occurrence') 
}}



select 
     cast(a.procedure_occurrence_id as int) as procedure_occurrence_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.procedure_concept_id as int) as procedure_concept_id
    ,{{ dbt.safe_cast("a.procedure_date", api.Column.translate_type("date")) }} as procedure_date
    ,{{ dbt.safe_cast("a.procedure_datetime", api.Column.translate_type("timestamp")) }} as procedure_datetime
    ,{{ dbt.safe_cast("a.procedure_end_date", api.Column.translate_type("date")) }} as procedure_end_date
    ,{{ dbt.safe_cast("a.procedure_end_datetime", api.Column.translate_type("timestamp")) }} as procedure_end_datetime
    ,cast(a.procedure_type_concept_id as int) as procedure_type_concept_id
    ,cast(a.modifier_concept_id as int) as modifier_concept_id
    ,cast(a.quantity as int) as quantity
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
    ,cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.procedure_source_value as varchar(50)) as procedure_source_value
    ,cast(a.procedure_source_concept_id as int) as procedure_source_concept_id
    ,cast(a.modifier_source_value as varchar(50)) as modifier_source_value
from {{ ref('omop_stg_procedure_occurrence') }} a 




