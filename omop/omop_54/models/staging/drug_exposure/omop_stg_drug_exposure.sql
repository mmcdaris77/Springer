
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_drug_exposure__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.drug_exposure_start_date, a.drug_concept_id) as drug_exposure_id
    ,a.person_id
    ,a.drug_concept_id
    ,a.drug_exposure_start_date
    ,a.drug_exposure_start_datetime
    ,a.drug_exposure_end_date
    ,a.drug_exposure_end_datetime
    ,a.verbatim_end_date
    ,a.drug_type_concept_id
    ,a.stop_reason
    ,a.refills
    ,a.quantity
    ,a.days_supply
    ,a.sig
    ,a.route_concept_id
    ,a.lot_number
    ,a.provider_id
    ,a.visit_occurrence_id
    ,a.visit_detail_id
    ,a.drug_source_value
    ,a.drug_source_concept_id
    ,a.route_source_value
    ,a.dose_unit_source_value
from cte_combined a