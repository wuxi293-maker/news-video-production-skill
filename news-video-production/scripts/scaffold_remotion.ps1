$ErrorActionPreference = "Stop"

$SkillDir = Split-Path -Parent $PSScriptRoot
$Target = if ($args.Count -gt 0) { $args[0] } else { ".\remotion-news-video" }

if (Test-Path $Target) {
  throw "Target already exists: $Target. Move it away or pass another path."
}

New-Item -ItemType Directory -Path $Target | Out-Null
Copy-Item -Path (Join-Path $SkillDir "assets\remotion-starter\*") -Destination $Target -Recurse

Set-Location $Target
if ($env:SKIP_INSTALL -ne "1") { npm install }
if (Test-Path "scripts\ensure-bgm.mjs") { node scripts\ensure-bgm.mjs }
if ($env:SKIP_BROWSER -ne "1") { npx remotion browser ensure }

Write-Host "Starter created at: $Target"
Write-Host "Next:"
Write-Host "  cd `"$Target`""
Write-Host "  npm run render"
