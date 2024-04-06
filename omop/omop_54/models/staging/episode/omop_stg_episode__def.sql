
select 
     cast(null as int) as person_id
    ,cast(null as int) as episode_concept_id
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as episode_start_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as episode_start_datetime
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as episode_end_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("timestamp")) }} as episode_end_datetime
    ,cast(null as int) as episode_parent_id
    ,cast(null as int) as episode_number
    ,cast(null as int) as episode_object_concept_id
    ,cast(null as int) as episode_type_concept_id
    ,cast(null as varchar(50)) as episode_source_value
    ,cast(null as int) as episode_source_concept_id
where 1=0


    