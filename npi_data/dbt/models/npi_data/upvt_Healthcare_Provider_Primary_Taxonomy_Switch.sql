{{
    config(
        alias='npi_healthcare_provider_primary_taxonomy_switch'
    )
}}


with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Healthcare_Provider_Primary_Taxonomy_Switch')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(lower(field_name), 'healthcare_provider_primary_taxonomy_switch', '') as Seq_Id
    ,value as Taxonomy_Code_Switch
from cte_unpivot
where nullif(trim(value), '') is not null