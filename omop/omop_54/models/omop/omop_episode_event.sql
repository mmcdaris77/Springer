{{ 
    config(alias='episode_event') 
}}



select 
     cast(a.episode_id as int) as episode_id
    ,cast(a.event_id as int) as event_id
    ,cast(a.episode_event_field_concept_id as int) as episode_event_field_concept_id
from {{ ref('omop_stg_episode_event') }} a 




