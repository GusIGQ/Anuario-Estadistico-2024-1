$path = "C:\Users\ivan-\Documents\GitHub\anuario\README_complemento.md"
$text = Get-Content -Path $path -Raw -Encoding UTF8

# Split using positive lookahead so we don't consume the "## Figura " text.
$sections = [System.Text.RegularExpressions.Regex]::Split($text, "(?m)^(?=## Figura )")

$intro = $sections[0]
$figSections = @()

for ($i = 1; $i -lt $sections.Count; $i++) {
    $sec = $sections[$i]
    # Extract the figure ID, e.g., "A.1", "B.10", "E.9", "F.1.1"
    if ($sec -match "^## Figura\s+([A-Z0-9\.]+)") {
        $id = $matches[1]
        
        # We need a sort key that zero-pads all numbers in the ID.
        # e.g., "A.1" -> "A.00001"
        # e.g., "F.1.10" -> "F.00001.00010"
        $sortKey = [regex]::Replace($id, "\d+", {param($m) $m.Value.PadLeft(5, '0')})
        
        $figSections += [PSCustomObject]@{
            Text = $sec
            SortKey = $sortKey
            OriginalId = $id
        }
    } else {
        # Edge case: maybe "## Figura" but without an ID? Just keep it at top or parse normally
        $figSections += [PSCustomObject]@{
            Text = $sec
            SortKey = "ZZZ"
            OriginalId = ""
        }
    }
}

# Sort the sections
$sortedSections = $figSections | Sort-Object SortKey

$newText = $intro + ($sortedSections.Text -join "")

# Write back
$newText | Set-Content -Path $path -NoNewline -Encoding UTF8
Write-Host "Ordenamiento completado. Revisa las figuras."
