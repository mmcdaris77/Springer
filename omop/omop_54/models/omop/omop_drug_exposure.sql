{{ 
    config(alias='drug_exposure') 
}}



select 
     cast(a.drug_exposure_id as int) as drug_exposure_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.drug_concept_id as int) as drug_concept_id
    ,{{ dbt.safe_cast("a.drug_exposure_start_date", api.Column.translate_type("date")) }} as drug_exposure_start_date
    ,{{ dbt.safe_cast("a.drug_exposure_start_datetime", api.Column.translate_type("timestamp")) }} as drug_exposure_start_datetime
    ,{{ dbt.safe_cast("a.drug_exposure_end_date", api.Column.translate_type("date")) }} as drug_exposure_end_date
    ,{{ dbt.safe_cast("a.drug_exposure_end_datetime", api.Column.translate_type("timestamp")) }} as drug_exposure_end_datetime
    ,{{ dbt.safe_cast("a.verbatim_end_date", api.Column.translate_type("date")) }} as verbatim_end_date
    ,cast(a.drug_type_concept_id as int) as drug_type_concept_id
    ,cast(a.stop_reason as varchar(20)) as stop_reason
    ,cast(a.refills as int) as refills
    ,cast(a.quantity as float) as quantity
    ,cast(a.days_supply as int) as days_supply
    ,cast(a.sig as text) as sig
    ,cast(a.route_concept_id as int) as route_concept_id
    ,cast(a.lot_number as varchar(50)) as lot_number
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
    ,cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.drug_source_value as varchar(50)) as drug_source_value
    ,cast(a.drug_source_concept_id as int) as drug_source_concept_id
    ,cast(a.route_source_value as varchar(50)) as route_source_value
    ,cast(a.dose_unit_source_value as varchar(50)) as dose_unit_source_value
from {{ ref('omop_stg_drug_exposure') }} a 




