

select
     npi
    ,Healthcare_Provider_Primary_Taxonomy_Switch1
    ,Healthcare_Provider_Primary_Taxonomy_Switch2
    ,Healthcare_Provider_Primary_Taxonomy_Switch3
    ,Healthcare_Provider_Primary_Taxonomy_Switch4
    ,Healthcare_Provider_Primary_Taxonomy_Switch5
    ,Healthcare_Provider_Primary_Taxonomy_Switch6
    ,Healthcare_Provider_Primary_Taxonomy_Switch7
    ,Healthcare_Provider_Primary_Taxonomy_Switch8
    ,Healthcare_Provider_Primary_Taxonomy_Switch9
    ,Healthcare_Provider_Primary_Taxonomy_Switch10
    ,Healthcare_Provider_Primary_Taxonomy_Switch11
    ,Healthcare_Provider_Primary_Taxonomy_Switch12
    ,Healthcare_Provider_Primary_Taxonomy_Switch13
    ,Healthcare_Provider_Primary_Taxonomy_Switch14
    ,Healthcare_Provider_Primary_Taxonomy_Switch15
from {{ ref('stg_npidata_pfile') }}

