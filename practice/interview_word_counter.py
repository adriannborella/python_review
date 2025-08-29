from collections import Counter
from utils import sample_text

def interview_question(text: str):
    """
    Dada una lista de palabras, encuentra:
    1. Palabras únicas (sin duplicados)
    2. Palabras que aparecen más de una vez
    3. Conteo de cada palabra
    4. Las 3 palabras más frecuentes
    
    Optimiza para mejor complejidad temporal posible.
    """
    # Normalizar palabras: convertir a minúsculas y quitar puntuación
    words_list = text.lower().split()
    words_list = [word.strip(".,!?\"'()[]{};:") for word in words_list if word.strip(".,!?\"'()[]{};:")]
    # Usar Counter para contar palabras
    counter = Counter(words_list)
    unique_words = []
    duplicate_words = []
    for word, count in counter.items():
        if count == 1:
            unique_words.append(word)
        else:
            duplicate_words.append(word)

    most_common = counter.most_common(3)

    return {
        "unique_words": unique_words,
        "duplicate_words": duplicate_words,
        "word_count": dict(counter),
        "most_common": most_common
    }

def interview_question_optimized(text: str):
    """
    Versión optimizada usando Set, Dict y Tuplas apropiadamente
    """
    # Normalizar y limpiar
    words_list = text.lower().split()
    words_list = [word.strip(".,!?\"'()[]{};:") for word in words_list if word.strip(".,!?\"'()[]{};:")]
    
    # SET: para encontrar palabras únicas rápidamente
    unique_words_set = set(words_list)
    
    # DICT: para conteos (Counter es un dict especializado)
    word_count = Counter(words_list)
    
    # Separar únicas vs duplicadas usando set comprehensions
    unique_words = {word for word, count in word_count.items() if count == 1}
    duplicate_words = {word for word, count in word_count.items() if count > 1}
    
    # TUPLA: para retornar datos inmutables estructurados
    most_common = word_count.most_common(3)  # Ya retorna lista de tuplas
    
    return {
        "unique_words": list(unique_words),      # SET → list
        "duplicate_words": list(duplicate_words), # SET → list  
        "word_count": dict(word_count),          # DICT
        "most_common": most_common               # Lista de TUPLAS
    }


if __name__ == "__main__":
    result = interview_question(sample_text)
    print(result)  # Debe imprimir las palabras únicas, duplicadas, conteo y las 3 más frecuentes