
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_metadata__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.metadata_concept_id, a.metadata_date, a.metadata_type_concept_id) as metadata_id
    ,a.metadata_concept_id
    ,a.metadata_type_concept_id
    ,a.name
    ,a.value_as_string
    ,a.value_as_concept_id
    ,a.value_as_number
    ,a.metadata_date
    ,a.metadata_datetime
from cte_combined a