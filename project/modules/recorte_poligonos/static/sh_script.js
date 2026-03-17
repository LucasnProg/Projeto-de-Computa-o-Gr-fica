document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-poligonos');
    const ctx = canvas.getContext('2d');
    const clipXminInput = document.getElementById('clip-xmin');
    const clipYminInput = document.getElementById('clip-ymin');
    const clipXmaxInput = document.getElementById('clip-xmax');
    const clipYmaxInput = document.getElementById('clip-ymax');
    const polygonVerticesInput = document.getElementById('polygon-vertices');
    const clearVerticesBtn = document.getElementById('clear-vertices-btn');
    const clipPolygonBtn = document.getElementById('clip-polygon-btn');

    const clipInfo = document.getElementById('clip-info');
    const clearCanvasBtn = document.getElementById('clear-canvas-btn');

    let subjectPolygon = []; 

    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
    };

    const canvasToWorld = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: x - centerX, y: centerY - y };
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#d3d0d0ff';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.stroke();
    };

    const drawPolygon = (points, color = 'black', lineWidth = 1) => {
        if (points.length < 2) return;
        const p1_canvas = worldToCanvas(points[0].x, points[0].y);
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.beginPath();
        ctx.moveTo(p1_canvas.x, p1_canvas.y);
        for (let i = 1; i < points.length; i++) {
            const p_canvas = worldToCanvas(points[i].x, points[i].y);
            ctx.lineTo(p_canvas.x, p_canvas.y);
        }
        ctx.closePath();
        ctx.stroke();
    };

    const fillPolygon = (points, color = 'rgba(0, 0, 0, 0.5)') => {
        if (points.length < 3) return;
        const p1_canvas = worldToCanvas(points[0].x, points[0].y);
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(p1_canvas.x, p1_canvas.y);
        for (let i = 1; i < points.length; i++) {
            const p_canvas = worldToCanvas(points[i].x, points[i].y);
            ctx.lineTo(p_canvas.x, p_canvas.y);
        }
        ctx.closePath();
        ctx.fill();
    };

    const drawClippingWindow = (xmin, ymin, xmax, ymax) => {
        const p1 = worldToCanvas(xmin, ymax); 
        const p2 = worldToCanvas(xmax, ymin); 
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 1;
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
        ctx.setLineDash([]);
    };

    const redrawAll = () => {
        drawAxes();
        const window = {
            xmin: parseFloat(clipXminInput.value), ymin: parseFloat(clipYminInput.value),
            xmax: parseFloat(clipXmaxInput.value), ymax: parseFloat(clipYmaxInput.value)
        };
        drawClippingWindow(window.xmin, window.ymin, window.xmax, window.ymax);
        drawPolygon(subjectPolygon, 'gray', 1);
    };

    const updateVerticesText = () => {
        polygonVerticesInput.value = subjectPolygon.map(p => `(${p.x.toFixed(0)}, ${p.y.toFixed(0)})`).join('\n');
    };

    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const canvasX = event.clientX - rect.left;
        const canvasY = event.clientY - rect.top;
        const worldCoords = canvasToWorld(canvasX, canvasY);

        subjectPolygon.push(worldCoords);
        redrawAll();
        updateVerticesText();
    });

    clearVerticesBtn.addEventListener('click', () => {
        subjectPolygon = [];
        redrawAll();
        updateVerticesText();
    });

    clearCanvasBtn.addEventListener('click', () => {
        subjectPolygon = [];
        redrawAll();
        updateVerticesText();
        clipInfo.value = "Pronto.";
    });

    clipPolygonBtn.addEventListener('click', async () => {
        if (subjectPolygon.length < 3) {
            alert("Por favor, defina um polígono com pelo menos 3 vértices.");
            return;
        }

        redrawAll(); 

        const payload = {
            subjectPolygon: subjectPolygon,
            clipWindow: {
                xmin: parseFloat(clipXminInput.value), ymin: parseFloat(clipYminInput.value),
                xmax: parseFloat(clipXmaxInput.value), ymax: parseFloat(clipYmaxInput.value)
            }
        };

        clipInfo.value = "Calculando...";
        try {
            const response = await fetch('/api/sh/clip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.clippedPolygon && data.clippedPolygon.length > 0) {
                fillPolygon(data.clippedPolygon, 'rgba(0, 0, 0, 0.5)');
                drawPolygon(data.clippedPolygon, 'black', 1);
                clipInfo.value = `Recorte concluído.\n${data.clippedPolygon.length} vértices resultantes.`;
            } else {
                clipInfo.value = `Recorte concluído.\nO polígono está totalmente fora da janela.`;
            }

        } catch (err) {
            clipInfo.value = `Erro de rede: ${err.message}`;
        }
    });

    redrawAll();
});