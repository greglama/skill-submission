$ErrorActionPreference = "Stop"

$SkillRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $SkillRoot ".venv"
$VenvPython = Join-Path $VenvPath "Scripts\python.exe"
$Requirements = Join-Path $SkillRoot "requirements.txt"

function Test-PythonCommand {
    param(
        [string]$Command,
        [string[]]$Arguments
    )

    try {
        & $Command @Arguments -c "import sys; print(sys.version)" *> $null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

$PythonCandidates = @()
if ($env:FIND_RPT_PYTHON) {
    $PythonCandidates += @{ Command = $env:FIND_RPT_PYTHON; Arguments = @() }
}
if (Get-Command py -ErrorAction SilentlyContinue) {
    $PythonCandidates += @{ Command = "py"; Arguments = @("-3.14") }
    $PythonCandidates += @{ Command = "py"; Arguments = @("-3") }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    $PythonCandidates += @{ Command = "python"; Arguments = @() }
}

$SelectedPython = $null
foreach ($Candidate in $PythonCandidates) {
    if (Test-PythonCommand -Command $Candidate.Command -Arguments $Candidate.Arguments) {
        $SelectedPython = $Candidate
        break
    }
}

if ($null -eq $SelectedPython) {
    throw "No compatible Python was found. Install Python or set FIND_RPT_PYTHON to a Python executable that can create venvs."
}

if (!(Test-Path -LiteralPath $VenvPython)) {
    & $SelectedPython.Command @($SelectedPython.Arguments + @("-m", "venv", $VenvPath))
}

& $VenvPython -m pip install --upgrade pip
& $VenvPython -m pip install -r $Requirements
& $VenvPython -c "import fitz, pymupdf4llm, spacy; spacy.load('en_core_web_sm'); print('find-rpt venv ok')"
