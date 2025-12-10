class CalculadoraISO:
    """13 Fórmulas ISO exactas"""
    
    @staticmethod
    def ICP(realizadas, planificadas):
        """Índice de Cumplimiento de Planificación"""
        if planificadas == 0:
            return 0
        return (realizadas / planificadas) * 100
    
    @staticmethod
    def NC(no_conformidades, auditados):
        """Índice de No Conformidades"""
        if auditados == 0:
            return 0
        return no_conformidades / auditados
    
    @staticmethod
    def FR(fallos, tiempo):
        """Tasa de Fallos"""
        if tiempo == 0:
            return 0
        return fallos / tiempo
    
    @staticmethod
    def MTBF(tiempo_total, fallos):
        """Tiempo Medio Entre Fallos"""
        if fallos == 0:
            return 0
        return tiempo_total / fallos
    
    @staticmethod
    def TPR(suma_tiempos, solicitudes):
        """Tiempo Promedio de Respuesta"""
        if solicitudes == 0:
            return 0
        return suma_tiempos / solicitudes
    
    @staticmethod
    def IVC(criticas, totales):
        """Índice de Vulnerabilidades Críticas"""
        if totales == 0:
            return 0
        return (criticas / totales) * 100
    
    @staticmethod
    def CC(E, N, P):
        """Complejidad Ciclomática"""
        return E - N + 2 * P
    
    @staticmethod
    def TS(correctas, totales):
        """Tasa de Sobrevivencia"""
        if totales == 0:
            return 0
        return (correctas / totales) * 100
    
    @staticmethod
    def IC(soportados, objetivo):
        """Índice de Compatibilidad"""
        if objetivo == 0:
            return 0
        return (soportados / objetivo) * 100
    
    @staticmethod
    def Ef(tareas_completadas, tiempo):
        """Eficiencia"""
        if tiempo == 0:
            return 0
        return tareas_completadas / tiempo
    
    @staticmethod
    def E(correctas, totales):
        """Exactitud"""
        if totales == 0:
            return 0
        return (correctas / totales) * 100
    
    @staticmethod
    def Uso(recurso_utilizado, total):
        """Tasa de Uso de Recursos"""
        if total == 0:
            return 0
        return (recurso_utilizado / total) * 100
    
    @staticmethod
    def IM(plataformas_soportadas, objetivo):
        """Índice de Interoperabilidad Multiplataforma"""
        if objetivo == 0:
            return 0
        return (plataformas_soportadas / objetivo) * 100


FORMULAS_DEFINICION = [
    {'codigo': 'ICP', 'nombre': 'Índice de Cumplimiento de Planificación', 'descripcion': 'Porcentaje de tareas realizadas respecto a planificadas', 'formula': '(Realizadas/Planificadas)*100', 'parametros': ['Realizadas', 'Planificadas'], 'unidad': '%'},
    {'codigo': 'NC', 'nombre': 'Índice de No Conformidades', 'descripcion': 'Ratio de no conformidades encontradas en auditorías', 'formula': 'NoConformidades/Auditados', 'parametros': ['NoConformidades', 'Auditados'], 'unidad': 'ratio'},
    {'codigo': 'FR', 'nombre': 'Tasa de Fallos', 'descripcion': 'Número de fallos por unidad de tiempo', 'formula': 'Fallos/Tiempo', 'parametros': ['Fallos', 'Tiempo'], 'unidad': 'fallos/unidad'},
    {'codigo': 'MTBF', 'nombre': 'Tiempo Medio Entre Fallos', 'descripcion': 'Tiempo promedio entre ocurrencias de fallos', 'formula': 'TiempoTotal/Fallos', 'parametros': ['TiempoTotal', 'Fallos'], 'unidad': 'horas'},
    {'codigo': 'TPR', 'nombre': 'Tiempo Promedio de Respuesta', 'descripcion': 'Tiempo medio de respuesta ante solicitudes', 'formula': 'ΣTiempos/Solicitudes', 'parametros': ['SumaTiempos', 'Solicitudes'], 'unidad': 'ms'},
    {'codigo': 'IVC', 'nombre': 'Índice de Vulnerabilidades Críticas', 'descripcion': 'Porcentaje de vulnerabilidades críticas encontradas', 'formula': '(Críticas/Totales)*100', 'parametros': ['Criticas', 'Totales'], 'unidad': '%'},
    {'codigo': 'CC', 'nombre': 'Complejidad Ciclomática', 'descripcion': 'Métrica de complejidad del código', 'formula': 'E-N+2P', 'parametros': ['E', 'N', 'P'], 'unidad': 'valor'},
    {'codigo': 'TS', 'nombre': 'Tasa de Sobrevivencia', 'descripcion': 'Porcentaje de tests que pasan correctamente', 'formula': '(Correctas/Totales)*100', 'parametros': ['Correctas', 'Totales'], 'unidad': '%'},
    {'codigo': 'IC', 'nombre': 'Índice de Compatibilidad', 'descripcion': 'Porcentaje de plataformas/sistemas soportados', 'formula': '(Soportados/Objetivo)*100', 'parametros': ['Soportados', 'Objetivo'], 'unidad': '%'},
    {'codigo': 'Ef', 'nombre': 'Eficiencia', 'descripcion': 'Tareas completadas por unidad de tiempo', 'formula': 'TareasCompletadas/Tiempo', 'parametros': ['TareasCompletadas', 'Tiempo'], 'unidad': 'tareas/hora'},
    {'codigo': 'E', 'nombre': 'Exactitud', 'descripcion': 'Porcentaje de resultados correctos', 'formula': '(Correctas/Totales)*100', 'parametros': ['Correctas', 'Totales'], 'unidad': '%'},
    {'codigo': 'Uso', 'nombre': 'Tasa de Uso de Recursos', 'descripcion': 'Porcentaje de recursos utilizados', 'formula': '(RecursoUtilizado/Total)*100', 'parametros': ['RecursoUtilizado', 'Total'], 'unidad': '%'},
    {'codigo': 'IM', 'nombre': 'Índice de Interoperabilidad Multiplataforma', 'descripcion': 'Cantidad de plataformas soportadas respecto a objetivo', 'formula': '(PlataformasSoportadas/Objetivo)*100', 'parametros': ['PlataformasSoportadas', 'Objetivo'], 'unidad': '%'}
]
