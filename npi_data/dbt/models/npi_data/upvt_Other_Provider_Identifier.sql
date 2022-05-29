{{
    config(
        alias='npi_other_provider_identifier'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Other_Provider_Identifier')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(field_name, 'Other_Provider_Identifier', '') as Seq_Id
    ,value as Provider_Identifier
from cte_unpivot
where nullif(trim(value), '') is not null