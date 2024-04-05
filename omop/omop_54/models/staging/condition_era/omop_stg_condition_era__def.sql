
select      
     cast(null as int) as person_id
    ,cast(null as int) as condition_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as condition_era_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as condition_era_end_date
    ,cast(null as int) as condition_occurrence_count
where 1=0


    