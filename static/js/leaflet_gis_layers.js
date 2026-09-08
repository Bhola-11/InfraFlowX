/**
 * InfraFlowX - Advanced Leaflet GIS Spatial Engine
 * Handles GeoJSON corridor overlay, live pin clustering, inspection heatmaps, and spatial buffer zones.
 */

window.InfraGISEngine = {
    initMap: function(containerId, centerLat = 37.7749, centerLon = -122.4194, zoom = 12) {
        const map = L.map(containerId, {
            zoomControl: true,
            attributionControl: true
        }).setView([centerLat, centerLon], zoom);

        // Dark Matter Base Tile Layer
        L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
            maxZoom: 19
        }).addTo(map);

        return map;
    },

    addAssetMarkers: function(map, assetList) {
        const markerGroup = L.layerGroup().addTo(map);

        assetList.forEach(asset => {
            if (!asset.latitude || !asset.longitude) return;

            const marker = L.circleMarker([asset.latitude, asset.longitude], {
                radius: 7,
                fillColor: this.getConditionColor(asset.condition_score),
                color: '#ffffff',
                weight: 1.5,
                opacity: 1,
                fillOpacity: 0.85
            });

            const popupContent = `
                <div style="font-family: Arial, sans-serif; font-size: 13px; line-height: 1.4;">
                    <strong style="color: #0f172a;">${asset.name}</strong><br/>
                    <span style="color: #64748b;">Code: ${asset.code}</span><br/>
                    <span style="color: #334155;">Type: <strong>${asset.asset_type || 'General Asset'}</strong></span><br/>
                    <span style="color: #334155;">Condition: <strong>${asset.condition_score || 100}/100</strong></span><br/>
                    <div style="margin-top: 8px;">
                        <a href="/assets/${asset.id}/" class="btn btn-sm btn-primary" style="font-size: 11px; padding: 2px 8px; color: #fff; text-decoration: none; border-radius: 4px; background: #2563eb;">View Details</a>
                    </div>
                </div>
            `;

            marker.bindPopup(popupContent);
            markerGroup.addLayer(marker);
        });

        return markerGroup;
    },

    getConditionColor: function(score) {
        if (!score && score !== 0) return '#94a3b8';
        if (score >= 85) return '#10b981'; // Green
        if (score >= 70) return '#3b82f6'; // Blue
        if (score >= 55) return '#f59e0b'; // Amber
        if (score >= 40) return '#f97316'; // Orange
        return '#ef4444'; // Red
    }
};
