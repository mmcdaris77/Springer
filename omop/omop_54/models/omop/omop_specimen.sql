{{ 
    config(alias='specimen') 
}}



select
     cast(a.specimen_id as int) as specimen_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.specimen_concept_id as int) as specimen_concept_id
    ,cast(a.specimen_type_concept_id as int) as specimen_type_concept_id
    ,{{ dbt.safe_cast("a.specimen_date", api.Column.translate_type("date")) }} as specimen_date
    ,{{ dbt.safe_cast("a.specimen_datetime", api.Column.translate_type("timestamp")) }} as specimen_datetime
    ,cast(a.quantity as float) as quantity
    ,cast(a.unit_concept_id as int) as unit_concept_id
    ,cast(a.anatomic_site_concept_id as int) as anatomic_site_concept_id
    ,cast(a.disease_status_concept_id as int) as disease_status_concept_id
    ,cast(a.specimen_source_id as int) as specimen_source_id
    ,cast(a.specimen_source_value as varchar(50)) as specimen_source_value
    ,cast(a.unit_source_value as varchar(50)) as unit_source_value
    ,cast(a.anatomic_site_source_value as varchar(50)) as anatomic_site_source_value
    ,cast(a.disease_status_source_value as varchar(50)) as disease_status_source_value
from {{ ref('omop_stg_specimen') }} a 




