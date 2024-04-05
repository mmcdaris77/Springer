
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_provider__def')
            ]
        )
    }}
)

select
     row_number() over(order by a.provider_source_value) as provider_id
    ,a.provider_name
    ,a.npi
    ,a.dea
    ,a.specialty_concept_id
    ,a.care_site_id
    ,a.year_of_birth
    ,a.gender_concept_id
    ,a.provider_source_value
    ,a.specialty_source_value
    ,a.specialty_source_concept_id
    ,a.gender_source_value
    ,a.gender_source_concept_id
from cte_combined a
