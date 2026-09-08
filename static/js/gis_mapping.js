/**
 * InfraFlowX Geospatial GIS Mapping Engine
 * Integrates Leaflet.js with OpenStreetMap, Esri Satellite, CartoDB tiles,
 * custom SVG vector markers, GeoJSON layer parsing, and spatial bounding boxes.
 */

class InfraGISMap {
    constructor(containerId, options = {}) {
        this.containerId = containerId;
        this.defaultCenter = options.center || [28.6139, 77.2090]; // New Delhi default
        this.defaultZoom = options.zoom || 12;
        this.map = null;
        this.markerLayerGroup = null;
        this.polygonLayerGroup = null;
        this.init();
    }

    init() {
        const container = document.getElementById(this.containerId);
        if (!container) return;

        // Base Tile Layers
        const osmLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors | InfraFlowX GIS'
        });

        const darkLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            maxZoom: 19,
            attribution: '© CARTO | InfraFlowX Enterprise'
        });

        const satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
            maxZoom: 19,
            attribution: '© Esri Satellite'
        });

        this.map = L.map(this.containerId, {
            center: this.defaultCenter,
            zoom: this.defaultZoom,
            layers: [darkLayer]
        });

        const baseMaps = {
            "Dark Theme GIS": darkLayer,
            "OpenStreetMap": osmLayer,
            "Satellite Imagery": satelliteLayer
        };

        this.markerLayerGroup = L.layerGroup().addTo(this.map);
        this.polygonLayerGroup = L.layerGroup().addTo(this.map);

        const overlayMaps = {
            "Infrastructure Assets": this.markerLayerGroup,
            "Corridor Geometries": this.polygonLayerGroup
        };

        L.control.layers(baseMaps, overlayMaps, { position: 'topright' }).addTo(this.map);
        L.control.scale({ imperial: false, metric: true }).addTo(this.map);
    }

    addAssetMarker(lat, lng, assetData) {
        if (!this.map || !lat || !lng) return;

        const colorMap = {
            'ROAD': '#3b82f6',
            'BRIDGE': '#10b981',
            'BUILDING': '#8b5cf6',
            'FACILITY': '#f59e0b',
            'ACTIVE': '#22c55e',
            'UNDER_MAINTENANCE': '#f59e0b',
            'DAMAGED': '#ef4444'
        };

        const markerColor = colorMap[assetData.type] || '#3b82f6';
        const iconHtml = `<div style="
            background-color: ${markerColor};
            width: 24px;
            height: 24px;
            border-radius: 50%;
            border: 2px solid #ffffff;
            box-shadow: 0 0 8px rgba(0,0,0,0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff;
            font-size: 11px;
            font-weight: bold;
        ">★</div>`;

        const customIcon = L.divIcon({
            html: iconHtml,
            className: 'infra-custom-pin',
            iconSize: [24, 24],
            iconAnchor: [12, 12]
        });

        const marker = L.marker([lat, lng], { icon: customIcon });
        const popupContent = `
            <div style="min-width: 180px; font-family: sans-serif; font-size: 13px;">
                <h6 style="margin: 0 0 4px 0; font-weight: bold; color: #1e293b;">${assetData.name || 'Infrastructure Asset'}</h6>
                <div style="color: #64748b; font-size: 11px; margin-bottom: 6px;">ID: ${assetData.code || assetData.id}</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>Type:</span><strong>${assetData.type || 'N/A'}</strong>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>Condition Score:</span><strong>${assetData.condition_score || 85}/100</strong>
                </div>
                <div style="margin-top: 8px;">
                    <a href="${assetData.url || '#'}" class="btn btn-sm btn-primary text-white" style="font-size: 11px; padding: 2px 8px; text-decoration: none; border-radius: 4px; background: #2563eb; display: inline-block;">View Asset ➔</a>
                </div>
            </div>
        `;
        marker.bindPopup(popupContent);
        this.markerLayerGroup.addLayer(marker);
        return marker;
    }

    loadGeoJsonFeatures(geoJsonData) {
        if (!this.map || !geoJsonData) return;
        L.geoJSON(geoJsonData, {
            style: {
                color: "#3b82f6",
                weight: 4,
                opacity: 0.85
            },
            onEachFeature: (feature, layer) => {
                if (feature.properties && feature.properties.name) {
                    layer.bindPopup(`<strong>${feature.properties.name}</strong><br>Type: ${feature.properties.type || 'Corridor'}`);
                }
            }
        }).addTo(this.polygonLayerGroup);
    }

    fitAllMarkers() {
        if (!this.map) return;
        const bounds = L.latLngBounds([]);
        this.markerLayerGroup.eachLayer(layer => {
            if (layer.getLatLng) bounds.extend(layer.getLatLng());
        });
        if (bounds.isValid()) {
            this.map.fitBounds(bounds, { padding: [40, 40] });
        }
    }
}

window.InfraGISMap = InfraGISMap;
