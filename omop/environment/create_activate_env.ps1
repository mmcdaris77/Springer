<#
.SYNOPSIS
    .
.DESCRIPTION
    .
.PARAMETER ForceRecreateEnv
    Force the python env to be removed and recreated.  May required the env to be deactivated before running.
.EXAMPLE
    .
.NOTES
    . 
#>

param(
    [switch]$ForceRecreateEnv
)

$install_reqs = $true
$new_env_name = 'dbt_omop'
$requirements_file = "/requirements.txt"
$start_path = (split-path $MyInvocation.MyCommand.Path -parent)
$requirements_file_full = $start_path + $requirements_file

# make a dir for the env:  user/<username>/python_env
$env_path = "$env:USERPROFILE/python_env"
new-item -ItemType Directory -Force -Path $env_path

# if ForceRecreateEnv.. then deate the env before rebuilding
$doc_env_path = "$env_path/$new_env_name"
if ($ForceRecreateEnv) {
    if (Test-Path -LiteralPath $doc_env_path) {
        Remove-Item -LiteralPath $doc_env_path -Recurse -Confirm
    }
}

# create the venv if it does not exist
# set flag if the env is new so reqs can be run
if (!(Test-Path -path $doc_env_path)) {
    cd $env_path
    python -m venv "$env_path/$new_env_name"
    $install_reqs = $true
}
else {
    $install_reqs = $false
}

# activate env
cd "$doc_env_path/Scripts/"
& "$env_path/$new_env_name/Scripts/activate.ps1"
if ($?) {
    write-host 'venv activated.'
} 
else {
    throw 'error in setting up venv'
}

# instal lhe reqs file
if ($install_reqs){
    write-host 'installing reqs from file'
    if([system.IO.File]::Exists($requirements_file_full)) {
        write-host "installing packages from $requirements_file"
        python -m pip install --upgrade pip
        pip install -r $requirements_file_full
    } else {
        write-host "no requirements file found at $requirements_file_full"
    }  
}

# bask to where it all started
cd "$start_path\..\dagster_omop"


#####################################################
# set up dagster env
#####################################################
$env_path = "C:\dagster"
new-item -ItemType Directory -Force -Path $env_path

$dagster_yaml_file = $start_path + "/dagster.yaml"

if (-not (Test-Path 'C:\dagster\dagster.yaml')) {
    copy-Item -Path $dagster_yaml_file -Destination 'C:\dagster'
} 



#####################################################
# start dagster web server
#####################################################

$env:DAGSTER_HOME = "c:\\dagster"; $env:DAGSTER_DBT_PARSE_PROJECT_ON_LOAD = "1"; dagster dev


cd $start_path

#####################################################
$h = "-" * 100
write-host $h`n
write-host   "ACTIVATE YOUR ENV IN ANYTIME WITH: $env_path/$new_env_name/Scripts/activate.ps1"
write-host   "use 'deactivate' to deactivate the env in a powershell session"
write-host `n$h


