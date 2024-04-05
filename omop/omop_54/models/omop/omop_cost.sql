{{ 
    config(alias='cost') 
}}



select 
     cast(a.cost_id as int) as cost_id
    ,cast(a.cost_event_id as int) as cost_event_id
    ,cast(a.cost_domain_id as int) as cost_domain_id
    ,cast(a.cost_type_concept_id as int) as cost_type_concept_id
    ,cast(a.currency_concept_id as int) as currency_concept_id
    ,cast(a.total_charge as float) as total_charge
    ,cast(a.total_cost as float) as total_cost
    ,cast(a.total_paid as float) as total_paid
    ,cast(a.paid_by_payer as float) as paid_by_payer
    ,cast(a.paid_by_patient as float) as paid_by_patient
    ,cast(a.paid_patient_copay as float) as paid_patient_copay
    ,cast(a.paid_patient_coinsurance as float) as paid_patient_coinsurance
    ,cast(a.paid_patient_deductible as float) as paid_patient_deductible
    ,cast(a.paid_by_primary as float) as paid_by_primary
    ,cast(a.paid_ingredient_cost as float) as paid_ingredient_cost
    ,cast(a.paid_dispensing_fee as float) as paid_dispensing_fee
    ,cast(a.payer_plan_period_id as int) as payer_plan_period_id
    ,cast(a.amount_allowed as float) as amount_allowed
    ,cast(a.revenue_code_concept_id as int) as revenue_code_concept_id
    ,cast(a.revenue_code_source_value as varchar(50)) as revenue_code_source_value
    ,cast(a.drg_concept_id as int) as drg_concept_id
    ,cast(a.drg_source_value as varchar(3)) as drg_source_value
from {{ ref('omop_stg_cost') }} a 




