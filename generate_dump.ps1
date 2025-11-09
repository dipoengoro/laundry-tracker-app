# --- generate_dump.ps1 ---
#
# Skrip ini akan mencari file kode yang relevan dan menggabungkannya
# menjadi satu file output tunggal.
# ----------------------------------------------------

# --- KONFIGURASI ---
$outputFile = "proyek_dump_final.txt"
$searchPaths = @("backend", "frontend", ".")

# Ekstensi file yang akan di-include
$includeExtensions = @(
    ".py", ".vue", ".js", ".css", "html", ".json", ".yml", ".ini", 
    ".md", ".mako", ".yaml", ".toml" 
)

# Nama file spesifik yang akan di-include
$includeFileNames = @(
    "Dockerfile", "alembic.ini", "requirements.txt", ".gitignore"
)

# Direktori yang akan di-exclude secara penuh (gunakan forward slashes)
$excludeDirs = @(
    "node_modules", "venv", "venv-docs", "__pycache__", 
    ".git", ".idea", ".vscode", "dist", "site", "backend_static",
    "backend/alembic/versions", "docs"
)

# Nama file spesifik yang akan di-exclude
$excludeFileNames = @(
    "package-lock.json", "proyek_dump_untuk_notebooklm.md", "dump_backend.txt", "dump_frontend.txt", "proyek_dump_final.txt"
)

# Pola file yang akan di-exclude (wildcard)
$excludePatterns = @(
    "*.un~",
    "*.pyc",
    "*.log"
)
# ---------------------

$rootPath = (Get-Location).Path

# --- Buat Header untuk File Output Tunggal ---
$timestamp = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss', [System.Globalization.CultureInfo]::InvariantCulture)

$header = "Kumpulan Kode: Proyek Laundry Tracker App`nDibuat pada: $timestamp"
Set-Content -Path $outputFile -Value $header

Write-Host "Mulai mencari file..."

# Ambil semua file, lalu filter
$allFiles = Get-ChildItem -Path $searchPaths -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
    $file = $_
    
    # Normalisasi path untuk perbandingan
    $normalizedPath = $file.FullName.Replace($rootPath, "").Replace("\", "/")

    # Cek direktori yang di-exclude
    $inExcludedDir = $false
    foreach ($dir in $excludeDirs) {
        if ($normalizedPath.StartsWith("/$dir")) {
            $inExcludedDir = $true
            break
        }
    }
    if ($inExcludedDir) { return $false }

    # Cek nama file & pola yang di-exclude
    if ($excludeFileNames -contains $file.Name) { return $false }
    foreach ($pattern in $excludePatterns) {
        if ($file.Name -like $pattern) { return $false }
    }

    # Cek file yang di-include
    ($includeExtensions -contains $file.Extension) -or ($includeFileNames -contains $file.Name)
}

$totalFiles = $allFiles.Count
Write-Host "Menemukan $totalFiles file kode. Mulai menulis ke $outputFile..."

# Loop setiap file dan tulis ke file output tunggal
foreach ($file in $allFiles) {
    $relativePath = $file.FullName.Replace($rootPath, "").Replace("\", "/")
    
    $content = Get-Content -Path $file.FullName -Raw -ErrorAction SilentlyContinue
    $cleanedContent = $content
    if (-not [string]::IsNullOrEmpty($content)) {
        $cleanedContent = $content.Replace("`r`n", "`n")
    }

    $template = @'

==================================================
File: {0}
==================================================

{1}
'@
    $fileBlock = $template -f $relativePath, $cleanedContent

    Add-Content -Path $outputFile -Value $fileBlock
    Write-Host "Menambahkan: $relativePath"
}

Write-Host "`n✅ Selesai!"
Write-Host "Output: $outputFile"