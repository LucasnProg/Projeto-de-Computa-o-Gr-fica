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
        const centerX = Math.floor(width / 2);
        const centerY = Math.floor(height / 2);

        const telaX = centerX + x;
        const telaY = centerY - y;

        ctx.fillStyle = '#000000';
        ctx.fillRect(telaX, telaY, 1, 1);
    };

    const drawPoints = (points) => {
        if (!points || points.length === 0) return;

        let index = 0;

        const drawNextPixel = () => {
            if (index < points.length) {
                const p = points[index];

                setPixel(p.x, p.y);

                index++;

                drawNextPixel();
            }
        };

        drawNextPixel();
    };

    const drawAxes = () => {
        const { width, height } = ctx.canvas;
        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#3c3c3c';
        ctx.lineWidth = 0.1;
        ctx.beginPath();
        ctx.moveTo(width / 2, 0); ctx.lineTo(width / 2, height);
        ctx.moveTo(0, height / 2); ctx.lineTo(width, height / 2);
        ctx.stroke();
    };

    const clearAll = () => {
        drawAxes();
        updateLineInfoPanel(null);
    };

    const updateLineInfoPanel = (data_points) => {
        let pointsText = '';
        if (data_points != null && lineAlgoSelect.value === 'DDA') {
            const points = data_points.points;
            pointsText = `x_inc = ${data_points.x_inc.toFixed(4)}\ny_inc = ${data_points.y_inc.toFixed(4)}\n\n` +
                points.map(p => `(${p.x}, ${p.y})`).join('\n');
        } else if (data_points != null && lineAlgoSelect.value !== 'DDA') {
            const points = data_points.points;
            pointsText = points.map(p =>
                `(${p.x}, ${p.y})     | D: ${p.d} | ${p.d < 0 ? 'Inc E' : 'Inc NE'}`
            ).join('\n');
        } else {
            pointsText = 'Nenhuma reta gerada.';
        }
        linePointsInfo.value = pointsText;
    };

    drawLineBtn.addEventListener('click', async () => {
        const payload = {
            x1: lineX1Input.value, y1: lineY1Input.value,
            x2: lineX2Input.value, y2: lineY2Input.value,
            algo: lineAlgoSelect.value
        };

        drawAxes();
        linePointsInfo.value = "Calculando...";

        try {
            const response = await fetch('/api/retas/draw_line', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data_points = await response.json();

            updateLineInfoPanel(data_points);

            drawPoints(data_points.points);

        } catch (error) {
            console.error("Erro ao calcular a reta:", error);
            linePointsInfo.value = "Erro de conexão com o servidor.";
        }
    });

    clearBtn.addEventListener('click', clearAll);

    clearAll();
});