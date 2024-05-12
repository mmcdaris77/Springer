    // set default terminal
    "terminal.integrated.defaultProfile.windows": "GIT BASH", 
    "terminal.integrated.profiles.windows": {
        "DBT_1.6.0": {
            "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "args": [
                "-noexit",
                "if([System.IO.Directory]::Exists(\"$pwd\\\\ic5_nophi\")){cd ic5_nophi};",
                "if([System.IO.File]::Exists(\"${env:HOMEPATH}\\\\python_env\\\\dbt_1_6_0\\\\Scripts\\\\activate.ps1\")){${env:HOMEPATH}/python_env/dbt_1_6_0/Scripts/activate.ps1};",
                "python --version;",
                "write-host hello miguel.  You are going to be awesome today!"
                
            ],
            "icon": "octoface",
            "overrideName": true
        },
        "DAGSTER": {
            "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "args": [
                "-noexit",
                "if([System.IO.File]::Exists(\"${env:HOMEPATH}\\\\python_env\\\\dagster_dbt\\\\Scripts\\\\activate.ps1\")){${env:HOMEPATH}/python_env/dagster_dbt/Scripts/activate.ps1};",
                "python --version;"
                
            ],
            "icon": "hubot",
            "overrideName": true
        },
        "KAFKA": {
            "path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
            "args": [
                "-noexit",
                "if([System.IO.File]::Exists(\"C:\\\\Users\\\\michael.mcdaris\\\\Documents\\\\projects_local\\\\containers\\\\kafka\\\\docker-compose.yml\")){ docker-compose -f \"C:\\\\Users\\\\michael.mcdaris\\\\Documents\\\\projects_local\\\\containers\\\\kafka\\\\docker-compose.yml\" up -d; cd \"C:\\\\Users\\\\michael.mcdaris\\\\Documents\\\\projects_local\\\\python\\\\kafka\"};",
                "if([System.IO.File]::Exists(\"${env:HOMEPATH}\\\\python_env\\\\kafka\\\\Scripts\\\\activate.ps1\")){${env:HOMEPATH}/python_env/kafka/Scripts/activate.ps1};",
                "python --version;"
                
            ],
            "icon": "hubot",
            "overrideName": true
        },
        "Command Prompt": {
            "path": [
                "${env:windir}\\Sysnative\\cmd.exe",
                "${env:windir}\\System32\\cmd.exe"
            ],
            "args": [],
            "icon": "terminal-cmd"
        },
        "GIT BASH": {
            "source": "Git Bash",
            "icon": "github-alt",
            "overrideName": true
        }
    }