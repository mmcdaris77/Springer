{{
    config(
        alias='npi_healthcare_provider_taxonomy_group'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Healthcare_Provider_Taxonomy_Group')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(field_name, 'Healthcare_Provider_Taxonomy_Group', '') as Seq_Id
    ,value as License_Number
from cte_unpivot
where nullif(trim(value), '') is not null