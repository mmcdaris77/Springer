
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_dose_era__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.dose_era_start_date, a.drug_concept_id) as dose_era_id
    ,a.person_id
    ,a.drug_concept_id
    ,a.unit_concept_id
    ,a.dose_value
    ,a.dose_era_start_date
    ,a.dose_era_end_date
from cte_combined a