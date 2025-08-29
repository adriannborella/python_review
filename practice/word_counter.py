from utils import track_time
from collections import Counter


@track_time
def word_frequency_counter(text):
    """
    Cuenta frecuencia de palabras en texto
    Optimiza para performance usando Counter
    """
    words = [
        word.lower().strip(".,!?\"'()[]{};:")
        for word in text.split()
        if word.strip(".,!?\"'()[]{};:")
    ]
    return dict(Counter(words))

@track_time
def word_count(text):
    """
    Cuenta frecuencia de palabras en texto
    Optimiza para performance
    """
    result = {}
    for word in text.split():
        word = word.lower().strip(".,!?\"'()[]{};:")
        if word:
            result[word] = result.get(word, 0) + 1
    return result
    


# Test data
sample_text = """
Este libro es para todos aquellos que quieran mejorar su cuerpo con ejercicios naturales,
independientemente de su forma física actual.
 Es útil para principiantes, personas que llevan una vida sedentaria y que nunca han realizado
actividad física. Los ejercicios que propongo tienen versiones básicas que cualquier persona
normal puede realizar, con una estrategia clara para ir mejorando poco a poco.
 Es útil para aquellos que llevan años yendo al gimnasio, haciendo siempre los mismos
ejercicios enlatados en las mismas máquinas, como robots; o corriendo constantemente en las
cintas, como hámsters en sus ruedas; con pocos resultados que mostrar después de tanto
esfuerzo. Entrenar con máquinas es antinatural y siempre te dará peores resultados que ejercitarte
con ejercicios corporales bien diseñados.
 Es útil para los obsesionados con levantar peso, acostumbrados a pasar horas al día en el
gimnasio con largas sesiones de sentadillas, press de banca, decenas de ejercicios de aislamiento
y un largo etc. Seguramente estas personas tengan grandes músculos y sean la envidia de
muchos de sus humildes compañeros de gimnasio; sin embargo, este régimen antinatural de
ejercicio conlleva en muchos casos problemas continuos de tendones inflamados (en muchos
casos tendinitis crónica), roturas fibrilares, contracturas musculares, desgarros, pinzamientos…
Acércate a estos ‘super-hombres’ en los vestuarios del gimnasio y sentirás el olor a mentol, verás
los analgésicos que deben tomar para las inflamaciones, y escucharás las conversaciones sobre
sus últimas infiltraciones de corticoides o inyecciones de ácido hialurónico (y no precisamente para
las arrugas)… Para los que no estáis en este mundo os sonarán raras estas cosas, pero creedme
que esta forma de auto-castigo no es el camino a un cuerpo saludable. A todos los que estáis en
este grupo, os recomiendo alternar estas sesiones de pesas con ejercicios corporales, que
fortalecerán vuestros cuerpos desde dentro y ayudarán a la reparación natural de las lesiones más
típicas. Además, los ejercicios corporales permiten desarrollar músculos con fuerza y utilidad real,
y no sólo músculos “de playa”.
El programa de ejercicios que propongo te llevará entre dos y tres horas a la semana, como mucho. Sí,
has leído bien, 2-3 horas a la semana, no al día. Esto es suficiente para tener un cuerpo bonito y saludable,
o como yo digo, un cuerpo funcional, tal como explico un poco más adelante
"""

if __name__ == "__main__":
    # Prueba word_frequency_counter
    freq = word_frequency_counter(sample_text)
    optimized_count = word_count(sample_text)
    # print("Número total de palabras:", optimized_count)
    # print("Frecuencia de palabras:", freq)
