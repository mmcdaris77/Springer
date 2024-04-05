
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_location__def')
            ]
        )
    }}
)

select
     row_number() over(order by a.location_source_value) as location_id
    ,a.address_1
    ,a.address_2
    ,a.city
    ,a.state
    ,a.zip
    ,a.county
    ,a.location_source_value
    ,a.country_concept_id
    ,a.country_source_value
    ,a.latitude    -- Must be between -90 and 90
    ,a.longitude   -- Must be between -180 and 180
from cte_combined a