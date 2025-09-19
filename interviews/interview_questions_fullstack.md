# 100 Preguntas Frecuentes para Entrevistas de Desarrollador Full Stack

## **Frontend (25 preguntas)**

### HTML/CSS

**1. ¿Cuál es la diferencia entre `display: none` y `visibility: hidden`?**
`display: none` elimina completamente el elemento del flujo del documento y no ocupa espacio, mientras que `visibility: hidden` mantiene el espacio ocupado por el elemento pero lo hace invisible.

**2. ¿Qué es el Box Model en CSS?**
Es el modelo que define cómo se calculan las dimensiones de los elementos HTML. Incluye: content, padding, border y margin. La propiedad `box-sizing` puede cambiar este comportamiento.

**3. ¿Cuáles son las diferencias entre `position: relative`, `absolute` y `fixed`?**
- `relative`: posiciona el elemento relativo a su posición normal
- `absolute`: posiciona el elemento relativo a su ancestro posicionado más cercano
- `fixed`: posiciona el elemento relativo al viewport

**4. ¿Qué es Flexbox y cuándo lo usarías?**
Flexbox es un método de layout unidimensional que permite distribuir espacio y alinear elementos en un contenedor. Es ideal para layouts de componentes y alineación de elementos.

**5. ¿Cuál es la diferencia entre `em`, `rem` y `px`?**
- `px`: unidad absoluta, tamaño fijo
- `em`: relativo al font-size del elemento padre
- `rem`: relativo al font-size del elemento root (html)

### JavaScript

**6. ¿Cuál es la diferencia entre `var`, `let` y `const`?**
- `var`: function-scoped, hoisting, puede redeclararse
- `let`: block-scoped, no hoisting, puede reasignarse
- `const`: block-scoped, no hoisting, no puede reasignarse

**7. ¿Qué es el hoisting en JavaScript?**
Es el comportamiento por el cual las declaraciones de variables y funciones se "elevan" al top de su scope durante la compilación, pero solo las declaraciones, no las inicializaciones.

**8. ¿Cuál es la diferencia entre `==` y `===`?**
`==` hace coerción de tipos antes de comparar, mientras que `===` compara valor y tipo sin coerción (strict equality).

**9. ¿Qué son las closures?**
Una closure es la combinación de una función y el entorno léxico en el que fue declarada. Permite que una función acceda a variables de su scope externo incluso después de que la función externa haya retornado.

**10. ¿Cómo funciona el Event Loop en JavaScript?**
El Event Loop es el mecanismo que permite a JavaScript ser asíncrono. Maneja la ejecución del código, eventos y callbacks usando el call stack, callback queue y microtask queue.

**11. ¿Cuál es la diferencia entre `null` y `undefined`?**
- `undefined`: variable declarada pero no inicializada
- `null`: valor asignado intencionalmente que representa "ningún valor"

**12. ¿Qué es el `this` keyword?**
`this` se refiere al contexto de ejecución actual. Su valor depende de cómo se llama la función: en métodos de objetos, event handlers, arrow functions, etc.

### React

**13. ¿Qué son los hooks en React?**
Los hooks son funciones que permiten usar state y otras características de React en componentes funcionales. Ejemplos: `useState`, `useEffect`, `useContext`.

**14. ¿Cuál es la diferencia entre state y props?**
- Props: datos pasados desde el componente padre, inmutables
- State: datos internos del componente, mutables a través de setState

**15. ¿Qué es el Virtual DOM?**
Es una representación en memoria del DOM real. React usa el Virtual DOM para optimizar las actualizaciones comparando el estado anterior con el nuevo (diffing) y aplicando solo los cambios necesarios.

**16. ¿Cuándo usar `useEffect`?**
Para efectos secundarios como llamadas a APIs, suscripciones, manipulación manual del DOM, timers. Se ejecuta después del render.

