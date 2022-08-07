{{
    config(
        alias='npi_usage_states'
    )
}}

with cte_seq as (
    select generated_number as seq_id
    from (
    {{ dbt_utils.generate_series(25) }} 
    ) x
)
, cte_cnt_all as (
    select
        cast(count(npi) as float) as cnt_npi 
    from {{ ref('npidata_pfile') }}
)
, cte_npi_healthcare_provider_primary_taxonomy_switch as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_taxonomy_code_switch
    from {{ ref('upvt_Healthcare_Provider_Primary_Taxonomy_Switch') }}
    group by Seq_Id
)
, cte_taxonomy_code as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_taxonomy_code
    from {{ ref('upvt_Healthcare_Provider_Taxonomy_Code') }}
    group by Seq_Id
)
, cte_other_provider_identifier_issuer as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_other_provider_identifier_issuer
    from {{ ref('upvt_Other_Provider_Identifier_Issuer') }}
    group by Seq_Id
)
, cte_other_provider_identifier_state as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_other_provider_identifier_state
    from {{ ref('upvt_Other_Provider_Identifier_State') }}
    group by Seq_Id
)
, cte_other_provider_identifier_type_code as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_other_provider_identifier_type_code
    from {{ ref('upvt_Other_Provider_Identifier_Type_Code') }}
    group by Seq_Id
)
, cte_other_provider_identifier as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_other_provider_identifier
    from {{ ref('upvt_Other_Provider_Identifier') }}
    group by Seq_Id
)
, cte_provider_license_number_state_code as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_provider_license_number_state_code
    from {{ ref('upvt_Provider_License_Number_State_Code') }}
    group by Seq_Id
)
, cte_provider_license_number as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_provider_license_number
    from {{ ref('upvt_Provider_License_Number') }}
    group by Seq_Id
)
, cte_healthcare_provider_taxonomy_group as (
    select 
        cast(Seq_Id as int) as Seq_Id
        ,count(*) as cnt_healthcare_provider_taxonomy_group
    from {{ ref('upvt_Healthcare_Provider_Taxonomy_Group') }}
    group by Seq_Id
)
select 
     s.seq_id 
    ,ca.cnt_npi
    ,ts.cnt_taxonomy_code_switch
    ,tc.cnt_taxonomy_code
    ,pii.cnt_other_provider_identifier_issuer
    ,pis.cnt_other_provider_identifier_state
    ,pitc.cnt_other_provider_identifier_type_code
    ,opi.cnt_other_provider_identifier
    ,plnsc.cnt_provider_license_number_state_code
    ,pln.cnt_provider_license_number
    ,hptp.cnt_healthcare_provider_taxonomy_group
    -- calc pct usage
    ,(ts.cnt_taxonomy_code_switch / ca.cnt_npi) as pct_taxonomy_code_switch
    ,(tc.cnt_taxonomy_code / ca.cnt_npi) as pct_taxonomy_code
    ,(pii.cnt_other_provider_identifier_issuer / ca.cnt_npi) as pct_other_provider_identifier_issuer
    ,(pis.cnt_other_provider_identifier_state / ca.cnt_npi) as pct_other_provider_identifier_state
    ,(pitc.cnt_other_provider_identifier_type_code / ca.cnt_npi) as pct_other_provider_identifier_type_code
    ,(opi.cnt_other_provider_identifier / ca.cnt_npi) as pct_other_provider_identifier
    ,(plnsc.cnt_provider_license_number_state_code / ca.cnt_npi) as pct_provider_license_number_state_code
    ,(pln.cnt_provider_license_number / ca.cnt_npi) as pct_provider_license_number
    ,(hptp.cnt_healthcare_provider_taxonomy_group / ca.cnt_npi) as pct_healthcare_provider_taxonomy_group
from cte_seq s 
cross join cte_cnt_all ca
left join cte_npi_healthcare_provider_primary_taxonomy_switch ts 
    on ts.Seq_Id = s.Seq_Id
left join cte_taxonomy_code tc
    on tc.Seq_Id = s.Seq_Id
left join cte_other_provider_identifier_issuer pii
    on pii.Seq_Id = s.Seq_Id
left join cte_other_provider_identifier_state pis
    on pis.Seq_Id = s.Seq_Id
left join cte_other_provider_identifier_type_code pitc
    on pitc.Seq_Id = s.Seq_Id
left join cte_other_provider_identifier opi
    on opi.Seq_Id = s.Seq_Id
left join cte_provider_license_number_state_code plnsc
    on plnsc.Seq_Id = s.Seq_Id
left join cte_provider_license_number pln
    on pln.Seq_Id = s.Seq_Id
left join cte_healthcare_provider_taxonomy_group hptp
    on hptp.Seq_Id = s.Seq_Id
