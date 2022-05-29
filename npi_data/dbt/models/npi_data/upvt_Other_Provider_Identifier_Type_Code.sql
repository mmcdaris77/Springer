{{
    config(
        alias='npi_other_provider_identifier_type_code'
    )
}}

with cte_unpivot as (
{{
    dbt_utils.unpivot(
        relation = ref('stg_Other_Provider_Identifier_Type_Code')
        ,exclude=['npi']
        ,cast_to='varchar(100)'
    )
}}
)

select 
     npi
    ,replace(field_name, 'Other_Provider_Identifier_Type_Code', '') as Seq_Id
    ,value as Provider_Identifier_Type_Code
from cte_unpivot
where nullif(trim(value), '') is not null