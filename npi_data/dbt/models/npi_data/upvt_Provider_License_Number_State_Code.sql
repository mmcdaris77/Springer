{{
    config(
        alias='npi_provider_license_number_state_code'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Provider_License_Number_State_Code')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(lower(field_name), 'provider_license_number_state_code', '') as Seq_Id
    ,value as State_Code
from cte_unpivot
where nullif(trim(value), '') is not null