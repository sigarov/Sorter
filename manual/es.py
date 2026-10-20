"""Manual en español — traducción del original alemán manual/de.py."""

ES = {
    "title": "Manual de usuario",
    "sections": [
        {
            "id": "intro",
            "title": "1. Qué hace el programa",
            "text": (
                "El clasificador de medios ordena imágenes y vídeos en una estructura de "
                "carpetas fija y después ayuda a limpiar los nombres duplicados.\n\n"
                "Eliges una o dos fuentes (carpetas o unidades completas) y una carpeta de "
                "destino. El programa lee todas las imágenes y vídeos, determina la fecha de "
                "captura y copia cada archivo en la carpeta correspondiente de año, mes y día.\n\n"
                "Conviene saber:\n"
                "• Las fuentes solo se leen, nunca se modifican.\n"
                '• No se elimina nada. Los duplicados van a la carpeta "Duplicates".\n'
                "• Los nombres de las carpetas de destino son siempre ingleses (Pictures, "
                "Videos, _No_Date). Así la estructura permanece estable al cambiar de idioma.\n"
                "• La interfaz está disponible en siete idiomas. Este manual aparece en el "
                "idioma elegido en cuanto exista una traducción; hasta entonces, en alemán."
            ),
        },
        {
            "id": "start",
            "title": "2. Primeros pasos",
            "text": (
                "1. Elige el idioma arriba a la izquierda: la pantalla cambia de inmediato.\n"
                "2. Elige la fuente 1: carpeta o unidad. Si quieres, añade la fuente 2.\n"
                "3. Elige el destino: allí se clasificará todo.\n"
                "4. Si quieres, activa la simulación para probar antes.\n"
                '5. Haz clic en "▶  Iniciar" (o pulsa F5).\n\n'
                "Durante la ejecución, dos barras de progreso muestran el estado: primero la "
                'indexación del destino y luego la clasificación. Con "■  Detener" (o Esc) '
                "cancelas el proceso; los archivos ya copiados se conservan.\n\n"
                'La pestaña "Limpiar" solo se desbloquea después de una clasificación real '
                "en el destino elegido."
            ),
        },
        {
            "id": "sort",
            "title": "3. Clasificación y estructura de carpetas",
            "text": (
                "La clasificación tiene dos fases:\n"
                "1. Se indexa la carpeta de destino. Para ello se registran el tamaño, la "
                "fecha de modificación y la suma de comprobación (hash) de todos los archivos "
                "existentes.\n"
                "2. Cada archivo de origen se comprueba y se copia a la carpeta de destino.\n\n"
                "La fecha se determina en este orden:\n"
                "• Fecha de captura EXIF de la imagen (requiere Pillow)\n"
                "• Metadatos del vídeo (requiere ffprobe en el PATH)\n"
                "• Fecha del nombre del archivo, p. ej. 2020-05-17, 20200517 o "
                "20200517_143025\n\n"
                "La fecha del sistema de archivos no se usa a propósito: los archivos sin una "
                "marca de tiempo real deben ir a la carpeta _No_Date en lugar de clasificarse "
                "mal por su fecha de copia.\n\n"
                "Estructura en el destino (ejemplo):\n"
                "• Pictures/2020/05/17/vacaciones.jpg\n"
                "• Videos/2020/05/17/vacaciones.mp4\n"
                "• _No_Date/Pictures/desconocido.jpg\n\n"
                "Si un archivo de destino ya existe y el contenido es el mismo, el archivo de "
                "origen se omite. Si el nombre es igual pero el contenido difiere, se crean "
                "_1, _2, etc. Antes de copiar, el programa comprueba el espacio libre y, "
                "después de copiar, compara el tamaño del archivo."
            ),
        },
        {
            "id": "names",
            "title": "4. Nombres de archivo",
            "text": (
                "Seis variantes para nombres de archivo nuevos (ejemplo: vacaciones.jpg del "
                "17/05/2020, 14:30:25):\n\n"
                "• Original: vacaciones.jpg\n"
                "• Fecha_Nombre: 20200517_vacaciones.jpg\n"
                "• Fecha_Hora_Nombre: 20200517_143025_vacaciones.jpg\n"
                "• Año-Mes-Día_Nombre: 2020-05-17_vacaciones.jpg\n"
                "• Número: 00001.jpg\n"
                "• Fecha_Número: 20200517_0001.jpg\n\n"
                'Sin fecha, "Número" solo asigna el número correlativo; en las demás '
                "variantes se conserva el nombre original. La extensión siempre se escribe en "
                "minúsculas. Si coinciden los nombres, el programa añade _1, _2, ..."
            ),
        },
        {
            "id": "structure",
            "title": "5. Estructura: separada o conjunta",
            "text": (
                "Separada (predeterminada): las imágenes y los vídeos están en árboles "
                "distintos.\n"
                "  Pictures/2020/05/17/... y Videos/2020/05/17/...\n"
                "Conjunta: ambos van a la misma carpeta de año/mes/día.\n"
                "  2020/05/17/...\n\n"
                "Granularidad:\n"
                "• Año: 2020/\n"
                "• Mes: 2020/05/\n"
                "• Día: 2020/05/17/\n\n"
                'Los archivos sin fecha van a _No_Date; con "Separada", además, bajo '
                "Pictures o Videos. Allí, _liste.txt enumera todos los archivos afectados."
            ),
        },
        {
            "id": "filters",
            "title": "6. Filtrar carpetas",
            "text": (
                "El campo de filtro limita qué subcarpetas de la fuente se recorren.\n"
                "• Separa varios términos con comas: Fotos, Pictures, DCIM\n"
                "• Solo cuentan los nombres de carpeta, no las extensiones de archivo.\n"
                "• Las mayúsculas y minúsculas no importan.\n"
                "• Una coincidencia se aplica también a todas las subcarpetas.\n"
                "• Campo vacío = toda la fuente.\n\n"
                'Ejemplo: en D:\\Backup hay "Fotos", "Documentos" y "Vídeos". Con el '
                'filtro "Fotos, Vídeos" solo se leen esas dos carpetas.\n\n'
                'La pestaña "Limpiar" no tiene filtro: allí siempre se revisa toda la carpeta '
                "de destino."
            ),
        },
        {
            "id": "dryrun",
            "title": "7. Simulación y caché del índice",
            "text": (
                "La simulación muestra lo que ocurriría sin cambiar nada:\n"
                "• No se copia, mueve ni renombra nada.\n"
                "• No se crea _index.txt, por lo que una simulación no desbloquea la pestaña "
                '"Limpiar".\n'
                "• Las acciones previstas aparecen en el registro y en _log_dry.txt.\n\n"
                "Aun así, la simulación lee la carpeta de destino y guarda una caché de hashes "
                "en la carpeta de la aplicación. La siguiente ejecución real usa esa caché y "
                "luego la elimina. Esto ahorra mucho tiempo en la segunda pasada."
            ),
        },
        {
            "id": "dedup",
            "title": "8. Limpiar duplicados",
            "text": (
                'La pestaña "Limpiar" elimina los nombres duplicados que se crearon durante '
                "la clasificación. Trabaja exclusivamente en la carpeta de destino y solo se "
                "desbloquea cuando allí ha tenido lugar una clasificación real (reconocible "
                "por _index.txt).\n\n"
                "Grupos: NAME.jpg, NAME_1.jpg, NAME_2.jpg ... van juntos.\n\n"
                "Regla estándar:\n"
                "• Si un archivo _1, _2 es idéntico byte a byte al archivo base, se mueve a "
                "Duplicates. El archivo base permanece en la carpeta de destino.\n"
                "• El archivo base se copia una vez por grupo a Duplicates para que puedas "
                "comparar ambas versiones directamente.\n"
                "• Si el contenido difiere, el archivo no se toca.\n\n"
                "Regla ampliada (Force):\n"
                "• Los archivos _1, _2 con contenido distinto también se mueven a Duplicates, "
                "sin comparar el contenido. Antes, el programa pide confirmación.\n"
                "• Pensada para copias de seguridad con el mismo nombre y para dos cámaras con "
                "nombres de archivo casualmente iguales.\n\n"
                "Si falta el archivo base, el número más bajo se renombra al nombre base "
                "(IMG_1.jpg -> IMG.jpg). El archivo permanece en la carpeta de destino.\n\n"
                "No se elimina nada: Duplicates refleja la estructura de carpetas y se omite "
                "en la siguiente clasificación. La limpieza la haces tú. La simulación también "
                "funciona aquí y solo escribe en el registro de simulación."
            ),
        },
        {
            "id": "skip",
            "title": "9. Omitir archivos existentes",
            "text": (
                '"Omitir archivos existentes" evita que se creen archivos _1, _2: si el '
                "archivo de destino ya existe, permanece sin cambios y el archivo de origen "
                "se omite.\n\n"
                "Está pensado para copias de seguridad guardadas con marcas de tiempo "
                "diferentes: en lugar de crear una segunda versión como archivo _1, se "
                "conserva la primera. En el registro, esos archivos aparecen como SKIP "
                "(existe) y cuentan como duplicados.\n\n"
                "Sin esta opción, los archivos con el mismo nombre se convierten en _1, _2, "
                'que puedes revisar más tarde en la pestaña "Limpiar".'
            ),
        },
        {
            "id": "log",
            "title": "10. Ventana del registro",
            "text": (
                "El registro muestra todas las acciones de la ejecución, con colores:\n"
                "• azul: información\n"
                "• amarillo: advertencias\n"
                "• rojo: errores\n"
                "• verde: informe/resumen\n\n"
                "Controles:\n"
                '• "Solo errores": oculta todo lo demás.\n'
                '• "Desplazamiento auto": salta automáticamente al final.\n'
                "• Campo de búsqueda + Intro: salta a la siguiente coincidencia (sin "
                "distinguir mayúsculas).\n"
                '• "Borrar" (Ctrl+L), "Guardar" (Ctrl+S), "Abrir".\n\n'
                "El registro se limita a 50.000 líneas para que las ejecuciones largas no "
                "llenen la memoria. En la carpeta de destino también hay _log.txt; en una "
                "simulación, en su lugar _log_dry.txt."
            ),
        },
        {
            "id": "settings",
            "title": "11. Ajustes, ubicación y idioma",
            "text": (
                "Los datos se guardan en el directorio del usuario en ~/.medien_sortierer:\n"
                "• settings.json: tamaño de la ventana, idioma y últimas carpetas elegidas\n"
                "• app.log: registro técnico del programa\n\n"
                "Los ajustes se escriben al cerrar y se cargan de nuevo en el siguiente "
                "inicio. El idioma se aplica de inmediato, sin reiniciar.\n\n"
                "Después de una ejecución real, la carpeta de destino contiene:\n"
                "• _index.txt: índice de archivos para acelerar las siguientes ejecuciones y "
                'marca de "ya clasificado" (desbloquea la pestaña "Limpiar")\n'
                "• _log.txt: registro de la ejecución\n"
                "• Duplicates: nombres duplicados apartados\n\n"
                "Si la fuente es igual al destino, el programa clasifica automáticamente en la "
                "subcarpeta Sorted. La carpeta de destino nunca se recorre como fuente."
            ),
        },
        {
            "id": "keys",
            "title": "12. Atajos de teclado y solución de problemas",
            "text": (
                "Atajos de teclado:\n"
                "• F1: abrir este manual\n"
                "• F5: iniciar la ejecución\n"
                "• Esc: detener la ejecución\n"
                "• Ctrl+L: borrar el registro\n"
                "• Ctrl+S: guardar el registro\n\n"
                "Los pequeños botones ? junto a los grupos muestran indicaciones breves sobre "
                "el área correspondiente.\n\n"
                "Si algo no funciona como se espera:\n"
                "• Todo acaba en _No_Date: no se encontró ninguna fecha. Instala Pillow para "
                "los datos EXIF y proporciona ffprobe para los vídeos.\n"
                '• La pestaña "Limpiar" está bloqueada: todavía no ha habido una '
                "clasificación real en este destino. Clasifica primero; una simulación no "
                "basta.\n"
                "• Los archivos se llaman _1, _2: hubo una coincidencia de nombres. Limpia en "
                'la pestaña "Limpiar".\n'
                "• Faltan archivos después de clasificar: ya existían con el mismo contenido y "
                "se omitieron como duplicados; el registro los muestra como DUP.\n"
                '• La ejecución se interrumpe con "No hay suficiente espacio": libera espacio '
                "en el destino o elige otra unidad de destino."
            ),
        },
    ],
}
