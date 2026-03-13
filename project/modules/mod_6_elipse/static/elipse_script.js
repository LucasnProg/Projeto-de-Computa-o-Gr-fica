document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-circ');
    const ctx = canvas.getContext('2d');
    const centerx = document.getElementById('center-x');
    const centerY = document.getElementById('center-y');
    const RxInput = document.getElementById('Rx');
    const RyInput = document.getElementById('Ry');
    const circleAlgoSelect = document.getElementById('circle-algo');
    const drawCircleBtn = document.getElementById('draw-circle-btn');
    const circPointsInfo = document.getElementById('circ-points-info');
    const clearBtn = document.getElementById('clear-btn');

    const setPixel = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        ctx.fillStyle = 'black';
        ctx.fillRect(centerX + x, centerY - y, 1, 1);
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#ccc';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.stroke();
    };

    const drawPoints = (points) => {
        if (!points || points.length === 0) return;
        points.forEach(p => {
            setPixel(p.x, p.y);
        });
    };

    const updateCircInfoPanel = (points) => {
        if (!points || !Array.isArray(points) || points.length === 0) {
            circPointsInfo.value = 'Nenhuma elipse gerada.';
            return;
        }
        // Limita a exibição para não travar o navegador se forem muitos pontos
        const limit = 2000; 
        let pointsText = points.slice(0, limit).map(p => `(${p.x}, ${p.y})`).join('  ');
        
        if (points.length > limit) {
            pointsText += `\n... e mais ${points.length - limit} pontos.`;
        }
        
        circPointsInfo.value = `Total: ${points.length} pontos.\n\n${pointsText}`;
    };

    const clearAll = () => {
        drawAxes();
        updateCircInfoPanel(null);
    };

    drawCircleBtn.addEventListener('click', async () => {
        const payload = { xc: centerx.value, yc: centerY.value, rx: RxInput.value, ry: RyInput.value};
        const response = await fetch('/api/elipse/draw_elipse', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
        const points = await response.json();
        clearAll();
        drawPoints(points);
        updateCircInfoPanel(points);
    });

    clearBtn.addEventListener('click', clearAll);

    clearAll();
});