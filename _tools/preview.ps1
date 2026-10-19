param(
    [switch]$Build,
    [ValidateRange(1, 65535)][int]$Port = 4000
)

$ErrorActionPreference = 'Stop'
$previewRoot = Split-Path $PSScriptRoot -Parent
$savedPath = $env:Path
$savedGemPath = $env:GEM_PATH
$savedBundleGemfile = $env:BUNDLE_GEMFILE
$savedBundleIgnoreConfig = $env:BUNDLE_IGNORE_CONFIG

Push-Location $previewRoot
try {
    # Pick up a newly installed Ruby without requiring a restart of the terminal.
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'User') + ';' + $env:Path
    $previewRuby = Get-Command ruby -ErrorAction Stop
    $rubyGemPaths = & $previewRuby.Source -e 'puts Gem.path'
    if ($LASTEXITCODE -ne 0) { throw 'Ruby could not start.' }
    $rubyGemVersion = & $previewRuby.Source -rrbconfig -e 'puts RbConfig::CONFIG[%q[ruby_version]]'
    if ($LASTEXITCODE -ne 0) { throw 'Could not determine the Ruby gem directory.' }

    # Include gems already installed for this project and the libraries shipped with Ruby.
    $projectGemPath = Join-Path $previewRoot ".bundle/gems/ruby/$rubyGemVersion"
    $env:GEM_PATH = (@($projectGemPath) + @($rubyGemPaths)) -join ';'
    $env:BUNDLE_GEMFILE = Join-Path $PSScriptRoot 'Gemfile.preview'
    $env:BUNDLE_IGNORE_CONFIG = '1'

    & $previewRuby.Source -S bundle check
    if ($LASTEXITCODE -ne 0) {
        & $previewRuby.Source -S bundle install
        if ($LASTEXITCODE -ne 0) { throw 'Could not install the local preview dependencies.' }
    }

    if ($Build) {
        & $previewRuby.Source -rbundler/setup -e "load Gem.bin_path('jekyll', 'jekyll')" -- build
    } else {
        Write-Host "Album preview: http://127.0.0.1:$Port/photos.html (Ctrl+C to stop)"
        & $previewRuby.Source -rbundler/setup -e "load Gem.bin_path('jekyll', 'jekyll')" -- serve --host 127.0.0.1 --port $Port --force_polling
    }
    if ($LASTEXITCODE -ne 0) { throw "Jekyll exited with code $LASTEXITCODE." }
} finally {
    $env:Path = $savedPath
    $env:GEM_PATH = $savedGemPath
    $env:BUNDLE_GEMFILE = $savedBundleGemfile
    $env:BUNDLE_IGNORE_CONFIG = $savedBundleIgnoreConfig
    Pop-Location
}
