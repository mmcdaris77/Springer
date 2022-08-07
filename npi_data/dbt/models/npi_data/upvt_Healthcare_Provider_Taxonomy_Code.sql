{{
    config(
        alias='npi_healthcare_provider_taxonomy_code'
    )
}}


with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Healthcare_Provider_Taxonomy_Code')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(lower(field_name), 'healthcare_provider_taxonomy_code', '') as Seq_Id
    ,value as Taxonomy_Code
from cte_unpivot
where nullif(trim(value), '') is not null