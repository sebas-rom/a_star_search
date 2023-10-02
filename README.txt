Modo de Uso 

Por el momento solo se soporta completamente puzzles de 3x3, implementacion 4x4 en progreso. (Cuello de botella, generar base de datos para 4x4)

Creación de la base de datos:
    Utilizar createSolvableDBnxn.py para generar una base de datos vacia, que contienene todas las combinaciones con solucion.
    Utilizar populateDB (multiThread preferiblemente) para llenar la base de datos con las soluciones de la heuristica.
    Se generará el archivo puzzle_database_nxn.db, el programa utilza actualmente el archivo nxnDataBase.db para la resolución de problemas.

