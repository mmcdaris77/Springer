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
$new_env_name = 'kafka_dev'
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

# back to where it all starte

cd $start_path

docker-compose -f "$start_path/containers/docker-compose.yml" up -d;
python "$start_path/kafka/open_terminals.py"

#####################################################
$h = "-" * 100
write-host $h`n
write-host   "ACTIVATE YOUR ENV IN ANYTIME WITH: $env_path/$new_env_name/Scripts/activate.ps1"
write-host   "use 'deactivate' to deactivate the env in a powershell session"
write-host `n$h


