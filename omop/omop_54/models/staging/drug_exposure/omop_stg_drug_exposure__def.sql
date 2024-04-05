
select 
     cast(null as int) as person_id
    ,cast(null as int) as drug_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as drug_exposure_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as drug_exposure_start_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as drug_exposure_end_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as drug_exposure_end_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as verbatim_end_date
    ,cast(null as int) as drug_type_concept_id
    ,cast(null as varchar(20)) as stop_reason
    ,cast(null as int) as refills
    ,cast(null as float) as quantity
    ,cast(null as int) as days_supply
    ,cast(null as text) as sig
    ,cast(null as int) as route_concept_id
    ,cast(null as varchar(50)) as lot_number
    ,cast(null as int) as provider_id
    ,cast(null as int) as visit_occurrence_id
    ,cast(null as int) as visit_detail_id
    ,cast(null as varchar(50)) as drug_source_value
    ,cast(null as int) as drug_source_concept_id
    ,cast(null as varchar(50)) as route_source_value
    ,cast(null as varchar(50)) as dose_unit_source_value
where 1=0


    