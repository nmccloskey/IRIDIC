param(
    [string[]]$PytestArgs = @("tests")
)

$ErrorActionPreference = "Stop"

$Python = if ($env:REPO_PYTHON) {
    $env:REPO_PYTHON
} else {
    "$env:USERPROFILE\anaconda3\envs\repo\python.exe"
}

if (-not (Test-Path $Python)) {
    throw "Could not find REPO Python at $Python. Set REPO_PYTHON to override."
}

& $Python -m pytest @PytestArgs
exit $LASTEXITCODE
