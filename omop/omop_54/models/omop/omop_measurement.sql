{{ 
    config(alias='measurement') 
}}



select 
     cast(a.measurement_id as int) as measurement_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.measurement_concept_id as int) as measurement_concept_id
    ,{{ dbt.safe_cast("a.measurement_date", api.Column.translate_type("date")) }} as measurement_date
    ,{{ dbt.safe_cast("a.measurement_datetime", api.Column.translate_type("timestamp")) }} as measurement_datetime
    ,cast(a.measurement_time as varchar(10)) as measurement_time
    ,cast(a.measurement_type_concept_id as int) as measurement_type_concept_id
    ,cast(a.operator_concept_id as int) as operator_concept_id
    ,cast(a.value_as_number as float) as value_as_number
    ,cast(a.value_as_concept_id as int) as value_as_concept_id
    ,cast(a.unit_concept_id as int) as unit_concept_id
    ,cast(a.range_low as float) as range_low
    ,cast(a.range_high as float) as range_high
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
    ,cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.unit_source_value as varchar(50)) as unit_source_value
    ,cast(a.unit_source_concept_id as int) as unit_source_concept_id
    ,cast(a.value_source_value as varchar(50)) as value_source_value
    ,cast(a.measurement_event_id as int) as measurement_event_id
    ,cast(a.meas_event_field_concept_id as int) as meas_event_field_concept_id
from {{ ref('omop_stg_measurement') }} a 




