
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_cost__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.cost_event_id, a.cost_domain_id, a.cost_type_concept_id) as cost_id
    ,a.cost_event_id
    ,a.cost_domain_id
    ,a.cost_type_concept_id
    ,a.currency_concept_id
    ,a.total_charge
    ,a.total_cost
    ,a.total_paid
    ,a.paid_by_payer
    ,a.paid_by_patient
    ,a.paid_patient_copay
    ,a.paid_patient_coinsurance
    ,a.paid_patient_deductible
    ,a.paid_by_primary
    ,a.paid_ingredient_cost
    ,a.paid_dispensing_fee
    ,a.payer_plan_period_id
    ,a.amount_allowed
    ,a.revenue_code_concept_id
    ,a.revenue_code_source_value
    ,a.drg_concept_id
    ,a.drg_source_value
from cte_combined a