

select 
     npi
    ,Healthcare_Provider_Taxonomy_Group1
    ,Healthcare_Provider_Taxonomy_Group2
    ,Healthcare_Provider_Taxonomy_Group3
    ,Healthcare_Provider_Taxonomy_Group4
    ,Healthcare_Provider_Taxonomy_Group5
    ,Healthcare_Provider_Taxonomy_Group6
    ,Healthcare_Provider_Taxonomy_Group7
    ,Healthcare_Provider_Taxonomy_Group8
    ,Healthcare_Provider_Taxonomy_Group9
    ,Healthcare_Provider_Taxonomy_Group10
    ,Healthcare_Provider_Taxonomy_Group11
    ,Healthcare_Provider_Taxonomy_Group12
    ,Healthcare_Provider_Taxonomy_Group13
    ,Healthcare_Provider_Taxonomy_Group14
    ,Healthcare_Provider_Taxonomy_Group15
from {{ ref('stg_npidata_pfile') }}


