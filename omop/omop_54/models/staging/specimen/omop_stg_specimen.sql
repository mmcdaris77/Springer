
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_specimen__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.specimen_date, a.specimen_concept_id) as specimen_id
    ,a.person_id
    ,a.specimen_concept_id
    ,a.specimen_type_concept_id
    ,a.specimen_date
    ,a.specimen_datetime
    ,a.quantity
    ,a.unit_concept_id
    ,a.anatomic_site_concept_id
    ,a.disease_status_concept_id
    ,a.specimen_source_id
    ,a.specimen_source_value
    ,a.unit_source_value
    ,a.anatomic_site_source_value
    ,a.disease_status_source_value
from cte_combined a