# Declaración sobre el uso de inteligencia artificial

En la elaboración de esta tesis doctoral se ha empleado una herramienta de inteligencia artificial generativa, Claude (Anthropic), a través de su entorno de programación Claude Code, como apoyo en las tareas que se detallan a continuación. Su uso se ha limitado a esas tareas, y en todas ellas la autora ha supervisado, revisado y validado los resultados. Las preguntas de investigación, el diseño del corpus y de los experimentos, la anotación terminológica, la interpretación de los resultados, las conclusiones y la redacción de la tesis son obra de la autora, que asume la plena responsabilidad de su contenido.

## Tareas en las que se ha empleado

1. **Refactorización del código.** Los programas de la tesis (el procesamiento del corpus, la extracción de candidatos a término, el entrenamiento y la evaluación de los modelos y la herramienta TECLA) los ha diseñado y escrito la autora, a partir de su propio pseudocódigo. La herramienta de IA se ha empleado para refactorizarlos, es decir, para mejorar su organización interna sin cambiar lo que hacen: dividir el código en partes más claras y reutilizables, eliminar repeticiones, simplificar algunas instrucciones y documentarlo. El objetivo era que el código fuera más fácil de leer, mantener y reproducir por otros investigadores. Ni el método de extracción ni el diseño de los experimentos ni sus resultados dependen de esa refactorización.

2. **Aplicación de pruebas de contraste de hipótesis.** Implementación y ejecución de las pruebas estadísticas con que se contrastan los resultados:
   - la prueba de rangos con signo de Wilcoxon, con la corrección de Holm, para comparar partición a partición el modelo basado en rasgos (CRF) y el modelo neuronal (BiLSTM-CRF) en las ocho comparaciones que resultan de dos lenguas y cuatro niveles de reserva (capítulos 5 y 7);
   - la prueba *t*, con la corrección de Holm, para determinar qué variaciones de la ablación por familias de rasgos se distinguen de cero (72 contrastes: nueve familias, dos lenguas y cuatro niveles; capítulos 5 y 7);
   - la prueba *t* de una muestra, con la corrección de Holm, para comparar los dos modelos en la validación externa sobre ACTER con el protocolo *leave-one-domain-out* (capítulo 7);
   - la prueba exacta de Fisher, para comprobar si la cobertura de las líneas temáticas difiere entre los dos subcorpus (capítulo 4).

3. **Revisión final de estilo e incongruencias.** Revisión de la coherencia interna del texto: numeración y remisiones a capítulos, apartados, tablas y figuras; concordancia de las cifras entre capítulos, tablas, resúmenes y material complementario; coherencia terminológica y uniformidad del formato. Las correcciones propuestas fueron revisadas y aceptadas o descartadas por la autora una a una.

4. **Generación de algunas figuras.** Elaboración del código de las siguientes figuras, a partir de las indicaciones y el contenido aportados por la autora:
   - Figura 3.2: Resultado de la extracción según el tipo de método y su contraste con la referencia humana.
   - Figura 3.3: Lectura de una oración por una red LSTM bidireccional (BiLSTM).
   - Figura 5.5: Arquitectura del modelo neuronal (BiLSTM-CRF) aplicada al reconocimiento de términos.
   - Figura 5.6: Esquema ilustrativo del espacio vectorial que aprende el modelo neuronal.
