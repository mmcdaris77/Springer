
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_person__def')
            ]
        )
    }}
)

select
     row_number() over(order by a.person_source_value) as person_id
    ,a.gender_concept_id
    ,a.year_of_birth
    ,a.month_of_birth
    ,a.day_of_birth
    ,a.birth_datetime
    ,a.race_concept_id
    ,a.ethnicity_concept_id
    ,a.location_id
    ,a.provider_id
    ,a.care_site_id
    ,a.person_source_value
    ,a.gender_source_value
    ,a.gender_source_concept_id
    ,a.race_source_value
    ,a.race_source_concept_id
    ,a.ethnicity_source_value
    ,a.ethnicity_source_concept_id
from cte_combined a