**17. ¿Qué es prop drilling y cómo se puede evitar?**
Es pasar props a través de múltiples niveles de componentes. Se puede evitar con Context API, Redux, o composition patterns.

**18. ¿Cuál es la diferencia entre componentes controlados y no controlados?**
- Controlados: el valor del input es controlado por React state
- No controlados: el valor es manejado por el DOM directamente usando refs

**19. ¿Qué es el key prop en listas de React?**
Una prop especial que ayuda a React identificar qué elementos han cambiado, se agregaron o eliminaron en listas, optimizando el re-rendering.

**20. ¿Cómo optimizarías el rendimiento de una aplicación React?**
- React.memo para componentes
- useMemo y useCallback para valores y funciones costosas
- Lazy loading con React.lazy
- Separación de código (code splitting)
- Virtualizacion para listas largas

### Frameworks/Tools Frontend

**21. ¿Qué es Webpack?**
Es un module bundler que empaqueta archivos JavaScript y sus dependencias en uno o más bundles. También puede procesar CSS, imágenes y otros assets.

**22. ¿Cuál es la diferencia entre SSR y CSR?**
- SSR (Server-Side Rendering): HTML generado en el servidor
- CSR (Client-Side Rendering): HTML generado en el cliente con JavaScript

**23. ¿Qué es Next.js y cuáles son sus ventajas?**
Framework de React que proporciona SSR/SSG out-of-the-box, routing automático, optimización de imágenes, API routes, y mejor SEO.

**24. ¿Qué es TypeScript y por qué usarlo?**
Es un superset de JavaScript que añade tipado estático. Beneficios: detección temprana de errores, mejor IntelliSense, refactoring más seguro, documentación implícita.

**25. ¿Qué es el PWA (Progressive Web App)?**
Aplicaciones web que usan tecnologías modernas para proporcionar experiencias similares a aplicaciones nativas: offline functionality, push notifications, instalable.

## **Backend (35 preguntas)**

### Node.js/JavaScript Backend

**26. ¿Qué es Node.js?**
Runtime de JavaScript construido sobre el motor V8 de Chrome que permite ejecutar JavaScript en el servidor. Es event-driven, non-blocking I/O.

**27. ¿Cómo funciona el Event Loop en Node.js?**
Maneja operaciones asíncronas usando fases: timers, pending callbacks, poll, check, close callbacks. Permite alta concurrencia sin threading.

**28. ¿Cuál es la diferencia entre `process.nextTick()` y `setImmediate()`?**
- `process.nextTick()`: se ejecuta antes que cualquier otra fase del event loop
- `setImmediate()`: se ejecuta en la fase check del event loop

**29. ¿Qué es middleware en Express?**
Funciones que tienen acceso a req, res y next. Se ejecutan secuencialmente y pueden modificar request/response o terminar el ciclo.

**30. ¿Cómo manejas errores en Node.js?**
- Try/catch para código síncrono
- Callbacks con error-first pattern
- Promises con .catch()
- Async/await con try/catch
- Event emitters para errores no manejados

### APIs y HTTP

**31. ¿Cuál es la diferencia entre REST y GraphQL?**
- REST: múltiples endpoints, over/under-fetching posible, cacheable
- GraphQL: single endpoint, obtiene exactamente lo que necesitas, queries complejas

**32. ¿Qué son los códigos de estado HTTP más importantes?**
- 200 (OK), 201 (Created), 400 (Bad Request)
- 401 (Unauthorized), 403 (Forbidden), 404 (Not Found)
- 500 (Internal Server Error), 502 (Bad Gateway)

**33. ¿Qué es CORS y cómo lo manejas?**
Cross-Origin Resource Sharing. Mecanismo que permite requests desde dominios diferentes. Se maneja con headers como `Access-Control-Allow-Origin`.

**34. ¿Cuál es la diferencia entre authentication y authorization?**
- Authentication: verificar identidad ("¿quién eres?")
- Authorization: verificar permisos ("¿qué puedes hacer?")

