
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_drug_era__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.drug_era_start_date, a.drug_concept_id) as drug_era_id
    ,a.person_id
    ,a.drug_concept_id
    ,a.drug_era_start_date
    ,a.drug_era_end_date
    ,a.drug_exposure_count
    ,a.gap_days
from cte_combined a