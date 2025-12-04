document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-pipeline');
    const ctx = canvas.getContext('2d');

    // Inputs da Janela
    const worldXmin = document.getElementById('world-xmin');
    const worldYmin = document.getElementById('world-ymin');
    const worldXmax = document.getElementById('world-xmax');
    const worldYmax = document.getElementById('world-ymax');

    // Inputs da Viewport
    const viewXmin = document.getElementById('view-xmin');
    const viewYmin = document.getElementById('view-ymin');
    const viewXmax = document.getElementById('view-xmax');
    const viewYmax = document.getElementById('view-ymax');

    // Controles do Polígono
    const polygonVerticesInput = document.getElementById('polygon-vertices');
    const clearVerticesBtn = document.getElementById('clear-vertices-btn');
    const processBtn = document.getElementById('process-pipeline-btn');

    const clipInfo = document.getElementById('pipeline-info');
    const clearCanvasBtn = document.getElementById('clear-canvas-btn');

    // Estado da Aplicação
    let subjectPolygon = []; // Lista de pontos {x, y} em COORDENADAS DO MUNDO

    // --- Funções de Desenho ---
    // NOVO: Coordenadas do Canvas (0,0 no topo-esquerdo)
    // E Coordenadas do Mundo (0,0 no centro)

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
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2); // Eixo X
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height); // Eixo Y
        ctx.stroke();
    };

    // Desenha um polígono em COORDENADAS DO MUNDO
    const drawWorldPolygon = (points, color = 'gray', lineWidth = 2) => {
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

    // Desenha um polígono em COORDENADAS DE VIEWPORT (TELA)
    const drawViewportPolygon = (points, color = 'black', fill = 'rgba(0,0,0,0.5)') => {
        if (points.length < 3) return;
        // Pontos já estão em coordenadas de tela (canvas)
        ctx.fillStyle = fill;
        ctx.strokeStyle = color;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
            ctx.lineTo(points[i].x, points[i].y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    };

    // Desenha a Janela do Mundo (em Coordenadas do Mundo)
    const drawClippingWindow = (xmin, ymin, xmax, ymax) => {
        const p1 = worldToCanvas(xmin, ymax);
        const p2 = worldToCanvas(xmax, ymin);
        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
        ctx.setLineDash([]);
    };

    // Desenha a Viewport (em Coordenadas de Tela)
    const drawViewport = (vx_min, vy_min, vx_max, vy_max) => {
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 3]);
        // Coordenadas do canvas (Y é invertido)
        ctx.strokeRect(vx_min, vy_min, vx_max - vx_min, vy_max - vy_min);
        ctx.setLineDash([]);
    };

    const redrawAll = () => {
        drawAxes();
        // Desenha Janela
        drawClippingWindow(
            parseFloat(worldXmin.value), parseFloat(worldYmin.value),
            parseFloat(worldXmax.value), parseFloat(worldYmax.value)
        );
        // Desenha Viewport
        drawViewport(
            parseFloat(viewXmin.value), parseFloat(viewYmin.value),
            parseFloat(viewXmax.value), parseFloat(viewYmax.value)
        );
        // Desenha Polígono "Subject" original
        drawWorldPolygon(subjectPolygon, 'gray', 2);
    };

    const updateVerticesText = () => {
        polygonVerticesInput.value = subjectPolygon.map(p => `(${p.x.toFixed(0)}, ${p.y.toFixed(0)})`).join('\n');
    };

    // --- Event Listeners ---
    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const canvasX = event.clientX - rect.left;
        const canvasY = event.clientY - rect.top;
        // Adiciona pontos em Coordenadas do Mundo
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

    processBtn.addEventListener('click', async () => {
        if (subjectPolygon.length < 3) {
            alert("Por favor, defina um polígono com pelo menos 3 vértices.");
            return;
        }

        redrawAll(); // Desenha a cena original

        const payload = {
            subjectPolygon: subjectPolygon,
            window: {
                xmin: parseFloat(worldXmin.value), ymin: parseFloat(worldYmin.value),
                xmax: parseFloat(worldXmax.value), ymax: parseFloat(worldYmax.value)
            },
            viewport: {
                vx_min: parseFloat(viewXmin.value), vy_min: parseFloat(viewYmin.value),
                vx_max: parseFloat(viewXmax.value), vy_max: parseFloat(viewYmax.value)
            }
        };

        clipInfo.value = "Processando pipeline...";
        try {
            const response = await fetch('/api/2d/pipeline_process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.viewport_polygon && data.viewport_polygon.length > 0) {
                // Desenha o polígono FINAL, já mapeado para a viewport
                drawViewportPolygon(data.viewport_polygon, 'black', 'rgba(0,0,0,0.5)');
                const pointsStr = data.viewport_polygon
                    .map(p => `(${p.x.toFixed(1)}, ${p.y.toFixed(1)})`)
                    .join('\n');

                clipInfo.value = `Pipeline concluído.\n${data.viewport_polygon.length} vértices na tela:\n\n${pointsStr}`;
            } else {
                clipInfo.value = `Pipeline concluído.\nO polígono está totalmente fora da Janela do Mundo.`;
            }

        } catch (err) {
            clipInfo.value = `Erro de rede: ${err.message}`;
        }
    });

    // Inicializa a tela
    redrawAll();
});