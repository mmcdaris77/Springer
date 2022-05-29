

select 
     npi
    ,Provider_License_Number_State_Code1
    ,Provider_License_Number_State_Code2
    ,Provider_License_Number_State_Code3
    ,Provider_License_Number_State_Code4
    ,Provider_License_Number_State_Code5
    ,Provider_License_Number_State_Code6
    ,Provider_License_Number_State_Code7
    ,Provider_License_Number_State_Code8
    ,Provider_License_Number_State_Code9
    ,Provider_License_Number_State_Code10
    ,Provider_License_Number_State_Code11
    ,Provider_License_Number_State_Code12
    ,Provider_License_Number_State_Code13
    ,Provider_License_Number_State_Code14
    ,Provider_License_Number_State_Code15
from {{ ref('stg_npidata_pfile') }}


