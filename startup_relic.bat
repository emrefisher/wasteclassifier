NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program $YOUR_COMMAND_OPTIONS;
[Net.ServicePointManager]::SecurityProtocol = 'tls12, tls'; (New-Object System.Net.WebClient).DownloadFile("https://download.newrelic.com/install/newrelic-cli/scripts/install.ps1", "$env:TEMP\install.ps1"); & $env:TEMP\install.ps1; $env:NEW_RELIC_API_KEY='NRAK-U2WRFY6DWA2QYOLZFT35JHAIIFV'; $env:NEW_RELIC_ACCOUNT_ID='3913539'; & 'C:\Program Files\New Relic\New Relic CLI\newrelic.exe' install -n logs-integration;