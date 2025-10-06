Param(
    [string]$FrontendPath,
    [ValidateSet('npm','yarn','pnpm','bun')]
    [string]$PackageManager = 'npm',
    [string]$ScriptName = 'dev',
    [switch]$SkipInstall,
    [string[]]$ScriptArguments
)

$ErrorActionPreference = 'Stop'

function Ensure-Command($commandName) {
    if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        throw "Required command '$commandName' was not found on PATH. Install it before running this script."
    }
}

$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $FrontendPath) {
    $FrontendPath = Join-Path $projectRoot 'frontend'
}

if (-not (Test-Path $FrontendPath)) {
    throw "Unable to locate a frontend workspace at '$FrontendPath'. Clone the Riven frontend repository into this path or pass -FrontendPath to the script."
}

$packageJson = Join-Path $FrontendPath 'package.json'
if (-not (Test-Path $packageJson)) {
    throw "No package.json found at '$FrontendPath'. Ensure the frontend project is present before running this script."
}

Push-Location $FrontendPath
try {
    Ensure-Command $PackageManager

    if (-not $SkipInstall) {
        switch ($PackageManager) {
            'npm'  { & npm install }
            'yarn' { & yarn install }
            'pnpm' { & pnpm install }
            'bun'  { & bun install }
        }
    }

    $command = @()
    switch ($PackageManager) {
        'npm'  { $command = @('npm', 'run', $ScriptName) }
        'yarn' { $command = @('yarn', $ScriptName) }
        'pnpm' { $command = @('pnpm', 'run', $ScriptName) }
        'bun'  { $command = @('bun', 'run', $ScriptName) }
    }

    if ($ScriptArguments) {
        $command += '--'
        $command += $ScriptArguments
    }

    if ($command.Length -gt 1) {
        & $command[0] @($command[1..($command.Length - 1)])
    } else {
        & $command[0]
    }
}
finally {
    Pop-Location
}