**35. ¿Qué es JWT y cómo funciona?**
JSON Web Token. Token self-contained con header, payload y signature. Usado para authentication stateless. Se firma para verificar integridad.

**36. ¿Cómo implementarías rate limiting?**
Usando middleware como express-rate-limit, Redis para contadores distribuidos, o algoritmos como token bucket o sliding window.

**37. ¿Qué es la paginación y cómo la implementarías?**
Técnica para dividir resultados grandes en páginas. Implementación: offset/limit o cursor-based pagination para mejor rendimiento.

### Bases de Datos

**38. ¿Cuál es la diferencia entre SQL y NoSQL?**
- SQL: estructurado, ACID, relacional, esquema fijo
- NoSQL: flexible, eventualmente consistente, varios tipos (document, key-value, graph)

**39. ¿Qué es un índice de base de datos?**
Estructura de datos que mejora la velocidad de consultas. Trade-off: consultas más rápidas vs inserts/updates más lentos y más espacio.

**40. ¿Qué son las transacciones ACID?**
- Atomicity: todo o nada
- Consistency: mantiene reglas de integridad
- Isolation: transacciones concurrentes no interfieren
- Durability: cambios persisten

**41. ¿Cuándo usarías MongoDB vs PostgreSQL?**
- MongoDB: datos no estructurados, desarrollo rápido, escalabilidad horizontal
- PostgreSQL: datos relacionales, transacciones complejas, integridad de datos

**42. ¿Qué es el N+1 problem?**
Problema donde una query inicial genera N queries adicionales. Se soluciona con eager loading, joins, o DataLoader.

**43. ¿Qué son las migraciones de base de datos?**
Scripts versionados que modifican el esquema de BD de forma controlada y reversible. Permiten evolucionar la BD en diferentes ambientes.

### Seguridad

**44. ¿Qué es SQL Injection y cómo prevenirlo?**
Ataque donde se inyecta código SQL malicioso. Prevención: prepared statements, ORMs, validación de input, principio de menor privilegio.

**45. ¿Qué es XSS y cómo prevenirlo?**
Cross-Site Scripting. Inyección de scripts maliciosos. Prevención: sanitización de input, Content Security Policy, escape de output.

**46. ¿Qué es CSRF y cómo prevenirlo?**
Cross-Site Request Forgery. Ataques que ejecutan acciones no deseadas. Prevención: CSRF tokens, SameSite cookies, verificación de origin.

**47. ¿Cómo almacenarías contraseñas de forma segura?**
Usando hashing con salt: bcrypt, scrypt, o Argon2. Nunca plain text o algoritmos rápidos como MD5 o SHA1.

**48. ¿Qué son las variables de entorno y por qué son importantes?**
Configuración externa a la aplicación. Importantes para: secrets, configuración por ambiente, twelve-factor app principles.

### Arquitectura Backend

**49. ¿Qué es la arquitectura de microservicios?**
Patrón donde la aplicación se divide en servicios pequeños e independientes. Ventajas: escalabilidad, tecnologías diversas. Desventajas: complejidad, latencia de red.

**50. ¿Qué es un API Gateway?**
Punto de entrada único para múltiples microservicios. Funciones: routing, authentication, rate limiting, load balancing, monitoring.

**51. ¿Qué es Docker y por qué usarlo?**
Plataforma de containerización que empaqueta aplicaciones con sus dependencias. Beneficios: consistencia entre ambientes, escalabilidad, aislamiento.

**52. ¿Qué son los message queues?**
Sistemas de comunicación asíncrona entre servicios. Ejemplos: RabbitMQ, Apache Kafka, Redis Pub/Sub. Patrones: pub/sub, work queues.

**53. ¿Qué es caching y qué estrategias conoces?**
Almacenamiento temporal de datos frecuentemente accedidos. Estrategias: cache-aside, write-through, write-behind, refresh-ahead.

