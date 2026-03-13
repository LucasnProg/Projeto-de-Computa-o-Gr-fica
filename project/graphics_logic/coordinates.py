"""
MÓDULO: SISTEMAS DE COORDENADAS
-------------------------------
Responsável pela conversão entre diferentes espaços de representação.
Contém:
- Mapeamento Window-to-Viewport.
- Conversões entre Coordenadas de Mundo (WC), Normalizadas (NDC) e de Dispositivo (DC).

Utilizado por: Módulo 2 (Sistemas de Coordenadas) e Módulo 11 (Pipeline).
"""

def dc_to_ndc(x_dc, y_dc, w, h):
    return x_dc/float(w), y_dc/float(h)

def ndc_to_wc(ndc_x, ndc_y, x_max, x_min, y_max, y_min):
    wc_x = ndc_x * (x_max - x_min) + x_min
    wc_y = ndc_y * (y_max - y_min) + y_min
    return wc_x, wc_y

def wc_to_ndc(wc_x, wc_y, x_max, x_min, y_max, y_min):
    ndc_x = (wc_x - x_min) / (x_max - x_min)
    ndc_y = (wc_y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y