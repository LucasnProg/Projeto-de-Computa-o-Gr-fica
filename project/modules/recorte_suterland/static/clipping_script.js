document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('canvas-clipping');
    const ctx = canvas.getContext('2d');
    const clipXminInput = document.getElementById('clip-xmin');
    const clipYminInput = document.getElementById('clip-ymin');
    const clipXmaxInput = document.getElementById('clip-xmax');
    const clipYmaxInput = document.getElementById('clip-ymax');
    const lineX1Input = document.getElementById('line-x1');
    const lineY1Input = document.getElementById('line-y1');
    const lineX2Input = document.getElementById('line-x2');
    const lineY2Input = document.getElementById('line-y2');
    const clipLineBtn = document.getElementById('clip-line-btn');
    const clipInfo = document.getElementById('clip-info');
    const clearBtn = document.getElementById('clear-btn');

    const toggleAnimationBtn = document.getElementById('toggle-animation-btn');
    let animationId = null; 
    let currentAngle = 0;   


    const INSIDE = 0; // 0b0000
    const LEFT = 1;   // 0b0001
    const RIGHT = 2;  // 0b0010
    const BOTTOM = 4; // 0b0100
    const TOP = 8;    // 0b1000


    function computeOutcode(x, y, xmin, ymin, xmax, ymax) {
        let code = INSIDE;
        if (x < xmin) code |= LEFT;
        else if (x > xmax) code |= RIGHT;
        if (y < ymin) code |= BOTTOM;
        else if (y > ymax) code |= TOP;
        return code;
    }

    function cohenSutherlandClip_JS(x1, y1, x2, y2, xmin, ymin, xmax, ymax) {
        let code1 = computeOutcode(x1, y1, xmin, ymin, xmax, ymax);
        let code2 = computeOutcode(x2, y2, xmin, ymin, xmax, ymax);
        let accepted = false;

        while (true) {
            if ((code1 | code2) === 0) {
                accepted = true;
                break;
            }
            else if ((code1 & code2) !== 0) {
                break;
            }
            else {
                let codeOut = code1 !== 0 ? code1 : code2;
                let x = 0, y = 0;

                if (codeOut & TOP) {
                    t = (ymax - y1) / (y2 - y1);
                    x = x1 + (t * (x2 - x1));
                    y = ymax;
                } else if (codeOut & BOTTOM) {
                    t = (ymin - y1) / (y2 - y1);
                    x = x1 + (t * (x2 - x1));
                    y = ymin;
                } else if (codeOut & RIGHT) {
                    t = (xmax - x1) / (x2 - x1);
                    y = y1 + (t * (y2 - y1));
                    x = xmax;
                } else if (codeOut & LEFT) {
                    t = (xmin - x1) / (x2 - x1);
                    y = y1 + (t * (y2 - y1));
                    x = xmin;
                }

                if (codeOut === code1) {
                    x1 = x; y1 = y;
                    code1 = computeOutcode(x1, y1, xmin, ymin, xmax, ymax);
                } else {
                    x2 = x; y2 = y;
                    code2 = computeOutcode(x2, y2, xmin, ymin, xmax, ymax);
                }
            }
        }

        if (accepted) {
            return { accepted: true, x1: x1, y1: y1, x2: x2, y2: y2 };
        } else {
            return { accepted: false };
        }
    }

    const worldToCanvas = (x, y) => {
        const { width, height } = ctx.canvas;
        const centerX = width / 2;
        const centerY = height / 2;
        return { x: centerX + x, y: centerY - y };
    };

    const drawLine = (x1, y1, x2, y2, color = 'black', lineWidth = 0.1) => {
        const p1 = worldToCanvas(x1, y1);
        const p2 = worldToCanvas(x2, y2);
        ctx.strokeStyle = color;
        ctx.lineWidth = lineWidth;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
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

    const drawClippingWindow = (xmin, ymin, xmax, ymax) => {
        const p1 = worldToCanvas(xmin, ymax);
        const p2 = worldToCanvas(xmax, ymin);

        ctx.strokeStyle = 'blue';
        ctx.lineWidth = 1;
        ctx.strokeRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
    };

    const clearAll = () => {
        stopAnimation();
        drawAxes();
        drawClippingWindow(
            parseFloat(clipXminInput.value), parseFloat(clipYminInput.value),
            parseFloat(clipXmaxInput.value), parseFloat(clipYmaxInput.value)
        );
        clipInfo.value = 'Pronto para recortar.';
    };


    function animationLoop() {
        if (currentAngle <= -Math.PI * 2) {
            currentAngle = 0;
        }
        drawAxes();
        const xmin = parseFloat(clipXminInput.value);
        const ymin = parseFloat(clipYminInput.value);
        const xmax = parseFloat(clipXmaxInput.value);
        const ymax = parseFloat(clipYmaxInput.value);
        drawClippingWindow(xmin, ymin, xmax, ymax);


        const L = 500; 

        currentAngle -= 0.01; 

        const rad = currentAngle;
        const cosA = Math.cos(rad);
        const sinA = Math.sin(rad);

        const x1_orig = -L * cosA;
        const y1_orig = -L * sinA;
        const x2_orig = L * cosA;
        const y2_orig = L * sinA;

        drawLine(x1_orig, y1_orig, x2_orig, y2_orig, '#cccccc', 1);

        const clipped = cohenSutherlandClip_JS(x1_orig, y1_orig, x2_orig, y2_orig, xmin, ymin, xmax, ymax);

        if (clipped.accepted) {
            drawLine(clipped.x1, clipped.y1, clipped.x2, clipped.y2, 'black', 1);
            clipInfo.value = `RECORTANDO...\nÂngulo: ${(currentAngle * 180 / Math.PI).toFixed(0)}°\n` +
                `P1': (${clipped.x1.toFixed(1)}, ${clipped.y1.toFixed(1)})\n` +
                `P2': (${clipped.x2.toFixed(1)}, ${clipped.y2.toFixed(1)})`;
        } else {
            clipInfo.value = `REJEITADA\nÂngulo: ${(currentAngle * 180 / Math.PI).toFixed(0)}°`;
        }

        animationId = requestAnimationFrame(animationLoop);
    }

    function toggleAnimation() {
        if (animationId) {
            stopAnimation();
        } else {
            currentAngle = 0;
            toggleAnimationBtn.textContent = "Parar Animação";
            clipLineBtn.disabled = true;
            animationLoop();
        }
    }

    function stopAnimation() {
        if (animationId) {
            cancelAnimationFrame(animationId);
            animationId = null;
        }
        toggleAnimationBtn.textContent = "Aplicar Item 2";
        clipLineBtn.disabled = false;
    }

    clipLineBtn.addEventListener('click', async () => {
        clearAll();

        const line = {
            x1: parseFloat(lineX1Input.value), y1: parseFloat(lineY1Input.value),
            x2: parseFloat(lineX2Input.value), y2: parseFloat(lineY2Input.value)
        };
        const window = {
            xmin: parseFloat(clipXminInput.value), ymin: parseFloat(clipYminInput.value),
            xmax: parseFloat(clipXmaxInput.value), ymax: parseFloat(clipYmaxInput.value)
        };

        drawLine(line.x1, line.y1, line.x2, line.y2, '#cccccc', 1);

        const payload = { ...line, ...window };
        const response = await fetch('/api/clipping/clip_line', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();

        if (data.accepted) {
            const { x1, y1, x2, y2 } = data.coords;
            drawLine(x1, y1, x2, y2, 'black', 1);
            clipInfo.value = `LINHA ACEITA.\nNovos pontos:\n(${x1}, ${y1}) para (${x2}, ${y2})`;
        } else {
            clipInfo.value = 'LINHA REJEITADA :\nCompletamente fora da janela.';
        }
    });

    toggleAnimationBtn.addEventListener('click', toggleAnimation);

    clearBtn.addEventListener('click', clearAll);

    clearAll();
});