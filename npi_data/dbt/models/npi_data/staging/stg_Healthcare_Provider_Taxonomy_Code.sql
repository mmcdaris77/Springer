

select
     npi
    ,Healthcare_Provider_Taxonomy_Code1
    ,Healthcare_Provider_Taxonomy_Code2
    ,Healthcare_Provider_Taxonomy_Code3
    ,Healthcare_Provider_Taxonomy_Code4
    ,Healthcare_Provider_Taxonomy_Code5
    ,Healthcare_Provider_Taxonomy_Code6
    ,Healthcare_Provider_Taxonomy_Code7
    ,Healthcare_Provider_Taxonomy_Code8
    ,Healthcare_Provider_Taxonomy_Code9
    ,Healthcare_Provider_Taxonomy_Code10
    ,Healthcare_Provider_Taxonomy_Code11
    ,Healthcare_Provider_Taxonomy_Code12
    ,Healthcare_Provider_Taxonomy_Code13
    ,Healthcare_Provider_Taxonomy_Code14
    ,Healthcare_Provider_Taxonomy_Code15
from {{ ref('stg_npidata_pfile') }}

