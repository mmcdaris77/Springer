{{ 
    config(alias='cdm_source') 
}}



select 
     cast(a.cdm_source_name as varchar(255)) as cdm_source_name
    ,cast(a.cdm_source_abbreviation as varchar(25)) as cdm_source_abbreviation
    ,cast(a.cdm_holder as varchar(255)) as cdm_holder
    ,cast(a.source_description as text) as source_description
    ,cast(a.source_documentation_reference as varchar(255)) as source_documentation_reference
    ,cast(a.cdm_etl_reference as varchar(255)) as cdm_etl_reference
    ,{{ dbt.safe_cast("a.source_release_date", api.Column.translate_type("date")) }} as source_release_date
    ,{{ dbt.safe_cast("a.cdm_release_date", api.Column.translate_type("date")) }} as cdm_release_date
    ,cast(a.cdm_version as varchar(10)) as cdm_version
    ,cast(a.cdm_version_concept_id as int) as cdm_version_concept_id
    ,cast(a.vocabulary_version as varchar(20)) as vocabulary_version
from {{ ref('omop_stg_cdm_source') }} a 




