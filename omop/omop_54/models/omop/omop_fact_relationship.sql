{{ 
    config(alias='fact_relationship') 
}}



select 
     cast(a.domain_concept_id_1 as int) as domain_concept_id_1
    ,cast(a.fact_id_1 as int) as fact_id_1
    ,cast(a.domain_concept_id_2 as int) as domain_concept_id_2
    ,cast(a.fact_id_2 as int) as fact_id_2
    ,cast(a.relationship_concept_id as int) as relationship_concept_id
from {{ ref('omop_stg_fact_relationship') }} a 




