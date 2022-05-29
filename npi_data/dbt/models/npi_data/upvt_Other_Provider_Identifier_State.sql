{{
    config(
        alias='npi_other_provider_identifier_state'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Other_Provider_Identifier_State')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(field_name, 'Other_Provider_Identifier_State', '') as Seq_Id
    ,value as Provider_Identifier_State
from cte_unpivot
where nullif(trim(value), '') is not null