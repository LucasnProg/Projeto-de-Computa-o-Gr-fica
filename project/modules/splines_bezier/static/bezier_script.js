document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-bezier');
    const ctx = canvas.getContext('2d');

    const coordInputs = [
        { x: document.getElementById('p0-x'), y: document.getElementById('p0-y') },
        { x: document.getElementById('p1-x'), y: document.getElementById('p1-y') },
        { x: document.getElementById('p2-x'), y: document.getElementById('p2-y') },
        { x: document.getElementById('p3-x'), y: document.getElementById('p3-y') }
    ];
    
    const clearBtn = document.getElementById('clear-btn');
    const infoBox = document.getElementById('bezier-info');
    const updateFromInputsBtn = document.getElementById('update-from-inputs-btn');

    let controlPoints = []; 

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

    const drawControlPoint = (p, label) => {
        const c = worldToCanvas(p.x, p.y);
        ctx.fillStyle = 'red';
        ctx.beginPath();
        ctx.arc(c.x, c.y, 5, 0, 2 * Math.PI);
        ctx.fill();

        ctx.fillStyle = 'black';
        ctx.font = '12px Arial';
        ctx.fillText(label, c.x + 8, c.y + 3);
    };

    const drawControlPolygon = () => {
        if (controlPoints.length < 2) return;

        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 1;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();

        let p_canvas = worldToCanvas(controlPoints[0].x, controlPoints[0].y);
        ctx.moveTo(p_canvas.x, p_canvas.y);

        for (let i = 1; i < controlPoints.length; i++) {
            p_canvas = worldToCanvas(controlPoints[i].x, controlPoints[i].y);
            ctx.lineTo(p_canvas.x, p_canvas.y);
        }
        ctx.stroke();
        ctx.setLineDash([]);
    };

    const drawCurve = (points) => {
        if (points.length < 2) return;

        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 2;
        ctx.beginPath();

        const p_canvas = worldToCanvas(points[0].x, points[0].y);
        ctx.moveTo(p_canvas.x, p_canvas.y);

        for (let i = 1; i < points.length; i++) {
            const p = worldToCanvas(points[i].x, points[i].y);
            ctx.lineTo(p.x, p.y);
        }
        ctx.stroke();
    };

    const redrawAll = () => {
        drawAxes();
        drawControlPolygon();
        controlPoints.forEach((p, i) => {
            drawControlPoint(p, `P${i}`);
        });
    };

    const updateInfo = () => {
        const nextPoint = controlPoints.length;
        if (nextPoint < 4) {
            infoBox.value = `Defina 4 pontos de controle.\n\n` +
                `Faltando P${nextPoint}...\n\n` +
                `Clique no canvas OU preencha os campos e clique em "Gerar Curva".`;
        } else {
            infoBox.value = "Curva de Bézier Cúbica calculada com sucesso!\n\n" +
                "P0: Ponto de início\n" +
                "P3: Ponto final\n" +
                "P1 e P2: Definem as tangentes da curva.";
        }
    };

    const calculateAndDrawCurve = async () => {
        if (controlPoints.length !== 4) return;

        const payload = {
            p0: controlPoints[0],
            p1: controlPoints[1],
            p2: controlPoints[2],
            p3: controlPoints[3]
        };

        try {
            const response = await fetch('/api/bezier/calculate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await response.json();

            if (data.curve_points) {
                drawCurve(data.curve_points);
            } else if (data.error) {
                infoBox.value = `Erro: ${data.error}`;
            }
        } catch (err) {
            infoBox.value = `Erro ao calcular curva: ${err.message}`;
        }
    };

    canvas.addEventListener('click', (event) => {
        if (controlPoints.length >= 4) {
            infoBox.value = "Já existem 4 pontos. Limpe para começar de novo.";
            return;
        }

        const rect = canvas.getBoundingClientRect();
        const canvasX = event.clientX - rect.left;
        const canvasY = event.clientY - rect.top;
        const worldCoords = canvasToWorld(canvasX, canvasY);

        const index = controlPoints.length;
        controlPoints.push(worldCoords);

        coordInputs[index].x.value = worldCoords.x.toFixed(0);
        coordInputs[index].y.value = worldCoords.y.toFixed(0);

        redrawAll();
        updateInfo();

        if (controlPoints.length === 4) {
            calculateAndDrawCurve();
        }
    });

    updateFromInputsBtn.addEventListener('click', () => {
        let newPoints = [];
        try {
            for (let i = 0; i < 4; i++) {
                const xVal = coordInputs[i].x.value;
                const yVal = coordInputs[i].y.value;
                
                if (xVal === "" || yVal === "") {
                    throw new Error(`As coordenadas do P${i} devem estar preenchidas.`);
                }
                
                newPoints.push({
                    x: parseFloat(xVal),
                    y: parseFloat(yVal)
                });
            }

            controlPoints = newPoints;
            redrawAll();
            calculateAndDrawCurve();
            updateInfo();

        } catch (e) {
            infoBox.value = `Atenção: ${e.message}`;
        }
    });

    clearBtn.addEventListener('click', () => {
        controlPoints = [];
        coordInputs.forEach(input => {
            input.x.value = '';
            input.y.value = '';
        });
        drawAxes();
        updateInfo();
    });

    drawAxes();
    updateInfo();
});