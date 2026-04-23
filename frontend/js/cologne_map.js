let map;
let networkData = null;
let pathLayer = null;
let markers = {};
let selectedStart = null;
let selectedEnd = null;

async function initCologneMap() {
    map = L.map('map').setView([50.9375, 6.9603], 13); // Center of Cologne

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20
    }).addTo(map);

    try {
        await refreshNetwork();
        await loadLineControls();
    } catch (e) {
        console.error("Failed to load network:", e);
    }
}

async function refreshNetwork() {
    networkData = await TransitAPI.getNetwork();
    renderNetwork();
}

function renderNetwork() {
    // Clear existing markers and layers
    Object.values(markers).forEach(m => m.remove());
    markers = {};
    if (pathLayer) pathLayer.remove();

    // Draw edges
    networkData.edges.forEach(edge => {
        const u = networkData.nodes.find(n => n.id === edge.source);
        const v = networkData.nodes.find(n => n.id === edge.target);
        
        if (u && v) {
            const color = edge.active ? getLineColor(edge.line) : '#333';
            const weight = edge.active ? 3 : 1;
            const opacity = edge.active ? 0.7 : 0.2;

            L.polyline([[u.lat, u.lon], [v.lat, v.lon]], {
                color: color,
                weight: weight,
                opacity: opacity
            }).addTo(map);
        }
    });

    // Add node markers (only for important stations or on zoom)
    networkData.nodes.forEach(node => {
        const marker = L.circleMarker([node.lat, node.lon], {
            radius: 4,
            fillColor: '#fff',
            color: '#000',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);

        marker.bindPopup(`<b>${node.name}</b><br>ID: ${node.id}`);
        
        marker.on('click', () => {
            selectNode(node);
        });

        markers[node.id] = marker;
    });
}

function selectNode(node) {
    if (!selectedStart) {
        selectedStart = node;
        document.getElementById('startInfo').innerText = node.name;
        markers[node.id].setStyle({ fillColor: '#2ecc71', radius: 8 });
    } else if (!selectedEnd) {
        selectedEnd = node;
        document.getElementById('endInfo').innerText = node.name;
        markers[node.id].setStyle({ fillColor: '#e74c3c', radius: 8 });
        findPath();
    } else {
        // Reset
        resetSelection();
        selectedStart = node;
        document.getElementById('startInfo').innerText = node.name;
        markers[node.id].setStyle({ fillColor: '#2ecc71', radius: 8 });
    }
}

function resetSelection() {
    if (selectedStart) markers[selectedStart.id].setStyle({ fillColor: '#fff', radius: 4 });
    if (selectedEnd) markers[selectedEnd.id].setStyle({ fillColor: '#fff', radius: 4 });
    selectedStart = null;
    selectedEnd = null;
    document.getElementById('startInfo').innerText = '—';
    document.getElementById('endInfo').innerText = '—';
    if (pathLayer) pathLayer.remove();
}

async function findPath() {
    if (!selectedStart || !selectedEnd) return;

    const result = await TransitAPI.findPath(selectedStart.id, selectedEnd.id);
    
    if (result.success) {
        const pathCoords = [];
        result.details.forEach(step => {
            const u = networkData.nodes.find(n => n.id === step.from);
            pathCoords.push([u.lat, u.lon]);
        });
        const lastNode = networkData.nodes.find(n => n.id === result.path[result.path.length-1]);
        pathCoords.push([lastNode.lat, lastNode.lon]);

        if (pathLayer) pathLayer.remove();
        pathLayer = L.polyline(pathCoords, {
            color: '#f1c40f',
            weight: 6,
            opacity: 0.9,
            dashArray: '10, 10'
        }).addTo(map);

        map.fitBounds(pathLayer.getBounds());
        
        document.getElementById('distInfo').innerText = (result.total_distance / 1000).toFixed(2) + ' km';
    } else {
        alert("No path found: " + result.error);
    }
}

async function loadLineControls() {
    const linesData = await TransitAPI.getLines();
    const container = document.getElementById('line-controls');
    container.innerHTML = '';

    linesData.all_lines.forEach(line => {
        const div = document.createElement('div');
        div.className = 'line-item';
        const isDisabled = linesData.disabled_lines.includes(line);
        
        div.innerHTML = `
            <span>${line}</span>
            <label class="switch">
                <input type="checkbox" ${isDisabled ? '' : 'checked'} onchange="toggleLine('${line}', this.checked)">
                <span class="slider round"></span>
            </label>
        `;
        container.appendChild(div);
    });
}

async function toggleLine(lineName, active) {
    await TransitAPI.toggleLine(lineName, !active);
    await refreshNetwork();
    if (selectedStart && selectedEnd) findPath();
}

function getLineColor(line) {
    if (!line) return '#999';
    // Cologne KVB Colors (simplified)
    if (line.startsWith('1')) return '#ed1c24';
    if (line.startsWith('3') || line.startsWith('4')) return '#f68b1e';
    if (line.startsWith('5')) return '#92278f';
    if (line.startsWith('7')) return '#f58220';
    if (line.startsWith('9')) return '#f9ad81';
    if (line.startsWith('12')) return '#00a651';
    if (line.startsWith('15')) return '#00a651';
    if (line.startsWith('16')) return '#0072bc';
    if (line.startsWith('18')) return '#0072bc';
    if (line.startsWith('S')) return '#00964b'; // S-Bahn
    return '#' + Math.floor(Math.random()*16777215).toString(16);
}

// initCologneMap is called from index.html with loading overlay handling