**54. ¿Cómo manejarías el scaling de una aplicación?**
- Horizontal: más instancias
- Vertical: más recursos por instancia
- Database sharding, read replicas, CDNs, load balancers

**55. ¿Qué es CI/CD?**
Continuous Integration/Continuous Deployment. Automatización de testing, building y deployment. Tools: GitHub Actions, Jenkins, GitLab CI.

**56. ¿Qué son los logs y cómo los estructurarías?**
Registros de eventos de la aplicación. Estructuración: formato consistente (JSON), niveles (error, warn, info), timestamps, context.

**57. ¿Cómo implementarías monitoring en una aplicación?**
- Application metrics (response time, error rate)
- Infrastructure metrics (CPU, memory)
- Business metrics
- Tools: Prometheus, New Relic, DataDog

**58. ¿Qué es testing en backend y qué tipos conoces?**
- Unit tests: funciones individuales
- Integration tests: componentes trabajando juntos
- E2E tests: flujo completo de usuario
- Tools: Jest, Mocha, Supertest

**59. ¿Qué patrones de diseño has usado en backend?**
- Repository pattern: abstracción de data access
- Factory pattern: creación de objetos
- Observer pattern: pub/sub systems
- Singleton pattern: instancia única

**60. ¿Cómo optimizarías queries de base de datos?**
- Índices apropiados
- Evitar N+1 queries
- Usar EXPLAIN para analizar
- Denormalización cuando sea necesario
- Connection pooling

## **Conceptos Generales (25 preguntas)**

### Algoritmos y Estructuras de Datos

**61. ¿Cuál es la diferencia entre Array y Linked List?**
- Array: acceso O(1), inserción/eliminación O(n)
- Linked List: acceso O(n), inserción/eliminación O(1) si tienes referencia

**62. ¿Qué es Big O notation?**
Notación para describir la complejidad temporal y espacial de algoritmos en el peor caso. Común: O(1), O(log n), O(n), O(n²).

**63. ¿Cuándo usarías un Hash Map?**
Para lookups rápidos O(1), cuando necesitas mapear keys a values. Perfecto para caches, contadores, índices.

**64. ¿Qué algoritmos de sorting conoces?**
- Quick Sort: O(n log n) promedio, O(n²) peor caso
- Merge Sort: O(n log n) garantizado, estable
- Bubble Sort: O(n²), simple pero ineficiente

**65. ¿Qué es recursión y cuándo la usarías?**
Función que se llama a sí misma. Útil para: estructuras de datos en árbol, divide y vencerás, backtracking. Cuidado con stack overflow.

### Git y Control de Versiones

**66. ¿Cuál es la diferencia entre `git merge` y `git rebase`?**
- Merge: combina branches preservando historial
- Rebase: reaplica commits sobre otra base, historial linear

**67. ¿Qué es un merge conflict y cómo lo resuelves?**
Ocurre cuando Git no puede merger cambios automáticamente. Resolución: editar archivos conflictivos, marcar como resuelto, commit.

**68. ¿Qué estrategias de branching conoces?**
- Git Flow: master/develop/feature/release/hotfix
- GitHub Flow: master/feature branches
- GitLab Flow: production/pre-production/feature

**69. ¿Cuándo usarías `git cherry-pick`?**
Para aplicar commits específicos de una branch a otra, útil para hotfixes o features específicos sin merger toda la branch.

**70. ¿Qué hace `git stash`?**
Guarda cambios no commiteados temporalmente, útil para cambiar de branch rápidamente sin hacer commit incompleto.

### DevOps y Deployment

**71. ¿Qué es la diferencia entre development, staging y production?**
- Development: ambiente local de desarrollo
- Staging: replica de production para testing
- Production: ambiente live donde interactúan usuarios reales

