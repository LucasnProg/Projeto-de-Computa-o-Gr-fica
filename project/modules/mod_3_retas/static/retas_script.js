document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-retas');
    const ctx = canvas.getContext('2d');
    const lineX1Input = document.getElementById('line-x1');
    const lineY1Input = document.getElementById('line-y1');
    const lineX2Input = document.getElementById('line-x2');
    const lineY2Input = document.getElementById('line-y2');
    const lineAlgoSelect = document.getElementById('line-algo');
    const drawLineBtn = document.getElementById('draw-line-btn');
    const linePointsInfo = document.getElementById('line-points-info');
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
        ctx.strokeStyle = '#d3d0d0ff';
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

    const updateLineInfoPanel = (data_points) => {
        let pointsText = '';
        if (data_points != null) {
            const points = data_points.points;
            const x_inc = data_points.x_inc;
            const y_inc = data_points.y_inc;
            

            pointsText = `x_inc = ${x_inc}\ny_inc = ${y_inc}\n\n` + points.map(p => `(${p.x}, ${p.y})`).join('\n');
        } else{
            pointsText = 'Nenhuma reta gerada.';
        }

        
        linePointsInfo.value = pointsText;
    };

    const clearAll = () => {
        drawAxes();
        updateLineInfoPanel(null);
    };

    drawLineBtn.addEventListener('click', async () => {
        const payload = { x1: lineX1Input.value, y1: lineY1Input.value, x2: lineX2Input.value, y2: lineY2Input.value, algo: lineAlgoSelect.value };
        const response = await fetch('/api/retas/draw_line', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data_points = await response.json();

        clearAll();
        drawPoints(data_points.points);
        updateLineInfoPanel(data_points);
    });

    clearBtn.addEventListener('click', clearAll);

    clearAll();
});