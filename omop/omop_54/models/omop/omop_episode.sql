{{ 
    config(alias='episode') 
}}



select 
     cast(a.episode_id as int) as episode_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.episode_concept_id as int) as episode_concept_id
    ,{{ dbt.safe_cast("a.episode_start_date", api.Column.translate_type("date")) }} as episode_start_date
    ,{{ dbt.safe_cast("a.episode_start_datetime", api.Column.translate_type("timestamp")) }} as episode_start_datetime
    ,{{ dbt.safe_cast("a.episode_end_date", api.Column.translate_type("date")) }} as episode_end_date
    ,{{ dbt.safe_cast("a.episode_end_datetime", api.Column.translate_type("timestamp")) }} as episode_end_datetime
    ,cast(a.episode_parent_id as int) as episode_parent_id
    ,cast(a.episode_number as int) as episode_number
    ,cast(a.episode_object_concept_id as int) as episode_object_concept_id
    ,cast(a.episode_type_concept_id as int) as episode_type_concept_id
    ,cast(a.episode_source_value as varchar(50)) as episode_source_value
    ,cast(a.episode_source_concept_id as int) as episode_source_concept_id
from {{ ref('omop_stg_episode') }} a 