**72. ¿Qué es Infrastructure as Code?**
Gestión de infraestructura usando código (Terraform, CloudFormation). Beneficios: versionado, reproducibilidad, consistencia.

**73. ¿Qué son las environment variables?**
Configuración externa que varía por ambiente. Uso: API keys, database URLs, feature flags. Siguiendo twelve-factor app.

**74. ¿Qué es blue-green deployment?**
Estrategia donde mantienes dos ambientes idénticos. Cambias tráfico del azul (actual) al verde (nuevo) instantáneamente.

**75. ¿Qué es un health check?**
Endpoint que verifica si el servicio está funcionando correctamente. Usado por load balancers y monitoring systems.

### Performance y Optimización

**76. ¿Cómo optimizarías el tiempo de carga de una web?**
- Minificación de assets
- Compresión (gzip)
- CDN para assets estáticos
- Lazy loading de imágenes
- Critical CSS inlined
- HTTP/2

**77. ¿Qué es lazy loading?**
Técnica que retrasa la carga de recursos hasta que son necesarios. Común en imágenes, componentes de React, rutas.

**78. ¿Cómo detectarías memory leaks?**
- Browser DevTools Memory tab
- Node.js: process.memoryUsage(), heapdump
- Monitoring tools
- Señales: memoria creciente constantemente

**79. ¿Qué es debouncing y throttling?**
- Debouncing: ejecuta función después de que eventos paren de ocurrir
- Throttling: limita ejecuciones a intervalos regulares

**80. ¿Cómo cachearías datos en una aplicación?**
- Browser: localStorage, sessionStorage, HTTP cache
- Server: Redis, Memcached, in-memory cache
- CDN para assets estáticos
- Database query cache

### Testing

**81. ¿Cuál es la diferencia entre unit, integration y e2e tests?**
- Unit: funciones aisladas, rápidos, mock dependencies
- Integration: componentes juntos, más lentos
- E2E: flujo completo del usuario, más realistas pero frágiles

**82. ¿Qué es TDD (Test Driven Development)?**
Metodología: escribir test → escribir código mínimo para pasar → refactorizar. Ciclo red-green-refactor.

**83. ¿Qué son los mocks y stubs?**
- Mock: objeto fake que verifica interacciones
- Stub: objeto fake con respuestas predefinidas
- Ambos aíslan código bajo testing

**84. ¿Cómo testearías una API REST?**
- Unit tests para lógica de negocio
- Integration tests para endpoints completos
- Tools: Jest, Supertest, Postman/Newman
- Verificar status codes, response body, headers

**85. ¿Qué métricas de testing consideras importantes?**
- Code coverage (pero no obsesionarse)
- Test execution time
- Test success rate
- Maintainability de tests

## **Preguntas Situacionales y Experiencia (15 preguntas)**

### Resolución de Problemas

**86. ¿Cómo debuggearías una aplicación que se cuelga en producción?**
1. Revisar logs y metrics
2. Identificar patrón (timing, load, specific actions)
3. Reproducir en staging
4. Usar profiling tools
5. Implementar más logging si es necesario
6. Hotfix y post-mortem

**87. ¿Cómo manejarías una aplicación con problemas de performance?**
1. Identificar bottlenecks con profiling
2. Optimizar queries de DB
3. Implementar caching
4. Optimizar frontend (bundle size, assets)
5. Considerar CDN
6. Evaluar scaling horizontal

**88. ¿Qué harías si una feature nueva causa bugs en producción?**
1. Rollback inmediato si es crítico
2. Feature flag para desactivar
3. Hotfix si es menor
4. Análisis de root cause
5. Mejorar testing y QA process

**89. ¿Cómo diseñarías un sistema de notificaciones?**
1. Message queue para reliability
2. Templates para diferentes tipos
3. User preferences y opt-out
4. Rate limiting para no spam
5. Delivery methods (email, push, SMS)
6. Analytics y tracking

