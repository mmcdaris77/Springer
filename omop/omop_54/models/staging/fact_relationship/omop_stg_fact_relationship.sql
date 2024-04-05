
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_fact_relationship__def')
            ]
        )
    }}
)

select 
     a.domain_concept_id_1
    ,a.fact_id_1
    ,a.domain_concept_id_2
    ,a.fact_id_2
    ,a.relationship_concept_id
from cte_combined a