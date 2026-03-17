document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-circ');
    const ctx = canvas.getContext('2d');
    const circleXcInput = document.getElementById('circle-xc');
    const circleYcInput = document.getElementById('circle-yc');
    const circleRInput = document.getElementById('circle-r');
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
        ctx.lineWidth = 0.1;
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
        if (!points || points.length === 0) {
            circPointsInfo.value = 'Nenhuma circunferência gerada.';
            return;
        }
        let pointsText;
        if (circleAlgoSelect.value === "PontoMedio"){
            pointsText = points.map(p => `[(${p.x}, ${p.y})  | D: ${p.d} | ${p.d < 0 ? 'Inc E' : 'Inc SE'})]\n`)
        } else{
            pointsText = points.map(p => `(${p.x}, ${p.y})`).join('\n');
        }
        
        circPointsInfo.value = pointsText;
    };

    const clearAll = () => {
        drawAxes();
        updateCircInfoPanel(null);
    };

    drawCircleBtn.addEventListener('click', async () => {
        const payload = { xc: circleXcInput.value, yc: circleYcInput.value, r: circleRInput.value, algo: circleAlgoSelect.value };
        const response = await fetch('/api/circ/draw_circle', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
        if (circleAlgoSelect.value === "PontoMedio"){
            const { points, calculed } = await response.json();
            clearAll();
            drawPoints(points);
            updateCircInfoPanel(calculed);
        } else{
            const points = await response.json();
            clearAll();
            drawPoints(points);
            updateCircInfoPanel(points);
        }
        
    });

    clearBtn.addEventListener('click', clearAll);

    clearAll();
});