# push_portfolio.ps1
# Automatisches Skript zum Hochladen des Portfolios auf GitHub

$repo_url = "https://github.com/Dtunder/portfolio.git"
$branch = "main"

Write-Host "Starte Git Push Prozess für das Portfolio..." -ForegroundColor Cyan

# Überprüfen, ob Git initialisiert ist
if (!(Test-Path ".git")) {
    Write-Host "Initialisiere neues Git Repository..." -ForegroundColor Yellow
    git init
    git remote add origin $repo_url
}

# Dateien hinzufügen
Write-Host "Füge Änderungen hinzu..." -ForegroundColor Yellow
git add .

# Status prüfen, ob es überhaupt Änderungen gibt
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "Keine neuen Änderungen gefunden. Alles ist auf dem neuesten Stand." -ForegroundColor Green
    exit
}

# Commit erstellen
$commit_msg = "Portfolio Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host "Erstelle Commit: '$commit_msg'" -ForegroundColor Yellow
git commit -m $commit_msg

# Branch sicherstellen
git branch -M $branch

# Push
Write-Host "Lade auf GitHub hoch..." -ForegroundColor Yellow
git push -u origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host "Erfolgreich hochgeladen! Die Live-Seite wird in wenigen Minuten aktualisiert." -ForegroundColor Green
    Write-Host "Dein Portfolio wird unter https://dtunder.github.io/portfolio/ erreichbar sein." -ForegroundColor Cyan
} else {
    Write-Host "Es gab einen Fehler beim Hochladen. Bitte überprüfe deine Git-Einstellungen und Credentials." -ForegroundColor Red
}

Read-Host "Drücke Enter zum Beenden"
