
select 
     cast(null as varchar(255)) as cdm_source_name
    ,cast(null as varchar(25)) as cdm_source_abbreviation
    ,cast(null as varchar(255)) as cdm_holder
    ,cast(null as text) as source_description
    ,cast(null as varchar(255)) as source_documentation_reference
    ,cast(null as varchar(255)) as cdm_etl_reference
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as source_release_date
    ,{{ dbt.safe_cast("null", api.Column.translate_type("date")) }} as cdm_release_date
    ,cast(null as varchar(10)) as cdm_version
    ,cast(null as int) as cdm_version_concept_id
    ,cast(null as varchar(20)) as vocabulary_version
where 1=0


    