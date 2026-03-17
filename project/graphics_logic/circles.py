
import math

def mid_Point_circle(xc, yc, r):

    def calc_simetry(xin , yin):
            points.extend([
            {"x": xc+yin, "y": yc+xin},
            {"x": xc+yin, "y": yc-xin},
            {"x": xc+xin, "y": yc-yin},
            {"x": xc-xin, "y": yc-yin},
            {"x": xc-yin, "y": yc-xin},
            {"x": xc-yin, "y": yc+xin},
            {"x": xc-xin, "y": yc+yin}
        ])

    points = []
    points_calculed = []

    xc, yc, r = int(xc), int(yc), int(r)
    x, y = 0, r
    d = 1 - r
    
    points_calculed.append({"x": xc+x, "y": yc+y, "d": d})
    points.append({"x": xc+x, "y": yc+y})
    calc_simetry(x,y)

    while y > x:
        x += 1
        if d < 0: 
            d += 2*x + 3
        else:
            y -= 1
            d += (2*(x-y)) + 5
        points_calculed.append({"x": xc+x, "y": yc+y , "d": d})
        points.append({"x": xc+x, "y": yc+y})
        calc_simetry(x,y)

    return points, points_calculed

def explicit_circle(xc, yc, r):
    points = []
    for x_off in range(-r, r+1):
        y_sq = r**2 - x_off**2
        if y_sq >= 0:
            y_off = math.sqrt(y_sq)
            points.append({"x": xc+x_off, "y": round(yc+y_off)})
            points.append({"x": xc+x_off, "y": round(yc-y_off)})
    return points

def parametric_circle(xc, yc, r, steps=360):
    points = []
    for i in range(steps+1):
        theta = math.radians(i * 360/steps)
        points.append({
            "x": round(xc + r*math.cos(theta)),
            "y": round(yc + r*math.sin(theta))
        })
    return points