document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-poligonos-wa');
    const ctx = canvas.getContext('2d');

    // Controles
    const drawSubjectBtn = document.getElementById('draw-subject-btn');
    const drawClipBtn = document.getElementById('draw-clip-btn');
    const subjectVerticesInput = document.getElementById('subject-vertices');
    const clipVerticesInput = document.getElementById('clip-vertices');
    const clearVerticesBtn = document.getElementById('clear-vertices-btn');
    const clipPolygonBtn = document.getElementById('clip-polygon-btn');

    const clipInfo = document.getElementById('clip-info');
    const clearCanvasBtn = document.getElementById('clear-canvas-btn');

    // Estado da Aplicação
    let subjectPolygon = []; // Lista de pontos {x, y}
    let clipPolygon = [];    // Lista de pontos {x, y}
    let currentDrawMode = 'subject'; // 'subject' ou 'clip'

    // --- Funções de Desenho e Coordenadas ---
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

    const drawPolygon = (points, color = 'black', lineWidth = 1, lineDash = []) => {
        if (points.length < 2) return;
        const p1_canvas = worldToCanvas(points[0].x, points[0].y);
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.setLineDash(lineDash);
        ctx.beginPath();
        ctx.moveTo(p1_canvas.x, p1_canvas.y);
        for (let i = 1; i < points.length; i++) {
            const p_canvas = worldToCanvas(points[i].x, points[i].y);
            ctx.lineTo(p_canvas.x, p_canvas.y);
        }
        ctx.closePath();
        ctx.stroke();
        ctx.setLineDash([]);
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

    const redrawAll = () => {
        drawAxes();
        // Desenha o polígono "Subject" (cinza)
        drawPolygon(subjectPolygon, 'gray', 2);
        // Desenha o polígono "Clip" (azul tracejado)
        drawPolygon(clipPolygon, 'blue', 2, [5, 5]);
    };

    const updateVerticesText = () => {
        subjectVerticesInput.value = subjectPolygon.map(p => `(${p.x.toFixed(0)}, ${p.y.toFixed(0)})`).join('\n');
        clipVerticesInput.value = clipPolygon.map(p => `(${p.x.toFixed(0)}, ${p.y.toFixed(0)})`).join('\n');
    };

    // --- Event Listeners ---
    canvas.addEventListener('click', (event) => {
        const rect = canvas.getBoundingClientRect();
        const canvasX = event.clientX - rect.left;
        const canvasY = event.clientY - rect.top;
        const worldCoords = canvasToWorld(canvasX, canvasY);

        if (currentDrawMode === 'subject') {
            subjectPolygon.push(worldCoords);
        } else {
            clipPolygon.push(worldCoords);
        }
        redrawAll();
        updateVerticesText();
    });

    drawSubjectBtn.addEventListener('click', () => {
        currentDrawMode = 'subject';
        drawSubjectBtn.classList.add('active');
        drawClipBtn.classList.remove('active');
    });

    drawClipBtn.addEventListener('click', () => {
        currentDrawMode = 'clip';
        drawClipBtn.classList.add('active');
        drawSubjectBtn.classList.remove('active');
    });

    clearVerticesBtn.addEventListener('click', () => {
        if (currentDrawMode === 'subject') {
            subjectPolygon = [];
        } else {
            clipPolygon = [];
        }
        redrawAll();
        updateVerticesText();
    });

    clearCanvasBtn.addEventListener('click', () => {
        subjectPolygon = [];
        clipPolygon = [];
        redrawAll();
        updateVerticesText();
        clipInfo.value = "Pronto.";
    });

    clipPolygonBtn.addEventListener('click', async () => {
        if (subjectPolygon.length < 3 || clipPolygon.length < 3) {
            alert("Por favor, defina um polígono 'Subject' e um polígono 'Clip', ambos com pelo menos 3 vértices.");
            return;
        }

        redrawAll(); // Desenha a cena original

        const payload = {
            subjectPolygon: subjectPolygon,
            clipPolygon: clipPolygon
        };

        clipInfo.value = "Calculando (API chamará o stub de W-A)...";
        try {
            const response = await fetch('/api/wa/clip', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.error) {
                clipInfo.value = `Erro: ${data.error}`;
                return;
            }

            // AVISO: A API está chamando um STUB.
            // O código abaixo irá preencher o polígono original.
            if (data.clippedPolygons && data.clippedPolygons.length > 0) {
                clipInfo.value = `Recorte (STUB) concluído.\n` +
                    `${data.clippedPolygons.length} polígono(s) resultante(s).\n`;

                data.clippedPolygons.forEach(polygon => {
                    fillPolygon(polygon, 'rgba(0, 0, 0, 0.5)'); // Preto semi-transparente
                    drawPolygon(polygon, 'black', 2); // Contorno preto sólido
                });
            } else {
                clipInfo.value = `Recorte (STUB) concluído.\nNenhum polígono resultante.`;
            }

        } catch (err) {
            clipInfo.value = `Erro de rede: ${err.message}`;
        }
    });

    // Inicializa a tela
    redrawAll();
});