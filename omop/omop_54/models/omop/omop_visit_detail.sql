{{ 
    config(alias='visit_detail') 
}}



select 
     cast(a.visit_detail_id as int) as visit_detail_id
    ,cast(a.person_id as int) as person_id
    ,cast(a.visit_detail_concept_id as int) as visit_detail_concept_id
    ,{{ dbt.safe_cast("a.visit_detail_start_date", api.Column.translate_type("date")) }} as visit_detail_start_date
    ,{{ dbt.safe_cast("a.visit_detail_start_datetime", api.Column.translate_type("timestamp")) }} as visit_detail_start_datetime
    ,{{ dbt.safe_cast("a.visit_detail_end_date", api.Column.translate_type("date")) }} as visit_detail_end_date
    ,{{ dbt.safe_cast("a.visit_detail_end_datetime", api.Column.translate_type("timestamp")) }} as visit_detail_end_datetime
    ,cast(a.visit_detail_type_concept_id as int) as visit_detail_type_concept_id
    ,cast(a.provider_id as int) as provider_id
    ,cast(a.care_site_id as int) as care_site_id
    ,cast(a.visit_detail_source_value as varchar(50)) as visit_detail_source_value
    ,cast(a.visit_detail_source_concept_id as int) as visit_detail_source_concept_id
    ,cast(a.admitted_from_concept_id as int) as admitted_from_concept_id
    ,cast(a.admitted_from_source_value as varchar(50)) as admitted_from_source_value
    ,cast(a.discharged_to_source_value as varchar(50)) as discharged_to_source_value
    ,cast(a.discharged_to_concept_id as int) as discharged_to_concept_id
    ,cast(a.preceding_visit_detail_id as int) as preceding_visit_detail_id
    ,cast(a.parent_visit_detail_id as int) as parent_visit_detail_id
    ,cast(a.visit_occurrence_id as int) as visit_occurrence_id
from {{ ref('omop_stg_visit_detail') }} a 




