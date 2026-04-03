import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import textwrap
import os
def wrap_text(text, width=42):
    """Envuelve el texto para que encaje en las cajas."""
    return '\n'.join(textwrap.wrap(text, width))

# 1. Configuración de la figura
fig, ax = plt.subplots(figsize=(16, 9))
fig.patch.set_facecolor('#f4f6f9')
ax.set_facecolor('#f4f6f9')
ax.axis('off')

# Ocultar marcos
for spine in ax.spines.values():
    spine.set_visible(False)

# Título Principal y cuadrado rojo decorativo
ax.add_patch(patches.Rectangle((0.02, 0.94), 0.008, 0.012, color='#e95a60', transform=ax.transAxes, clip_on=False))
ax.text(0.035, 0.946, "Figura E.2. ", color='#3f6f95', fontsize=16, fontweight='bold', ha='left', va='center', transform=ax.transAxes)
ax.text(0.125, 0.946, "Principales hallazgos de la Inteligencia Artificial (IA) y Chat GPT", color='#666666', fontsize=16, ha='left', va='center', transform=ax.transAxes)

# 2. Dibujar los fondos de colores (Izquierda: Rojo/Rosa, Derecha: Azul)
# Cajas principales con bordes redondeados
caja_ia = FancyBboxPatch((0.03, 0.15), 0.45, 0.73, boxstyle="round,pad=0.01,rounding_size=0.03", fc='#e85d62', ec="none")
ax.add_patch(caja_ia)

caja_gpt = FancyBboxPatch((0.52, 0.15), 0.45, 0.73, boxstyle="round,pad=0.01,rounding_size=0.03", fc='#326a8f', ec="none")
ax.add_patch(caja_gpt)

# 3. Textos y títulos de cada sección
ax.text(0.14, 0.35, "Inteligencia\nArtificial (IA)", color='white', fontsize=24, 
        fontweight='bold', ha='center', va='center', linespacing=1.2)
ax.text(0.63, 0.35, "ChatGPT", color='white', fontsize=24, 
        fontweight='bold', ha='center', va='center')

# Propiedades de las cajas de texto blancas
bbox_props = dict(boxstyle="round,pad=1.0,rounding_size=0.2", fc="white", ec="none", alpha=1.0)

# --- TEXTOS SECCIÓN IA (Izquierda) ---
textos_ia = [
    "> Es accesible, amigable y aporta muchos beneficios en diferentes áreas de la vida: laboral, escolar, salud y hogar, entre los más mencionados.",
    "> Los programas de IA pueden agruparse en tres categorías:\n1. Los programas en formato de texto que sirven como una introducción a la IA: ChatGPT, IA Bing y Bard de Google.\n2. Los programas que se utilizan para hacer presentaciones y para desarrollar contenido en redes sociales, como: Canva, Beautiful.ai, Synthesia y Pictory.\n3. Los programas dirigidos a segmentos muy concretos como publicidad, negocios, atención a clientes son: Jasper, Brand24 y ManyChat.",
    "> Las desventajas que pudieran tenerse son que no se dé la protección de privacidad de datos y los ciberdelitos. Es por ello que los entrevistados reconocen la importancia de la regulación del uso de estos programas."
]

# Modificando posiciones Y para que estén alineados en la parte derecha del recuadro rojo
y_pos_ia = [0.77, 0.52, 0.25]

for text, y in zip(textos_ia, y_pos_ia):
    ax.text(0.27, y, wrap_text(text, 44), color='#333333', fontsize=10.5,
            ha='left', va='center', bbox=bbox_props, linespacing=1.5)

# --- TEXTOS SECCIÓN CHATGPT (Derecha) ---
textos_chatgpt = [
    "> Es el programa de Inteligencia Artificial más conocido y utilizado.",
    "> Sorprende favorablemente la capacidad de resolver dudas, de redactar la información de forma concreta, organizada y sintetizada; además de que lo hace con una rapidez que agiliza el trabajo y tareas de cualquier persona que lo utilice.",
    "> Es atractivo para consultar temas laborales, escolares, de investigación, así como de cualquier cuestión de la vida cotidiana, desde recetas de cocina, consejos de salud, de entretenimiento, planes alimenticios, etcétera.",
    "> Entre las desventajas del ChatGPT se encuentran:\na) no brinda respuestas completas o da respuestas imprecisas y\nb) se tiene presente el hackeo, problemas con la privacidad de los datos personales y que puede ser utilizado para cometer fraudes y ciberdelitos."
]

# Posiciones de los textos para ChatGPT
y_pos_chatgpt = [0.80, 0.63, 0.43, 0.23]

for text, y in zip(textos_chatgpt, y_pos_chatgpt):
    ax.text(0.76, y, wrap_text(text, 44), color='#333333', fontsize=10.5,
            ha='left', va='center', bbox=bbox_props, linespacing=1.5)

# Notas al pie y fuente
ax.text(0.02, 0.07, "Fuente:", color='#333333', fontsize=10, fontweight='bold', ha='left', va='bottom', transform=ax.transAxes)
ax.text(0.06, 0.07, " IFT, con información del Estudio Cualitativo. Conocimiento y Percepción Sobre La Inteligencia Artificial (IA) y ChatGPT 2023. Para más información consultar:", color='#555555', fontsize=10, ha='left', va='bottom', transform=ax.transAxes)
ax.text(0.02, 0.04, "https://www.ift.org.mx/sites/default/files/contenidogeneral/usuarios-y-audiencias/estudiodeiaychatgpt2023_0.pdf.", color='#555555', fontsize=10, ha='left', va='bottom', transform=ax.transAxes)

ax.text(0.02, 0.01, "Nota:", color='#333333', fontsize=10, fontweight='bold', ha='left', va='bottom', transform=ax.transAxes)
ax.text(0.05, 0.01, " Reporte sobre el estudio cualitativo de un grupo de personas.", color='#555555', fontsize=10, ha='left', va='bottom', transform=ax.transAxes)

# 4. Ajustes finales
plt.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.02)

# Guardar la figura
output_dir = r"C:\Users\ivan-\Documents\GitHub\anuario\output"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "figura_e2.png")
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f"Gráfico guardado exitosamente en: {output_path}")