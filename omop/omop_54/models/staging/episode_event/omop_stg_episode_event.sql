
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_episode_event__def')
            ]
        )
    }}
)

select 
     a.episode_id
    ,a.event_id
    ,a.episode_event_field_concept_id
from cte_combined a