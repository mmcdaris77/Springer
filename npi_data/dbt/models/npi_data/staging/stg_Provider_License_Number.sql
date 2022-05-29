

select 
     npi
    ,Provider_License_Number1
    ,Provider_License_Number2
    ,Provider_License_Number3
    ,Provider_License_Number4
    ,Provider_License_Number5
    ,Provider_License_Number6
    ,Provider_License_Number7
    ,Provider_License_Number8
    ,Provider_License_Number9
    ,Provider_License_Number10
    ,Provider_License_Number11
    ,Provider_License_Number12
    ,Provider_License_Number13
    ,Provider_License_Number14
    ,Provider_License_Number15
from {{ ref('stg_npidata_pfile') }}


