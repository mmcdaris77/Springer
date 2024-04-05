
select 
     cast(null as int) as person_id
    ,cast(null as int) as drug_concept_id
    ,cast(null as int) as unit_concept_id
    ,cast(null as float) as dose_value
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as dose_era_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as dose_era_end_date
where 1=0


    