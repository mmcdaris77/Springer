
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_payer_plan_period__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.payer_plan_period_start_date, a.payer_concept_id) as payer_plan_period_id
    ,a.person_id
    ,a.payer_plan_period_start_date
    ,a.payer_plan_period_end_date
    ,a.payer_concept_id
    ,a.payer_source_value
    ,a.payer_source_concept_id
    ,a.plan_concept_id
    ,a.plan_source_value
    ,a.plan_source_concept_id
    ,a.sponsor_concept_id
    ,a.sponsor_source_value
    ,a.sponsor_source_concept_id
    ,a.family_source_value
    ,a.stop_reason_concept_id
    ,a.stop_reason_source_value
    ,a.stop_reason_source_concept_id
from cte_combined a