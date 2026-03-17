import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

target_vertices = []
target_edges = []
window_initialized = False

def update_live_object(vertices, edges):
    """Função chamada pelo Flask para atualizar os dados sem fechar a janela."""
    global target_vertices, target_edges
    target_vertices = vertices
    target_edges = edges

def draw_axes():
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0); glVertex3f(0,0,0); glVertex3f(1000,0,0) # X
    glColor3f(0.0, 1.0, 0.0); glVertex3f(0,0,0); glVertex3f(0,1000,0) # Y
    glColor3f(0.0, 0.0, 1.0); glVertex3f(0,0,0); glVertex3f(0,0,1000) # Z
    glEnd()

def open_3d_window():
    """Loop principal que roda em uma thread separada."""
    global window_initialized, target_vertices, target_edges
    
    try:
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Visualização 3D - OPENGL")
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() 
        gluPerspective(45, (display[0]/display[1]), 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        
        window_initialized = True 
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False 
            
            if not running:
                break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()
            gluLookAt(200, 200, 400, 40, 40, 40, 0, 1, 0)
            draw_axes()

            if target_vertices and target_edges:
                glBegin(GL_LINES)
                glColor3f(1.0, 1.0, 1.0)
                for edge in target_edges:
                    for v_idx_raw in edge:
                        try:
                            v_idx = int(v_idx_raw) 
                            
                            if v_idx < len(target_vertices):
                                v = target_vertices[v_idx]
                                glVertex3f(v['x'], v['y'], v['z'])
                        except (ValueError, TypeError):
                            continue
                glEnd()

            pygame.display.flip()
            pygame.time.wait(10)

    except Exception as e:
        print(f"Erro no OpenGL: {e}")
    finally:
        
        pygame.quit()
        window_initialized = False 