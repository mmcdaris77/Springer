
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_measurement__def')
            ]
        )
    }}
)

select 
     row_number() over(order by a.person_id, a.measurement_date, a.measurement_type_concept_id) as measurement_id
    ,a.person_id
    ,a.measurement_concept_id
    ,a.measurement_date
    ,a.measurement_datetime
    ,a.measurement_time
    ,a.measurement_type_concept_id
    ,a.operator_concept_id
    ,a.value_as_number
    ,a.value_as_concept_id
    ,a.unit_concept_id
    ,a.range_low
    ,a.range_high
    ,a.provider_id
    ,a.visit_occurrence_id
    ,a.visit_detail_id
    ,a.unit_source_value
    ,a.unit_source_concept_id
    ,a.value_source_value
    ,a.measurement_event_id
    ,a.meas_event_field_concept_id
from cte_combined a