**90. ¿Cómo implementarías un sistema de comentarios?**
1. Schema: users, posts, comments (nested)
2. API endpoints CRUD
3. Real-time con WebSockets
4. Moderation system
5. Pagination para performance
6. Caching para comentarios populares

### Liderazgo y Colaboración

**91. ¿Cómo manejarías conflicto técnico en el equipo?**
1. Escuchar todas las perspectivas
2. Evaluar pros/cons objetivamente
3. Hacer POC si es necesario
4. Decidir basado en requirements y constraints
5. Documentar decisión y reasoning

**92. ¿Cómo mentorarías a un developer junior?**
1. Pair programming regular
2. Code reviews constructivos
3. Asignar tasks graduales en dificultad
4. Sharing de recursos y learning path
5. Feedback frecuente y encouragement

**93. ¿Cómo priorizarías features con PM y stakeholders?**
1. Entender business value y urgencia
2. Estimar effort técnico
3. Considerar dependencies
4. Balancear quick wins vs long-term value
5. Comunicar trade-offs claramente

**94. ¿Cómo comunicarías problemas técnicos complejos a non-technical stakeholders?**
1. Usar analogías simples
2. Enfocar en business impact
3. Proporcionar opciones con pros/cons
4. Timeline realístico
5. Seguimiento regular

**95. ¿Cómo mantendrías la calidad de código en el equipo?**
1. Code reviews obligatorios
2. Linting y formatting automático
3. Testing requirements
4. Documentation standards
5. Regular refactoring sessions

### Aprendizaje y Crecimiento

**96. ¿Cómo te mantienes actualizado con nuevas tecnologías?**
1. Tech blogs y newsletters
2. Conferencias y meetups
3. Open source contributions
4. Side projects para experimentar
5. Team knowledge sharing sessions

**97. ¿Cuál ha sido el proyecto más desafiante y qué aprendiste?**
[Respuesta personal basada en experiencia real, pero estructura:]
1. Contexto del proyecto
2. Desafíos específicos
3. Approach tomado
4. Lecciones aprendidas
5. Cómo aplicarías esas lecciones ahora

**98. ¿Cómo decides qué tecnología usar para un proyecto nuevo?**
1. Analizar requirements y constraints
2. Evaluar team expertise
3. Considerar long-term maintainability
4. Community support y ecosystem
5. Performance requirements
6. Timeline del proyecto

**99. ¿Qué tecnología te emociona más actualmente y por qué?**
[Respuesta personal, pero mostrar:]
1. Conocimiento actual de la tecnología
2. Potential business impact
3. How it solves current problems
4. Plans para aprenderla más

**100. ¿Dónde te ves en 5 años como developer?**
[Respuesta personal que muestre:]
1. Ambiciones claras (technical lead, architect, etc.)
2. Skills que quieres desarrollar
3. Impact que quieres tener
4. Balance entre technical y leadership growth

---

## **Consejos para las Entrevistas**

### Antes de la Entrevista
- Investigar la empresa y sus productos
- Revisar la descripción del trabajo
- Preparar preguntas sobre el rol y la empresa
- Tener examples específicos de proyectos pasados

### Durante la Entrevista
- Pensar en voz alta al resolver problemas
- Hacer preguntas clarificadoras
- Admitir cuando no sabes algo, pero mostrar cómo lo aprenderías
- Relacionar respuestas con experiencia real cuando sea posible

### Después de la Entrevista
- Seguir up con thank you email
- Hacer las preguntas que se te olvidaron
- Reflejar sobre qué fue bien y qué mejorar

### Red Flags que Evitar
- Criticar employers anteriores
- Parecer desinteresado o poco preparado
- No hacer preguntas sobre la empresa
- Mentir sobre experiencia o skills

**Recuerda:** Las entrevistas son conversaciones bilaterales. No solo te están evaluando a ti, tú también evalúas si la empresa y el rol son fit para ti.