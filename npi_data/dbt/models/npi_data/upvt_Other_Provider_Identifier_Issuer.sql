{{
    config(
        alias='npi_other_provider_identifier_issuer'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Other_Provider_Identifier_Issuer')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(lower(field_name), 'other_provider_identifier_issuer', '') as Seq_Id
    ,value as Provider_Identifier_Issuer
from cte_unpivot
where nullif(trim(value), '') is not null