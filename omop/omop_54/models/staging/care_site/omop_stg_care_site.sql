
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_care_site__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.care_site_source_value) as care_site_id
    ,a.care_site_name
    ,a.place_of_service_concept_id
    ,a.location_id
    ,a.care_site_source_value
    ,a.place_of_service_source_value
from cte_combined a