const fs = require('fs');

const path = 'README_complemento.md';
const content = fs.readFileSync(path, 'utf8');

const parts = content.split(/\r?\n(?=## Figura )/);

if (parts.length < 2) {
    console.log("No parts found");
    process.exit(1);
}

const intro = parts[0];
const sections = [];

for (let i = 1; i < parts.length; i++) {
    const sec = parts[i];
    const match = sec.match(/^## Figura\s+([A-Z0-9\.]+)/);
    const id = match ? match[1] : '';
    const sortKey = id.replace(/\d+/g, d => d.padStart(5, '0'));
    sections.push({ text: sec, sortKey, id });
}

sections.sort((a, b) => a.sortKey.localeCompare(b.sortKey));

const newContent = intro + "\n" + sections.map(s => s.text).join("\n");
fs.writeFileSync(path, newContent, 'utf8');
console.log("Node sorting complete. Total parts: " + parts.length);
