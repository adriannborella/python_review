from collections import defaultdict


class DataAnalyzer:
    """
    Analizador de datos que demuestra uso óptimo de estructuras
    """
    
    def __init__(self):
        self.data = []
        self.cache = {}  # Para memoization
        self.unique_values = set()
        
    def add_record(self, record):
        """
        Agrega registro y mantiene estructuras actualizadas
        record: tuple de (id, category, value, timestamp)
        """
        self.data.append(record)
        self.unique_values.add(record)

    def get_statistics(self):
        """
        Retorna estadísticas usando todas las estructuras eficientemente
        """
        # TODO: Usar dict para conteos, set para únicos, tuple para resultados
        category_count = defaultdict(int)
        for record in self.data:
            category_count[record[1]] += 1
        return {
            "total_records": len(self.data),
            "unique_values": len(self.unique_values),
            "category_count": dict(category_count)
        }

    def find_outliers(self, threshold=2.0):
        """
        Encuentra valores atípicos usando set operations
        """
        # TODO: Implementar detección de outliers
        if not self.data:
            return []
        values = [record[2] for record in self.data]
        mean = sum(values) / len(values)
        std_dev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5
        outliers = [x for x in values if abs(x - mean) > threshold * std_dev]
        return outliers

    
    def group_by_category(self):
        """
        Agrupa datos por categoría optimizando performance
        """
        # TODO: Usar defaultdict + sets
        grouped_data = defaultdict(set)
        for record in self.data:
            grouped_data[record[1]].add(record)
        return dict(grouped_data)

if __name__ == "__main__":
    # Test del analyzer
    analyzer = DataAnalyzer()
    # Test básico de funcionalidad
    analyzer.add_record((1, 'A', 10, '2023-10-01'))
    analyzer.add_record((2, 'B', 20, '2023-10-02'))
    analyzer.add_record((3, 'A', 15, '2023-10-03'))
    
    stats = analyzer.get_statistics()
    print(f"Estadísticas: {stats}")
    
    outliers = analyzer.find_outliers()
    print(f"Outliers: {outliers}")
    
    grouped = analyzer.group_by_category()
    print(f"Datos agrupados: {grouped}")