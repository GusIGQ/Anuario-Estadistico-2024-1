import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[1]))
from _plot_data_logger import enable_plot_data_logging
enable_plot_data_logging()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Configurar figura
fig, ax = plt.subplots(figsize=(16, 8), dpi=200)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Colores extraídos aproximadamente de la imagen
color_izq = '#E75759'  # Rojo/Coral
color_der = '#30688E'  # Azul oscuro
color_texto = 'white'

# Textos del panel izquierdo
titulo_izq = "Medidas preventivas\npara evitar ser\nvíctima de violencia\ndigital"
textos_izq = [
    "Cuidar el tipo de información que comparten, así como evitar compartir información personal privada, de ellas mismas y de sus familiares.",
    "Tener contacto solamente con personas conocidas. No aceptar a desconocidos (as).",
    "No entrar a sitios, ni links desconocidos, aunque parezcan muy atractivos.",
    "Utilizar los filtros de seguridad que las mismas plataformas digitales proporcionan para restringir a quienes se les comparte la información."
]

# Textos del panel derecho
titulo_der = "Medidas de\nprotección una\nvez que han sido\nvíctimas de\nviolencia digital"
textos_der = [
    "En casos menos delicados hacer caso omiso a comentarios negativos, provocaciones, ataques.",
    "Platicar su caso con familiares y amistades de mucha confianza para recibir su apoyo y consejo.",
    "En casos mas graves, incluso acudir a la Policía Cibernética.",
    "Ayuda psicológica."
]

# Dibujar Panel Izquierdo (Rojo)
panel_izq = patches.FancyBboxPatch((0.02, 0.05), 0.45, 0.90, boxstyle="round,pad=0.03,rounding_size=0.02", color=color_izq)
ax.add_patch(panel_izq)
ax.text(0.05, 0.20, titulo_izq, color=color_texto, fontsize=18, fontweight='bold', va='center', ha='left')

# Dibujar Panel Derecho (Azul)
panel_der = patches.FancyBboxPatch((0.51, 0.05), 0.47, 0.90, boxstyle="round,pad=0.03,rounding_size=0.02", color=color_der)
ax.add_patch(panel_der)
ax.text(0.54, 0.20, titulo_der, color=color_texto, fontsize=18, fontweight='bold', va='center', ha='left')

# Función para dibujar las cajas de texto blancas
def dibujar_cajas(textos, x_base, width):
    y_pos = [0.85, 0.65, 0.45, 0.20] # Posiciones verticales distribuidas
    for i, texto in enumerate(textos):
        texto_wrap = textwrap.fill(texto, width=40)
        
        # Calcular altura aproximada según cantidad de líneas
        num_lineas = len(texto_wrap.split('\n'))
        height = 0.04 + (num_lineas * 0.025)
        
        # Caja blanca
        y_box = y_pos[i] - height/2
        caja = patches.FancyBboxPatch((x_base, y_box), width, height, 
                                      boxstyle="round,pad=0.04,rounding_size=0.03", 
                                      color='white', ec='none')
        ax.add_patch(caja)
        
        # Texto dentro de la caja
        ax.text(x_base + 0.02, y_pos[i], texto_wrap, color='#333333', 
                fontsize=11, va='center', ha='left')

# Dibujar las cajas en los paneles
# Panel Izquierdo: Cajas a la derecha del panel
dibujar_cajas(textos_izq, x_base=0.23, width=0.21)

# Panel Derecho: Cajas a la derecha del panel
dibujar_cajas(textos_der, x_base=0.74, width=0.21)

# Guardar y mostrar
plt.savefig(PROJECT_ROOT / "output" / "figura_f14.png", dpi=300)
plt.show()