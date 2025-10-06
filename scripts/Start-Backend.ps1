Param(
    [switch]$SkipInstall,
    [switch]$IncludeDevDependencies,
    [int]$Port = 8080,
    [switch]$EnableDebugger
)

$ErrorActionPreference = "Stop"

function Resolve-PythonCommand {
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "Python 3.11+ is required but was not found on PATH. Install it from https://www.python.org/downloads/windows/"
    }
    return $python.Source
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Push-Location $projectRoot

try {

    $pythonExe = Resolve-PythonCommand
    $venvPath = Join-Path $projectRoot '.venv'
    $venvPython = Join-Path $venvPath 'Scripts\python.exe'
    $venvPoetry = Join-Path $venvPath 'Scripts\poetry.exe'

    if (-not (Test-Path $venvPython)) {
        & $pythonExe -m venv $venvPath
    }

    & $venvPython -m pip install --upgrade pip | Out-Null

    if (-not (Test-Path $venvPoetry)) {
        & $venvPython -m pip install poetry | Out-Null
    }

    $env:POETRY_VIRTUALENVS_IN_PROJECT = '1'
    & $venvPoetry env use $venvPython | Out-Null

    if (-not $SkipInstall) {
        $installArgs = @('install')
        if ($IncludeDevDependencies) {
            $installArgs += '--with'
            $installArgs += 'dev'
        }
        & $venvPoetry @installArgs
    }

    if ($EnableDebugger) {
        $env:DEBUG = '1'
    } else {
        Remove-Item Env:DEBUG -ErrorAction SilentlyContinue | Out-Null
    }

    $runArgs = @('run', 'python', 'src/main.py', '--port', $Port)
    & $venvPoetry @runArgs
}
finally {
    Remove-Item Env:POETRY_VIRTUALENVS_IN_PROJECT -ErrorAction SilentlyContinue | Out-Null
    Pop-Location
}
