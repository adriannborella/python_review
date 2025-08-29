def track_time(func):
    """
    Decorador para medir el tiempo de ejecución de una función.
    """
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} - Tiempo de ejecución: {end_time - start_time:.6f} segundos")
        return result
    return wrapper

def analyze_list_operations():
    """
    Implementa y mide tiempo de diferentes operaciones
    """
    import time
    
    # TODO: Implementar y cronometrar:
    # 1. Crear lista de 100,000 elementos
    # 2. Acceder a elemento en posición 50,000
    # 3. Insertar elemento al inicio vs final
    # 4. Buscar elemento existente vs no existente
    # 5. Eliminar elemento del inicio vs final
    
    # Starter code:
    @track_time
    def create_large_list():
        return list(range(100000))
    
    @track_time
    def access_element(lst, index):
        return lst[index]
    
    @track_time
    def insert_element_start(lst, element):
        lst.insert(0, element)
        return lst
    
    @track_time
    def insert_element_end(lst, element):
        lst.append(element)
        return lst

    @track_time
    def search_element(lst, element):
        return element in lst

    @track_time
    def remove_element_start(lst):
        return lst.pop(0) if lst else None

    @track_time
    def remove_element_end(lst):
        return lst.pop() if lst else None

    large_list = create_large_list()
    accessed_element = access_element(large_list, 50000)
    inserted_list_start = insert_element_start(large_list, -1)
    inserted_list_end = insert_element_end(large_list, -1)
    found_existing = search_element(large_list, 50000)
    found_non_existing = search_element(large_list, 1000000)
    removed_start = remove_element_start(inserted_list_start)
    removed_end = remove_element_end(inserted_list_end)

def dictionary_vs_list_search():
    """
    Compara performance de búsqueda en dict vs list
    """
    # TODO: 
    # 1. Crear lista con 10,000 números aleatorios
    # 2. Crear diccionario con mismos números como keys
    # 3. Buscar 1,000 números aleatorios en ambas estructuras
    # 4. Comparar tiempos de ejecución
    
    import random
    
    @track_time
    def create_random_list(size=10000):
        return [random.randint(1, 100000) for _ in range(size)]

    random_list = create_random_list()
    random_dict = {num: num for num in random_list}

    for _ in range(1000):
        random_number = random.randint(1, 100000)
        
        # Búsqueda en lista
        @track_time
        def search_in_list(lst, number):
            return number in lst
        
        # Búsqueda en diccionario
        @track_time
        def search_in_dict(dct, number):
            return number in dct
        
        search_in_list(random_list, random_number)
        search_in_dict(random_dict, random_number)


if __name__ == "__main__":
    analyze_list_operations()
    print("Análisis de operaciones de lista completado.")

    dictionary_vs_list_search()
    print("Comparación de búsqueda en diccionario vs lista completada.")