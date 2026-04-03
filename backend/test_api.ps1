Set-Location -Path "$PSScriptRoot"

# Config
$baseUri = "http://localhost:8001"

# Tiny 1x1 PNG
$b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAn8B9mzy83QAAAAASUVORK5CYII="
[IO.File]::WriteAllBytes("$PSScriptRoot/test.png", [Convert]::FromBase64String($b64))

Write-Host "Health check:" -ForegroundColor Cyan
$health = Invoke-RestMethod -Method Get -Uri "$baseUri/health"
$health | ConvertTo-Json -Depth 3

Write-Host "---" -ForegroundColor DarkGray

Write-Host "OpenAPI paths:" -ForegroundColor Cyan
try {
    $openapi = Invoke-RestMethod -Method Get -Uri "$baseUri/openapi.json"
    $paths = $openapi.paths | Get-Member -MemberType NoteProperty | Select-Object -ExpandProperty Name
    $paths
} catch {
    Write-Host "Failed to fetch openapi" -ForegroundColor Red
}

Write-Host "---" -ForegroundColor DarkGray

try {
    Add-Type -AssemblyName System.Net.Http
    $client = New-Object System.Net.Http.HttpClient
    $content = New-Object System.Net.Http.MultipartFormDataContent
    $fileStream = [System.IO.File]::OpenRead("$PSScriptRoot/test.png")
    $fileContent = New-Object System.Net.Http.StreamContent($fileStream)
    $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("image/png")
    $content.Add($fileContent, "file", "test.png")

    $response = $client.PostAsync("$baseUri/analyze-document", $content).Result
    $body = $response.Content.ReadAsStringAsync().Result

    Write-Host "Analyze status: $($response.StatusCode)" -ForegroundColor Cyan
    $body
} catch {
    Write-Host "Analyze error:" -ForegroundColor Red
    $_ | Format-List * -Force
}
