{{
    config(
        alias='npi_provider_license_number'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Provider_License_Number')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(field_name, 'Provider_License_Number', '') as Seq_Id
    ,value as License_Number
from cte_unpivot
where nullif(trim(value), '') is not null