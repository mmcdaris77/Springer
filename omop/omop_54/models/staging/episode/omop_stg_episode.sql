
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_episode__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.episode_start_date, a.episode_concept_id) as episode_id
    ,a.person_id
    ,a.episode_concept_id
    ,a.episode_start_date
    ,a.episode_start_datetime
    ,a.episode_end_date
    ,a.episode_end_datetime
    ,a.episode_parent_id
    ,a.episode_number
    ,a.episode_object_concept_id
    ,a.episode_type_concept_id
    ,a.episode_source_value
    ,a.episode_source_concept_id
from cte_combined a