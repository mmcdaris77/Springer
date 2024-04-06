{{ 
    config(alias='metadata') 
}}



select 
     cast(a.metadata_id as int) as metadata_id
    ,cast(a.metadata_concept_id as int) as metadata_concept_id
    ,cast(a.metadata_type_concept_id as int) as metadata_type_concept_id
    ,cast(a.name as varchar(250)) as name
    ,cast(a.value_as_string as varchar(250)) as value_as_string
    ,cast(a.value_as_concept_id as int) as value_as_concept_id
    ,cast(a.value_as_number as float) as value_as_number
    ,{{ dbt.safe_cast("a.metadata_date", api.Column.translate_type("date")) }} as metadata_date
    ,{{ dbt.safe_cast("a.metadata_datetime", api.Column.translate_type("timestamp")) }} as metadata_datetime
from {{ ref('omop_stg_metadata') }} a 




