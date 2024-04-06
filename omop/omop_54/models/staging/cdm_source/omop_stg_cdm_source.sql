
with cte_combined as (
    {{
        dbt_utils.union_relations(
            [
                ref('omop_stg_cdm_source__def')
            ]
        )
    }}
)

select 
     a.cdm_source_name
    ,a.cdm_source_abbreviation
    ,a.cdm_holder
    ,a.source_description
    ,a.source_documentation_reference
    ,a.cdm_etl_reference
    ,a.source_release_date
    ,a.cdm_release_date
    ,a.cdm_version
    ,a.cdm_version_concept_id
    ,a.vocabulary_version
from cte_combined a