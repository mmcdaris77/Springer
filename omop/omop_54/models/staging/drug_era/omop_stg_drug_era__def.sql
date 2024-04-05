
select 
     cast(null as int) as person_id
    ,cast(null as int) as drug_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as drug_era_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as drug_era_end_date
    ,cast(null as int) as drug_exposure_count
    ,cast(null as int) as gap_days
where 1=0


    