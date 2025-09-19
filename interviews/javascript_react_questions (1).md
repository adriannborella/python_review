# 200 Preguntas sobre JavaScript y React - Guía Completa de Entrevista

## **JAVASCRIPT - 100 PREGUNTAS**

### **Conceptos Fundamentales (20 preguntas)**

**1. ¿Cuáles son los tipos de datos primitivos en JavaScript?**
Los tipos primitivos son: `number`, `string`, `boolean`, `undefined`, `null`, `symbol` (ES6) y `bigint` (ES2020). Son inmutables y se almacenan por valor.

**2. ¿Cuál es la diferencia entre `null` y `undefined`?**
- `undefined`: Variable declarada pero no inicializada, o propiedad no existente
- `null`: Valor asignado intencionalmente que representa "sin valor" o "vacío"

**3. ¿Qué es el hoisting en JavaScript?**
Es el comportamiento donde las declaraciones de variables (`var`) y funciones se "elevan" al top de su scope durante la fase de compilación. Solo se elevan las declaraciones, no las inicializaciones.

```javascript
console.log(x); // undefined (no error)
var x = 5;

// Se interpreta como:
var x;
console.log(x); // undefined
x = 5;
```

**4. ¿Cuál es la diferencia entre `var`, `let` y `const`?**
- `var`: function-scoped, hoisting, puede redeclararse
- `let`: block-scoped, temporal dead zone, puede reasignarse
- `const`: block-scoped, temporal dead zone, no puede reasignarse

**5. ¿Qué es el Temporal Dead Zone?**
Es el período entre la entrada al scope y la declaración donde la variable existe pero no puede ser accedida. Aplica a `let` y `const`.

```javascript
console.log(x); // ReferenceError
let x = 5;
```

**6. ¿Cuál es la diferencia entre `==` y `===`?**
- `==`: Comparación con coerción de tipos
- `===`: Comparación estricta sin coerción de tipos

```javascript
'5' == 5;  // true (coerción)
'5' === 5; // false (tipos diferentes)
```

**7. ¿Qué es la coerción de tipos en JavaScript?**
Es la conversión automática o explícita de valores de un tipo a otro. JavaScript realiza coerción implícita en operaciones y comparaciones.

**8. ¿Cómo funciona el operador `typeof`?**
Devuelve una string indicando el tipo de la variable. Casos especiales: `typeof null` devuelve `"object"` (bug histórico).

**9. ¿Qué es NaN y cómo lo detectas?**
`NaN` (Not a Number) representa un valor numérico inválido. Se detecta con `Number.isNaN()` o `isNaN()`, siendo `Number.isNaN()` más preciso.

```javascript
Number.isNaN(NaN);     // true
Number.isNaN('hello'); // false
isNaN('hello');        // true (coerción)
```

**10. ¿Qué es el scope en JavaScript?**
El scope determina la accesibilidad de variables en diferentes partes del código. Tipos: global, function, block (ES6).

**11. ¿Qué es el scope chain?**
Es la cadena de scopes que JavaScript recorre para resolver referencias de variables, desde el scope actual hasta el global.

**12. ¿Qué son las expresiones y statements?**
- **Expresión**: Produce un valor (`2 + 2`, `true`, `function() {}`)
- **Statement**: Ejecuta una acción (`if`, `for`, `var x = 5`)

**13. ¿Qué es el strict mode?**
`"use strict"` habilita un modo más estricto que previene errores comunes: no permite variables no declaradas, elimina `this` global, etc.

**14. ¿Cómo se maneja la herencia en JavaScript?**
A través del prototype chain. Cada objeto tiene una referencia a su prototipo, formando una cadena hasta `Object.prototype`.

**15. ¿Qué es el operador de coalescencia nula (`??`)?**
Devuelve el operando derecho si el izquierdo es `null` o `undefined`. Diferente de `||` que considera todos los valores falsy.

```javascript
null ?? 'default';      // 'default'
undefined ?? 'default'; // 'default'
0 ?? 'default';         // 0
'' ?? 'default';        // ''
```

**16. ¿Qué es el optional chaining (`?.`)?**
Permite acceder a propiedades anidadas sin errores si algún eslabón es `null` o `undefined`.

```javascript
user?.address?.street; // undefined si user o address es null/undefined
```

**17. ¿Qué son los template literals?**
Strings delimitados por backticks que permiten interpolación de expresiones y strings multilínea.

```javascript
const name = 'John';
const greeting = `Hello, ${name}!`;
```

**18. ¿Qué es destructuring?**
Sintaxis que permite extraer valores de arrays o propiedades de objetos en variables distintas.

```javascript
const [a, b] = [1, 2];
const {name, age} = {name: 'John', age: 30};
```

**19. ¿Qué son los spread y rest operators?**
- **Spread (`...`)**: Expande elementos de un iterable
- **Rest (`...`)**: Agrupa elementos restantes en un array

```javascript
const arr = [1, 2, 3];
const newArr = [...arr, 4]; // spread
const [first, ...rest] = arr; // rest
```

**20. ¿Qué es el operador ternario?**
Operador condicional que evalúa una expresión y devuelve uno de dos valores según el resultado.

```javascript
const result = condition ? valueIfTrue : valueIfFalse;
```

### **Funciones (20 preguntas)**

**21. ¿Cuáles son las formas de declarar funciones en JavaScript?**
- Function declaration: `function name() {}`
- Function expression: `const name = function() {}`
- Arrow function: `const name = () => {}`
- Constructor: `const name = new Function()`

**22. ¿Cuál es la diferencia entre function declaration y function expression?**
- **Declaration**: Hoisting completo, disponible antes de su declaración
- **Expression**: Solo se eleva la variable, no la función

**23. ¿Qué son las arrow functions y cómo difieren de las funciones regulares?**
Funciones con sintaxis más concisa. Diferencias: no tienen `this` propio, no tienen `arguments`, no pueden ser constructores.

```javascript
// Regular function
function regular() {
  console.log(this); // contexto dinámico
}

// Arrow function
const arrow = () => {
  console.log(this); // contexto léxico
};
```

**24. ¿Qué es el `this` keyword?**
Referencia al contexto de ejecución actual. Su valor depende de cómo se invoca la función: método de objeto, function call, arrow function, etc.

**25. ¿Cómo funciona el binding de `this`?**
Se puede controlar con:
- `call()`: invoca con `this` específico y argumentos individuales
- `apply()`: igual que call pero argumentos en array
- `bind()`: retorna nueva función con `this` fijo

```javascript
const obj = {name: 'John'};
function greet() { console.log(this.name); }

greet.call(obj);    // 'John'
greet.apply(obj);   // 'John'
const bound = greet.bind(obj); // función con this fijo
```

**26. ¿Qué son las closures?**
Una closure es la combinación de una función y el entorno léxico en el que fue declarada, permitiendo acceso a variables del scope externo.

```javascript
function outer(x) {
  return function inner(y) {
    return x + y; // accede a 'x' del scope externo
  };
}
const add5 = outer(5);
add5(3); // 8
```

**27. ¿Para qué sirven las closures?**
- Encapsulación y privacidad
- Factory functions
- Module pattern
- Callbacks que mantienen estado
- Event handlers con contexto

**28. ¿Qué es el currying?**
Técnica que transforma una función con múltiples parámetros en una secuencia de funciones que toman un parámetro cada una.

```javascript
// Normal function
function add(a, b, c) {
  return a + b + c;
}

// Curried function
const curriedAdd = (a) => (b) => (c) => a + b + c;
curriedAdd(1)(2)(3); // 6
```

**29. ¿Qué son las Higher-Order Functions?**
Funciones que reciben otras funciones como argumentos o retornan funciones. Ejemplos: `map`, `filter`, `reduce`.

**30. ¿Qué es el object `arguments`?**
Objeto array-like disponible en funciones regulares que contiene todos los argumentos pasados. No disponible en arrow functions.

```javascript
function example() {
  console.log(arguments.length);
  console.log(Array.from(arguments));
}
```

**31. ¿Qué son los parámetros rest?**
Sintaxis que permite representar un número indefinido de argumentos como un array.

```javascript
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
```

**32. ¿Qué son los parámetros por defecto?**
Valores asignados a parámetros cuando no se proporciona argumento o es `undefined`.

```javascript
function greet(name = 'World') {
  return `Hello, ${name}!`;
}
```

**33. ¿Qué es la recursión?**
Técnica donde una función se llama a sí misma. Útil para estructuras de datos anidadas, algoritmos divide y vencerás.

```javascript
function factorial(n) {
  if (n <= 1) return 1;
  return n * factorial(n - 1);
}
```

**34. ¿Qué es memoization?**
Técnica de optimización que almacena resultados de funciones costosas para evitar recálculos.

```javascript
function memoize(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (key in cache) return cache[key];
    return cache[key] = fn.apply(this, args);
  };
}
```

**35. ¿Qué son las funciones puras?**
Funciones que siempre devuelven el mismo resultado para los mismos argumentos y no tienen efectos secundarios.

**36. ¿Qué es el concepto de "first-class functions"?**
En JavaScript, las funciones son ciudadanos de primera clase: pueden ser asignadas a variables, pasadas como argumentos, retornadas de otras funciones.

**37. ¿Qué es una IIFE?**
Immediately Invoked Function Expression. Función que se ejecuta inmediatamente tras su definición.

```javascript
(function() {
  console.log('IIFE executed');
})();

// Arrow function IIFE
(() => {
  console.log('Arrow IIFE');
})();
```

**38. ¿Cuándo usarías una IIFE?**
- Crear scope privado
- Evitar contaminar el namespace global
- Módulos (antes de ES6 modules)
- Inicialización única

**39. ¿Qué es function hoisting?**
Las function declarations se elevan completamente (declaración e implementación), mientras que las function expressions solo elevan la variable.

**40. ¿Cómo implementarías un debounce function?**
```javascript
function debounce(func, delay) {
  let timeoutId;
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), delay);
  };
}
```

### **Objetos y Prototipos (15 preguntas)**

**41. ¿Cómo se crean objetos en JavaScript?**
- Object literal: `{}`
- Constructor function: `new Object()`
- `Object.create()`
- Factory functions
- ES6 classes

**42. ¿Qué es el prototype en JavaScript?**
Mecanismo por el cual los objetos heredan propiedades y métodos de otros objetos. Cada función tiene una propiedad `prototype`.

**43. ¿Cuál es la diferencia entre `__proto__` y `prototype`?**
- `__proto__`: Propiedad de instancias que apunta al prototype del constructor
- `prototype`: Propiedad de funciones constructoras que define el prototipo para instancias

**44. ¿Cómo funciona la herencia prototípica?**
Los objetos heredan directamente de otros objetos a través del prototype chain. Si una propiedad no existe en el objeto, se busca en su prototipo.

```javascript
function Animal(name) {
  this.name = name;
}

Animal.prototype.speak = function() {
  console.log(`${this.name} makes a sound`);
};

function Dog(name) {
  Animal.call(this, name);
}

Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;
```

**45. ¿Qué hace `Object.create()`?**
Crea un nuevo objeto usando un objeto existente como prototype del nuevo objeto.

```javascript
const animal = {
  speak() {
    console.log(`${this.name} speaks`);
  }
};

const dog = Object.create(animal);
dog.name = 'Buddy';
dog.speak(); // 'Buddy speaks'
```

**46. ¿Cuáles son los métodos útiles de Object?**
- `Object.keys()`: array de propiedades enumerables
- `Object.values()`: array de valores
- `Object.entries()`: array de pares [key, value]
- `Object.assign()`: copia propiedades
- `Object.freeze()`: hace inmutable
- `Object.seal()`: previene agregar/eliminar propiedades

**47. ¿Cuál es la diferencia entre `Object.freeze()` y `Object.seal()`?**
- `freeze()`: Inmutable completo (no se puede modificar, agregar o eliminar)
- `seal()`: Solo se pueden modificar propiedades existentes

**48. ¿Qué es property descriptor?**
Objeto que describe las características de una propiedad: `value`, `writable`, `enumerable`, `configurable`.

```javascript
Object.defineProperty(obj, 'prop', {
  value: 42,
  writable: false,
  enumerable: true,
  configurable: false
});
```

**49. ¿Cómo verificas si una propiedad existe en un objeto?**
- `in` operator: incluye prototype chain
- `hasOwnProperty()`: solo propiedades propias
- `Object.hasOwn()`: versión moderna de hasOwnProperty

**50. ¿Qué son los getters y setters?**
Métodos que permiten definir el comportamiento de acceso y asignación a propiedades.

```javascript
const obj = {
  _value: 0,
  get value() {
    return this._value;
  },
  set value(val) {
    this._value = val;
  }
};
```

**51. ¿Cómo iteras sobre las propiedades de un objeto?**
- `for...in`: propiedades enumerables (incluye prototype)
- `Object.keys()`: solo propiedades propias
- `Object.getOwnPropertyNames()`: incluye no enumerables

**52. ¿Qué es el `constructor` property?**
Propiedad que referencia la función que creó la instancia del objeto.

**53. ¿Cómo clonas objetos en JavaScript?**
- Shallow copy: `Object.assign()`, spread operator
- Deep copy: `JSON.parse(JSON.stringify())` (limitado), libraries como Lodash

**54. ¿Qué son las computed property names?**
Sintaxis ES6 que permite usar expresiones como nombres de propiedades en object literals.

```javascript
const prop = 'dynamicKey';
const obj = {
  [prop]: 'value',
  [`${prop}2`]: 'value2'
};
```

**55. ¿Cómo funciona el operador `new`?**
1. Crea un objeto vacío
2. Asigna el prototype del constructor al objeto
3. Ejecuta el constructor con `this` apuntando al objeto
4. Retorna el objeto (o el valor retornado por el constructor si es objeto)

### **Arrays (15 preguntas)**

**56. ¿Cuáles son los métodos principales de Array?**
- **Mutating**: `push()`, `pop()`, `shift()`, `unshift()`, `splice()`, `sort()`, `reverse()`
- **Non-mutating**: `slice()`, `concat()`, `map()`, `filter()`, `reduce()`

**57. ¿Cuál es la diferencia entre `slice()` y `splice()`?**
- `slice()`: No muta, extrae porción del array
- `splice()`: Muta, remueve/agrega elementos

**58. ¿Cómo funciona `map()`?**
Crea nuevo array con los resultados de aplicar una función a cada elemento.

```javascript
const numbers = [1, 2, 3];
const doubled = numbers.map(x => x * 2); // [2, 4, 6]
```

**59. ¿Cómo funciona `filter()`?**
Crea nuevo array con elementos que pasan la prueba de la función callback.

```javascript
const numbers = [1, 2, 3, 4];
const evens = numbers.filter(x => x % 2 === 0); // [2, 4]
```

**60. ¿Cómo funciona `reduce()`?**
Aplica función reductora a cada elemento del array, resultando en un valor único.

```javascript
const numbers = [1, 2, 3, 4];
const sum = numbers.reduce((acc, curr) => acc + curr, 0); // 10
```

**61. ¿Cuál es la diferencia entre `forEach()` y `map()`?**
- `forEach()`: Ejecuta función para cada elemento, no retorna nada
- `map()`: Transforma elementos y retorna nuevo array

**62. ¿Cómo encuentras elementos en un array?**
- `find()`: primer elemento que cumple condición
- `findIndex()`: índice del primer elemento que cumple condición
- `includes()`: si contiene el valor
- `indexOf()`: índice de la primera ocurrencia

**63. ¿Cómo verificas si algo es un array?**
- `Array.isArray()`: método recomendado
- `instanceof Array`: puede fallar con frames
- `Object.prototype.toString.call()`: más robusto

**64. ¿Qué son los array-like objects?**
Objetos que tienen índices numéricos y propiedad `length` pero no son arrays. Ejemplo: `arguments`, NodeLists.

```javascript
// Convertir a array
Array.from(arrayLike);
Array.prototype.slice.call(arrayLike);
[...arrayLike];
```

**65. ¿Cómo ordenas arrays?**
`sort()` convierte elementos a strings por defecto. Para orden numérico:

```javascript
numbers.sort((a, b) => a - b); // ascendente
numbers.sort((a, b) => b - a); // descendente
```

**66. ¿Cómo eliminas duplicados de un array?**
```javascript
// Con Set
const unique = [...new Set(array)];

// Con filter
const unique = array.filter((item, index) => array.indexOf(item) === index);

// Con reduce
const unique = array.reduce((acc, curr) => 
  acc.includes(curr) ? acc : [...acc, curr], []);
```

**67. ¿Cómo aplanas arrays anidados?**
```javascript
// Un nivel
[1, [2, 3]].flat(); // [1, 2, 3]

// Múltiples niveles
[1, [2, [3, 4]]].flat(2); // [1, 2, 3, 4]

// Todos los niveles
array.flat(Infinity);
```

**68. ¿Qué es `flatMap()`?**
Combina `map()` y `flat()` en una operación.

```javascript
const arr = [1, 2, 3];
arr.flatMap(x => [x, x * 2]); // [1, 2, 2, 4, 3, 6]
```

**69. ¿Cómo verificas si todos/algunos elementos cumplen una condición?**
- `every()`: todos los elementos deben cumplir
- `some()`: al menos uno debe cumplir

**70. ¿Cómo creas arrays con valores específicos?**
```javascript
// Array vacío con longitud
new Array(5); // [empty × 5]

// Array con valores
Array(5).fill(0); // [0, 0, 0, 0, 0]

// Secuencia de números
Array.from({length: 5}, (_, i) => i); // [0, 1, 2, 3, 4]
```

### **Asincronía (15 preguntas)**

**71. ¿Qué es el Event Loop?**
Mecanismo que permite a JavaScript ejecutar código asíncrono en un entorno single-threaded, manejando el call stack, callback queue y microtask queue.

**72. ¿Cuál es la diferencia entre Call Stack, Callback Queue y Microtask Queue?**
- **Call Stack**: Pila de ejecución síncrona
- **Callback Queue**: Cola de callbacks (setTimeout, eventos)
- **Microtask Queue**: Cola de alta prioridad (Promises, queueMicrotask)

**73. ¿Qué son las Promises?**
Objetos que representan la eventual finalización o falla de una operación asíncrona.

```javascript
const promise = new Promise((resolve, reject) => {
  // operación asíncrona
  if (success) resolve(value);
  else reject(error);
});

promise
  .then(value => console.log(value))
  .catch(error => console.error(error));
```

**74. ¿Cuáles son los estados de una Promise?**
- **Pending**: Estado inicial, ni cumplida ni rechazada
- **Fulfilled**: Operación completada exitosamente
- **Rejected**: Operación falló

**75. ¿Qué es Promise chaining?**
Técnica para ejecutar múltiples operaciones asíncronas en secuencia usando `.then()`.

```javascript
fetch('/api/user')
  .then(response => response.json())
  .then(user => fetch(`/api/posts/${user.id}`))
  .then(response => response.json())
  .then(posts => console.log(posts));
```

**76. ¿Qué son async/await?**
Sintaxis que hace que el código asíncrono se vea y comporte más como código síncrono.

```javascript
async function fetchUser() {
  try {
    const response = await fetch('/api/user');
    const user = await response.json();
    return user;
  } catch (error) {
    console.error('Error:', error);
  }
}
```

**77. ¿Cuál es la diferencia entre Promise y async/await?**
- **Promise**: Basado en callbacks (.then/.catch)
- **async/await**: Sintaxis más limpia, permite try/catch, mejor debugging

**78. ¿Cómo manejas múltiples Promises?**
- `Promise.all()`: Espera que todas se resuelvan (falla si una falla)
- `Promise.allSettled()`: Espera que todas se completen (exitosa o con error)
- `Promise.race()`: Resuelve/rechaza con la primera que se complete
- `Promise.any()`: Resuelve con la primera exitosa

**79. ¿Qué es callback hell?**
Patrón donde callbacks anidados crean código difícil de leer y mantener. Se soluciona con Promises o async/await.

```javascript
// Callback hell
getData(function(a) {
  getMoreData(a, function(b) {
    getEvenMoreData(b, function(c) {
      // ...
    });
  });
});

// Con Promises
getData()
  .then(a => getMoreData(a))
  .then(b => getEvenMoreData(b))
  .then(c => /* ... */);
```

**80. ¿Qué es setTimeout y cómo funciona?**
Función que ejecuta código después de un delay mínimo. No garantiza ejecución exacta debido al Event Loop.

```javascript
setTimeout(() => {
  console.log('Executed after 1000ms');
}, 1000);
```

**81. ¿Cuál es la diferencia entre setTimeout y setInterval?**
- `setTimeout`: Ejecuta una vez después del delay
- `setInterval`: Ejecuta repetidamente cada intervalo

**82. ¿Qué son los microtasks vs macrotasks?**
- **Microtasks**: Promises, queueMicrotask (alta prioridad)
- **Macrotasks**: setTimeout, setInterval, eventos (baja prioridad)

**83. ¿Cómo cancelarías una Promise?**
Las Promises no son cancelables nativamente. Opciones:
- AbortController con fetch
- Wrapper con flag de cancelación
- Libraries como p-cancelable

**84. ¿Qué es el patrón de error-first callback?**
Convención donde el primer parámetro del callback es el error.

```javascript
fs.readFile('file.txt', (error, data) => {
  if (error) {
    console.error(error);
    return;
  }
  console.log(data);
});
```

**85. ¿Cómo convertirías callback-based functions a Promises?**
```javascript
// Manual
function promisify(fn) {
  return function(...args) {
    return new Promise((resolve, reject) => {
      fn(...args, (error, result) => {
        if (error) reject(error);
        else resolve(result);
      });
    });
  };
}

// Node.js built-in
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
```

### **ES6+ Features (15 preguntas)**

**86. ¿Qué son los módulos ES6?**
Sistema nativo de módulos que permite importar y exportar código entre archivos.

```javascript
// export
export const name = 'John';
export default function greet() {}

// import
import greet, { name } from './module.js';
import * as utils from './utils.js';
```

**87. ¿Cuál es la diferencia entre named exports y default export?**
- **Named**: Múltiples exports por módulo, deben importarse con el mismo nombre
- **Default**: Un export por módulo, puede importarse con cualquier nombre

**88. ¿Qué son los Symbols?**
Tipo primitivo único e inmutable, útil para propiedades privadas y evitar colisiones de nombres.

```javascript
const sym = Symbol('description');
const obj = {
  [sym]: 'value'
};

// Well-known symbols
Symbol.iterator, Symbol.hasInstance, Symbol.toPrimitive
```

**89. ¿Qué son los iteradores e iterables?**
- **Iterable**: Objeto que implementa Symbol.iterator
- **Iterator**: Objeto con método `next()` que retorna `{value, done}`

```javascript
const iterable = {
  *[Symbol.iterator]() {
    yield 1;
    yield 2;
    yield 3;
  }
};

for (const value of iterable) {
  console.log(value); // 1, 2, 3
}
```

**90. ¿Qué son los generators?**
Funciones que pueden pausar y reanudar su ejecución, retornando múltiples valores.

```javascript
function* fibonacci() {
  let a = 0, b = 1;
  while (true) {
    yield a;
    [a, b] = [b, a + b];
  }
}

const fib = fibonacci();
console.log(fib.next().value); // 0
console.log(fib.next().value); // 1
```

**91. ¿Qué son los Proxy objects?**
Permiten interceptar y personalizar operaciones en objetos (get, set, has, etc.).

```javascript
const target = {};
const proxy = new Proxy(target, {
  get(obj, prop) {
    console.log(`Getting ${prop}`);
    return obj[prop];
  },
  set(obj, prop, value) {
    console.log(`Setting ${prop} to ${value}`);
    obj[prop] = value;
    return true;
  }
});
```

**92. ¿Qué son los WeakMap y WeakSet?**
Colecciones donde las referencias a objetos son "débiles", permitiendo garbage collection.

```javascript
const wm = new WeakMap();
const obj = {};
wm.set(obj, 'value');
// obj puede ser garbage collected si no hay otras referencias

const ws = new WeakSet();
ws.add(obj);
```

**93. ¿Qué son Map y Set?**
- **Map**: Colección de pares key-value donde keys pueden ser cualquier tipo
- **Set**: Colección de valores únicos

```javascript
const map = new Map();
map.set('key', 'value');
map.set(1, 'number key');

const set = new Set([1, 2, 3, 2]); // {1, 2, 3}
```

**94. ¿Qué son las tagged template literals?**
Función que procesa template literals, recibiendo strings y valores por separado.

```javascript
function tag(strings, ...values) {
  console.log(strings); // ['Hello ', ' world']
  console.log(values);  // ['beautiful']
  return strings[0] + values[0] + strings[1];
}

const name = 'beautiful';
tag`Hello ${name} world`; // 'Hello beautiful world'
```

**95. ¿Qué es la for...of loop?**
Itera sobre objetos iterables (arrays, strings, Maps, Sets).

```javascript
for (const value of [1, 2, 3]) {
  console.log(value); // 1, 2, 3
}

for (const char of 'hello') {
  console.log(char); // h, e, l, l, o
}
```

**96. ¿Cuál es la diferencia entre for...in y for...of?**
- `for...in`: Itera sobre propiedades enumerables (keys)
- `for...of`: Itera sobre valores de objetos iterables

**97. ¿Qué son las clases ES6?**
Syntactic sugar sobre funciones constructoras y prototipos, proporcionando una sintaxis más limpia para OOP.

```javascript
class Animal {
  constructor(name) {
    this.name = name;
  }
  
  speak() {
    console.log(`${this.name} makes a sound`);
  }
  
  static species() {
    return 'Unknown';
  }
}

class Dog extends Animal {
  speak() {
    console.log(`${this.name} barks`);
  }
}
```

**98. ¿Qué son los métodos estáticos en clases?**
Métodos que pertenecen a la clase en sí, no a las instancias. Se llaman en la clase directamente.

**99. ¿Qué son los private fields en clases?**
Campos que solo son accesibles dentro de la clase (sintaxis con `#`).

```javascript
class MyClass {
  #privateField = 'private';
  
  #privateMethod() {
    return this.#privateField;
  }
  
  publicMethod() {
    return this.#privateMethod();
  }
}
```

**100. ¿Qué son los BigInt?**
Tipo de datos para representar enteros más grandes que `Number.MAX_SAFE_INTEGER`.

```javascript
const big = BigInt(9007199254740991);
const big2 = 9007199254740991n; // literal syntax
console.log(big + 1n); // 9007199254740992n
```

---

## **REACT - 100 PREGUNTAS**

### **Conceptos Fundamentales (20 preguntas)**

**1. ¿Qué es React?**
React es una biblioteca de JavaScript para construir interfaces de usuario, especialmente aplicaciones de una sola página (SPAs). Se basa en componentes reutilizables y el concepto de Virtual DOM.

**2. ¿Qué es JSX?**
JSX (JavaScript XML) es una extensión de sintaxis que permite escribir HTML dentro de JavaScript. Se transpila a llamadas de `React.createElement()`.

```javascript
const element = <h1>Hello, World!</h1>;
// Se convierte en:
const element = React.createElement('h1', null, 'Hello, World!');
```

**3. ¿Qué es el Virtual DOM?**
Representación en memoria del DOM real. React usa el Virtual DOM para:
- Comparar el estado anterior con el nuevo (diffing)
- Actualizar solo las partes que cambiaron (reconciliation)
- Mejorar el rendimiento

**4. ¿Cuál es la diferencia entre elementos y componentes?**
- **Elemento**: Objeto plano que describe lo que quieres ver en pantalla
- **Componente**: Función o clase que acepta props y retorna elementos

**5. ¿Qué son los componentes funcionales vs componentes de clase?**
- **Funcionales**: Funciones que reciben props y retornan JSX (preferidos con hooks)
- **Clase**: Clases ES6 que extienden React.Component (legacy approach)

```javascript
// Funcional
function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

// Clase
class Welcome extends React.Component {
  render() {
    return <h1>Hello, {this.props.name}</h1>;
  }
}
```

**6. ¿Qué son las props?**
Argumentos que se pasan a los componentes, similares a parámetros de función. Son inmutables y fluyen de padre a hijo.

**7. ¿Qué es el state?**
Datos privados de un componente que pueden cambiar con el tiempo. Cuando cambia, el componente se re-renderiza.

**8. ¿Cuál es la diferencia entre props y state?**
- **Props**: Datos pasados desde el padre, inmutables
- **State**: Datos internos del componente, mutables

**9. ¿Qué significa "unidirectional data flow"?**
Los datos fluyen en una sola dirección: de componentes padre a hijo a través de props. Los hijos no pueden modificar directamente las props del padre.

**10. ¿Qué es prop drilling?**
Problema donde se pasan props a través de múltiples niveles de componentes que no las necesitan, solo para llegar al componente que sí las necesita.

**11. ¿Cómo se pueden evitar los prop drilling?**
- Context API
- State management (Redux, Zustand)
- Component composition
- Custom hooks

**12. ¿Qué son los children props?**
Prop especial que contiene el contenido entre las etiquetas de apertura y cierre de un componente.

```javascript
function Card({ children }) {
  return <div className="card">{children}</div>;
}

<Card>
  <p>This is children content</p>
</Card>
```

**13. ¿Qué es el reconciliation process?**
Algoritmo que React usa para comparar el Virtual DOM anterior con el nuevo y determinar qué cambios aplicar al DOM real.

**14. ¿Qué son las keys en React?**
Atributo especial que ayuda a React identificar qué elementos han cambiado, se agregaron o eliminaron en listas.

```javascript
const items = todos.map(todo => 
  <li key={todo.id}>{todo.text}</li>
);
```

**15. ¿Por qué son importantes las keys?**
- Optimizan el proceso de reconciliation
- Previenen bugs en componentes con estado
- Mejoran el rendimiento en listas dinámicas

**16. ¿Qué es el componente Fragment?**
Wrapper que permite agrupar elementos sin agregar nodos extra al DOM.

```javascript
return (
  <React.Fragment>
    <h1>Title</h1>
    <p>Description</p>
  </React.Fragment>
);

// Sintaxis corta
return (
  <>
    <h1>Title</h1>
    <p>Description</p>
  </>
);
```

**17. ¿Qué son los componentes controlados vs no controlados?**
- **Controlados**: El valor del input es controlado por React state
- **No controlados**: El valor es manejado por el DOM, accedido via refs

```javascript
// Controlado
function ControlledInput() {
  const [value, setValue] = useState('');
  return (
    <input 
      value={value} 
      onChange={e => setValue(e.target.value)} 
    />
  );
}

// No controlado
function UncontrolledInput() {
  const inputRef = useRef();
  return <input ref={inputRef} />;
}
```

**18. ¿Qué es el synthetic event?**
Sistema de eventos de React que wrappea eventos nativos del DOM, proporcionando API consistente entre navegadores.

**19. ¿Cuáles son las reglas de JSX?**
- Solo un elemento raíz (o Fragment)
- Cerrar todos los tags (self-closing para elementos vacíos)
- `className` en lugar de `class`
- `camelCase` para propiedades
- Expresiones JavaScript entre llaves `{}`

**20. ¿Qué es React.StrictMode?**
Componente que activa verificaciones y advertencias adicionales en desarrollo para detectar problemas potenciales.

### **Hooks (25 preguntas)**

**21. ¿Qué son los React Hooks?**
Funciones que permiten usar state y otras características de React en componentes funcionales. Introducidos en React 16.8.

**22. ¿Cuáles son las reglas de los Hooks?**
- Solo llamar Hooks en el nivel superior (no en loops, condiciones, funciones anidadas)
- Solo llamar Hooks desde componentes funcionales o custom hooks

**23. ¿Qué es useState?**
Hook que permite añadir state local a componentes funcionales.

```javascript
function Counter() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>
    </div>
  );
}
```

**24. ¿Cómo funciona el batching en useState?**
React agrupa múltiples actualizaciones de state en una sola re-renderización para mejorar rendimiento.

```javascript
function handleClick() {
  setCount(count + 1);
  setFlag(!flag);
  // Solo una re-renderización
}
```

**25. ¿Qué es useEffect?**
Hook para realizar efectos secundarios en componentes funcionales (equivalente a componentDidMount, componentDidUpdate, componentWillUnmount).

```javascript
useEffect(() => {
  // Efecto
  document.title = `Count: ${count}`;
  
  // Cleanup (opcional)
  return () => {
    document.title = 'React App';
  };
}, [count]); // Dependency array
```

**26. ¿Cuáles son los tipos de useEffect?**
- Sin dependency array: se ejecuta en cada render
- Array vacío `[]`: se ejecuta solo en mount
- Con dependencias `[dep]`: se ejecuta cuando las dependencias cambian

**27. ¿Qué es el cleanup en useEffect?**
Función que se ejecuta para limpiar efectos (cancelar subscripciones, limpiar timers, etc.) antes de que el componente se desmonte o antes del próximo efecto.

**28. ¿Qué es useContext?**
Hook que permite consumir un Context sin necesidad de un Consumer component.

```javascript
const ThemeContext = React.createContext();

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Themed Button</button>;
}
```

**29. ¿Qué es useReducer?**
Hook para manejar state complejo usando un patrón similar a Redux.

```javascript
function reducer(state, action) {
  switch (action.type) {
    case 'increment':
      return { count: state.count + 1 };
    case 'decrement':
      return { count: state.count - 1 };
    default:
      throw new Error();
  }
}

function Counter() {
  const [state, dispatch] = useReducer(reducer, { count: 0 });
  
  return (
    <div>
      Count: {state.count}
      <button onClick={() => dispatch({ type: 'increment' })}>
        +
      </button>
    </div>
  );
}
```

**30. ¿Cuándo usar useState vs useReducer?**
- **useState**: State simple, pocas actualizaciones
- **useReducer**: State complejo, múltiples sub-valores, lógica de actualización compleja

**31. ¿Qué es useRef?**
Hook que retorna un objeto mutable cuya propiedad `.current` persiste entre renders.

```javascript
function FocusInput() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <div>
      <input ref={inputRef} />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}
```

**32. ¿Cuáles son los usos de useRef?**
- Acceder a elementos DOM
- Almacenar valores mutables que no causan re-render
- Mantener referencias a valores entre renders

**33. ¿Qué es useMemo?**
Hook que memoriza el resultado de una computación costosa y solo la recalcula cuando sus dependencias cambian.

```javascript
function ExpensiveComponent({ items }) {
  const expensiveValue = useMemo(() => {
    return items.reduce((sum, item) => sum + item.value, 0);
  }, [items]);
  
  return <div>Total: {expensiveValue}</div>;
}
```

**34. ¿Qué es useCallback?**
Hook que memoriza una función y solo crea una nueva instancia cuando sus dependencias cambian.

```javascript
function Parent({ items }) {
  const [filter, setFilter] = useState('');
  
  const handleClick = useCallback((id) => {
    // handle click logic
  }, []);
  
  return (
    <div>
      {items.map(item => 
        <Child 
          key={item.id} 
          item={item} 
          onClick={handleClick} 
        />
      )}
    </div>
  );
}
```

**35. ¿Cuándo usar useMemo vs useCallback?**
- **useMemo**: Memoriza valores/objetos computados
- **useCallback**: Memoriza funciones

**36. ¿Qué son los custom hooks?**
Funciones JavaScript que usan otros hooks y permiten extraer lógica de componentes para reutilizar.

```javascript
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  
  const increment = useCallback(() => setCount(c => c + 1), []);
  const decrement = useCallback(() => setCount(c => c - 1), []);
  const reset = useCallback(() => setCount(initialValue), [initialValue]);
  
  return { count, increment, decrement, reset };
}
```

**37. ¿Cómo compartir lógica entre componentes?**
- Custom hooks
- Higher-Order Components (HOCs)
- Render props
- Context API

**38. ¿Qué es useLayoutEffect?**
Similar a useEffect pero se ejecuta sincrónicamente después de todas las mutaciones del DOM, antes de que el navegador pinte.

**39. ¿Cuándo usar useLayoutEffect vs useEffect?**
- **useLayoutEffect**: Cuando necesitas leer/modificar DOM antes del paint
- **useEffect**: Para la mayoría de casos (asíncrono)

**40. ¿Qué es useImperativeHandle?**
Hook que customiza la instancia expuesta cuando se usa `ref` con `forwardRef`.

**41. ¿Qué es useDebugValue?**
Hook para mostrar una etiqueta en React DevTools para custom hooks.

**42. ¿Cómo manejarías el estado global con hooks?**
- Context API + useContext
- Custom hooks que encapsulen lógica de estado
- Libraries como Zustand que usan hooks

**43. ¿Qué son las dependencies en hooks?**
Array que especifica qué valores debe "observar" el hook para decidir cuándo ejecutarse o recalcularse.

**44. ¿Qué pasa si omites dependencias en useEffect?**
El efecto puede usar valores obsoletos (stale closures) o no ejecutarse cuando debería.

**45. ¿Cómo simular ciclos de vida con hooks?**
- `componentDidMount`: `useEffect(() => {}, [])`
- `componentDidUpdate`: `useEffect(() => {})`
- `componentWillUnmount`: cleanup function en useEffect

### **Lifecycle y Performance (15 preguntas)**

**46. ¿Cuáles son los métodos de ciclo de vida en componentes de clase?**
- **Mounting**: constructor, componentDidMount
- **Updating**: componentDidUpdate, getSnapshotBeforeUpdate
- **Unmounting**: componentWillUnmount
- **Error**: componentDidCatch, getDerivedStateFromError

**47. ¿Qué es React.memo?**
Higher-order component que memoriza componentes funcionales, similar a PureComponent para clases.

```javascript
const MemoizedComponent = React.memo(function MyComponent({ name }) {
  return <div>Hello {name}</div>;
});

// Con custom comparison
const MemoizedComponent = React.memo(MyComponent, (prevProps, nextProps) => {
  return prevProps.name === nextProps.name;
});
```

**48. ¿Cuándo usar React.memo?**
- Componentes que renderizan frecuentemente
- Componentes con props complejas
- Cuando el costo de memorización es menor que el re-render

**49. ¿Qué es PureComponent?**
Clase base que implementa `shouldComponentUpdate` con shallow comparison de props y state.

**50. ¿Cómo optimizar el rendimiento en React?**
- React.memo para componentes funcionales
- useMemo para valores costosos
- useCallback para funciones estables
- Lazy loading con React.lazy
- Code splitting
- Virtualization para listas largas

**51. ¿Qué es React.lazy?**
Función que permite cargar componentes dinámicamente (code splitting).

```javascript
const LazyComponent = React.lazy(() => import('./LazyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
}
```

**52. ¿Qué es Suspense?**
Componente que permite especificar el loading state mientras se espera que algún componente hijo termine de cargar.

**53. ¿Qué causa re-renders innecesarios?**
- Crear objetos/arrays inline en props
- Pasar funciones inline como props
- Context value que cambia en cada render
- No usar React.memo cuando es necesario

**54. ¿Cómo profilerías una aplicación React?**
- React DevTools Profiler
- Browser DevTools Performance tab
- React.Profiler API
- Libraries como why-did-you-render

**55. ¿Qué es el patrón de render prop?**
Técnica para compartir código entre componentes usando una prop cuyo valor es una función.

```javascript
function DataProvider({ render }) {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    fetchData().then(setData);
  }, []);
  
  return render(data);
}

<DataProvider render={data => (
  <div>{data ? <p>{data.message}</p> : <p>Loading...</p>}</div>
)} />
```

**56. ¿Qué son los Higher-Order Components (HOCs)?**
Funciones que toman un componente y retornan un nuevo componente con funcionalidad adicional.

```javascript
function withLoading(Component) {
  return function WithLoadingComponent({ isLoading, ...props }) {
    if (isLoading) return <div>Loading...</div>;
    return <Component {...props} />;
  };
}

const EnhancedComponent = withLoading(MyComponent);
```

**57. ¿Cuándo usar HOCs vs hooks vs render props?**
- **Hooks**: Preferidos para la mayoría de casos, composición más limpia
- **HOCs**: Para wrapping logic, cross-cutting concerns
- **Render props**: Cuando necesitas máxima flexibilidad en el render

**58. ¿Qué es error boundary?**
Componente que captura errores JavaScript en cualquier lugar del árbol de componentes hijo.

```javascript
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.log('Error caught:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return <h1>Something went wrong.</h1>;
    }
    return this.props.children;
  }
}
```

**59. ¿Qué errores NO capturan los error boundaries?**
- Event handlers
- Asynchronous code (setTimeout, promises)
- Server-side rendering
- Errores en el propio error boundary

**60. ¿Cómo implementar error boundaries con hooks?**
No hay equivalente directo, pero puedes usar libraries como react-error-boundary o crear custom hooks con try/catch para casos específicos.

### **State Management (15 preguntas)**

**61. ¿Qué es el Context API?**
Mecanismo para pasar datos a través del árbol de componentes sin tener que pasar props manualmente en cada nivel.

```javascript
const ThemeContext = React.createContext('light');

function App() {
  return (
    <ThemeContext.Provider value="dark">
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  return <ThemedButton />;
}

function ThemedButton() {
  const theme = useContext(ThemeContext);
  return <button className={theme}>Themed Button</button>;
}
```

**62. ¿Cuándo usar Context API?**
- Datos que necesitan muchos componentes (theme, auth, language)
- Evitar prop drilling
- No para datos que cambian frecuentemente (puede causar re-renders)

**63. ¿Cuáles son los problemas del Context API?**
- Re-renders de todos los consumers cuando cambia el value
- Dificulta optimizaciones
- No tiene time-travel debugging como Redux

**64. ¿Cómo optimizar Context para evitar re-renders?**
- Dividir contexts (separar datos que cambian frecuentemente)
- Memorizar el value con useMemo
- Usar React.memo en consumers

```javascript
const value = useMemo(() => ({
  user,
  login,
  logout
}), [user]);

<AuthContext.Provider value={value}>
```

**65. ¿Qué es Redux y por qué usarlo?**
Library de state management predecible para aplicaciones JavaScript. Beneficios:
- Single source of truth
- State inmutable
- Time-travel debugging
- Middleware ecosystem

**66. ¿Cuáles son los principios de Redux?**
- Single source of truth (store único)
- State is read-only (solo se modifica via actions)
- Changes are made with pure functions (reducers)

**67. ¿Qué son las actions en Redux?**
Objetos planos que describen qué pasó en la aplicación. Tienen un tipo y opcionalmente payload.

```javascript
const addTodo = (text) => ({
  type: 'ADD_TODO',
  payload: {
    id: Date.now(),
    text,
    completed: false
  }
});
```

**68. ¿Qué son los reducers?**
Funciones puras que toman el state actual y una action, y retornan un nuevo state.

```javascript
function todosReducer(state = [], action) {
  switch (action.type) {
    case 'ADD_TODO':
      return [...state, action.payload];
    case 'TOGGLE_TODO':
      return state.map(todo =>
        todo.id === action.payload.id
          ? { ...todo, completed: !todo.completed }
          : todo
      );
    default:
      return state;
  }
}
```

**69. ¿Qué es Redux Toolkit?**
Set oficial de herramientas para uso eficiente de Redux que incluye:
- configureStore
- createSlice
- createAsyncThunk
- Immer para immutabilidad

**70. ¿Cómo manejas async actions en Redux?**
- Redux Thunk: permite action creators que retornan funciones
- Redux Saga: usa generators para efectos side
- createAsyncThunk de Redux Toolkit

```javascript
const fetchUser = createAsyncThunk(
  'users/fetchById',
  async (userId) => {
    const response = await api.fetchUser(userId);
    return response.data;
  }
);
```

**71. ¿Qué es middleware en Redux?**
Funciones que se ejecutan entre dispatching una action y el momento que llega al reducer.

**72. ¿Cuáles son alternativas modernas a Redux?**
- Zustand: Simple y lightweight
- Jotai: Atomic state management
- Valtio: Proxy-based state
- SWR/React Query: Para server state

**73. ¿Qué es server state vs client state?**
- **Server state**: Datos del servidor (async, shared, cached)
- **Client state**: UI state local del cliente (sync, private)

**74. ¿Cómo manejar server state en React?**
- React Query (TanStack Query)
- SWR
- Apollo Client (GraphQL)
- Custom hooks con fetch

**75. ¿Qué es React Query?**
Library para fetching, caching, synchronizing y updating server state.

```javascript
function Profile() {
  const { data, isLoading, error } = useQuery(
    ['profile'],
    fetchProfile
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <div>Welcome {data.name}</div>;
}
```

### **Testing (10 preguntas)**

**76. ¿Cómo testeas componentes React?**
- React Testing Library (recomendado)
- Enzyme (legacy)
- Jest para unit tests
- Cypress/Playwright para E2E

**77. ¿Qué es React Testing Library?**
Library que proporciona utilidades para testear componentes React enfocándose en cómo el usuario interactúa con la aplicación.

```javascript
import { render, screen, fireEvent } from '@testing-library/react';

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
```

**78. ¿Cuáles son las filosofías de testing?**
- Test behavior, not implementation
- Test from the user's perspective
- Write tests that give confidence

**79. ¿Cómo testeas hooks?**
- @testing-library/react-hooks
- Testear hooks dentro de componentes
- Custom render helpers

```javascript
import { renderHook, act } from '@testing-library/react-hooks';

test('should increment counter', () => {
  const { result } = renderHook(() => useCounter());
  
  act(() => {
    result.current.increment();
  });
  
  expect(result.current.count).toBe(1);
});
```

**80. ¿Cómo testeas componentes con Context?**
Crear custom render que incluya providers:

```javascript
const CustomProvider = ({ children }) => (
  <ThemeProvider value="dark">
    <AuthProvider>
      {children}
    </AuthProvider>
  </ThemeProvider>
);

const renderWithProviders = (ui) => {
  return render(ui, { wrapper: CustomProvider });
};
```

**81. ¿Cómo mockeas API calls en tests?**
- Jest mocks
- Mock Service Worker (MSW)
- Axios mock adapter

**82. ¿Qué son snapshot tests?**
Tests que capturan el output renderizado de un componente y lo comparan con snapshots guardados.

**83. ¿Cuáles son las mejores prácticas de testing?**
- Test user behavior, not implementation details
- Use meaningful test descriptions
- Arrange-Act-Assert pattern
- Mock external dependencies
- Test error states

**84. ¿Cómo testeas componentes async?**
```javascript
test('loads and displays greeting', async () => {
  render(<Greeting />);
  
  const greeting = await screen.findByText(/hello/i);
  expect(greeting).toBeInTheDocument();
});
```

**85. ¿Qué es el patrón AAA en testing?**
- **Arrange**: Configurar el test (render componente, setup mocks)
- **Act**: Ejecutar la acción (click, type, etc.)
- **Assert**: Verificar el resultado

### **Advanced React (15 preguntas)**

**86. ¿Qué es Server-Side Rendering (SSR)?**
Técnica donde el HTML se genera en el servidor en lugar del cliente, mejorando SEO y performance inicial.

**87. ¿Cuáles son los beneficios de SSR?**
- Mejor SEO
- Faster first contentful paint
- Mejor experiencia en conexiones lentas
- Social media sharing (meta tags)

**88. ¿Qué es Static Site Generation (SSG)?**
Generar páginas HTML en build time en lugar de request time. Más rápido que SSR para contenido que no cambia frecuentemente.

**89. ¿Cuál es la diferencia entre SSR, SSG y CSR?**
- **SSR**: Renderizado en servidor por request
- **SSG**: Generado en build time
- **CSR**: Renderizado en cliente

**90. ¿Qué es hydration?**
Proceso donde React toma el HTML renderizado por el servidor y lo convierte en una aplicación React interactiva.

**91. ¿Qué son los React Server Components?**
Componentes que se ejecutan en el servidor y permiten:
- Acceso directo a backend
- Bundle size más pequeño
- Mejor performance

**92. ¿Qué es Concurrent Mode?**
Conjunto de características que ayudan a que las aplicaciones React se mantengan responsivas y se ajusten a la capacidad del dispositivo del usuario.

**93. ¿Qué es Time Slicing?**
Característica de Concurrent Mode que permite a React interrumpir el trabajo de renderizado para manejar tareas de alta prioridad.

**94. ¿Qué son las transiciones en React?**
Forma de marcar actualizaciones como no urgentes, permitiendo que React las interrumpa para manejar actualizaciones más urgentes.

```javascript
import { startTransition } from 'react';

function handleClick() {
  // Urgent update
  setInputValue(value);
  
  // Non-urgent update
  startTransition(() => {
    setSearchResults(results);
  });
}
```

**95. ¿Qué es useTransition?**
Hook que permite marcar actualizaciones como transiciones no urgentes.

```javascript
function SearchBox() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();
  
  const handleChange = (e) => {
    setQuery(e.target.value);
    startTransition(() => {
      setResults(search(e.target.value));
    });
  };
  
  return (
    <div>
      <input 
        value={query} 
        onChange={handleChange}
        placeholder="Search..."
      />
      {isPending && <div>Searching...</div>}
      <ul>
        {results.map(result => (
          <li key={result.id}>{result.name}</li>
        ))}
      </ul>
    </div>
  );
}
```

**96. ¿Qué es useDeferredValue?**
Hook que permite defer updates a valores que no son críticos, similar a debouncing.

```javascript
function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  const results = useMemo(() => 
    search(deferredQuery), [deferredQuery]
  );
  
  return (
    <div>
      {results.map(result => (
        <div key={result.id}>{result.name}</div>
      ))}
    </div>
  );
}
```

**97. ¿Qué es React.forwardRef?**
Función que permite a un componente pasar una ref a uno de sus componentes hijo.

```javascript
const FancyButton = React.forwardRef((props, ref) => (
  <button ref={ref} className="fancy-button">
    {props.children}
  </button>
));

// Uso
function App() {
  const ref = useRef();
  return <FancyButton ref={ref}>Click me!</FancyButton>;
}
```

**98. ¿Qué son los portals en React?**
Forma de renderizar componentes hijo en un nodo DOM que existe fuera de la jerarquía del componente padre.

```javascript
import ReactDOM from 'react-dom';

function Modal({ children }) {
  return ReactDOM.createPortal(
    <div className="modal">
      {children}
    </div>,
    document.getElementById('modal-root')
  );
}
```

**99. ¿Cuándo usar portals?**
- Modals y overlays
- Tooltips
- Dropdowns
- Notifications
- Cualquier UI que necesite "escapar" del contenedor padre

**100. ¿Cuáles son las mejores prácticas en React?**
- **Componentes pequeños y enfocados**: Single responsibility
- **Composición sobre herencia**: Usa composition patterns
- **Props drilling**: Evitar con Context o state management
- **Performance**: Usa React.memo, useMemo, useCallback cuando sea necesario
- **Naming**: Nombres descriptivos para componentes y props
- **Error boundaries**: Maneja errores graciosamente
- **Testing**: Testa comportamiento del usuario, no implementación
- **Accessibility**: Usa semantic HTML, ARIA attributes
- **File structure**: Organiza por features/domains
- **Code splitting**: Usa React.lazy para componentes grandes
- **State management**: Local state primero, luego global si es necesario
- **Custom hooks**: Extrae lógica reutilizable
- **TypeScript**: Para mejor developer experience y menos bugs

---

## **Consejos para Entrevistas**

### **Preguntas de JavaScript que debes dominar:**
1. **Event Loop y Asincronía**: Cómo funciona, promises vs callbacks
2. **Closures**: Qué son, casos de uso prácticos
3. **Prototypes**: Herencia prototípica, diferencia con clases
4. **this binding**: Contextos diferentes, call/apply/bind
5. **Hoisting**: var vs let/const, function declarations
6. **ES6+ features**: Destructuring, spread/rest, arrow functions
7. **Async/await vs Promises**: Cuándo usar cada uno
8. **Array methods**: map, filter, reduce y cuándo usar cada uno

### **Preguntas de React que debes dominar:**
1. **Virtual DOM**: Cómo funciona, por qué es útil
2. **Hooks**: useState, useEffect, useContext, custom hooks
3. **Performance**: React.memo, useMemo, useCallback
4. **State management**: Context API, cuándo usar Redux
5. **Component lifecycle**: Con hooks y clases
6. **Testing**: React Testing Library, mejores prácticas
7. **Error handling**: Error boundaries, manejo de errores async
8. **Modern features**: Suspense, Concurrent features

### **Durante la entrevista:**
- **Explica tu proceso de pensamiento** en voz alta
- **Haz preguntas clarificadoras** sobre los requisitos
- **Considera edge cases** y menciona limitaciones
- **Habla sobre performance** cuando sea relevante
- **Menciona testing** si es apropiado
- **Relaciona con experiencia real** cuando sea posible

### **Ejemplo de respuesta completa:**
**Pregunta**: "¿Cómo optimizarías un componente que se renderiza frecuentemente?"

**Respuesta estructurada**:
1. **Identifica la causa**: "Primero usaría React DevTools Profiler para identificar por qué se re-renderiza"
2. **Soluciones técnicas**: "Dependiendo del caso, usaría React.memo si las props no cambian, useMemo para valores computados costosos, useCallback para funciones que se pasan como props"
3. **Consideraciones adicionales**: "También verificaría si el componente padre está pasando objetos/arrays inline, y consideraría dividir el state si es muy complejo"
4. **Experiencia real**: "En mi último proyecto, tuve un componente de tabla que se renderizaba constantemente, y lo optimicé implementando virtualization con react-window"
5. **Trade-offs**: "Es importante balancear la optimización con la complejidad del código - no todas las optimizaciones valen la pena"

Esta estructura muestra conocimiento técnico profundo, experiencia práctica, y pensamiento crítico sobre trade-offs - exactamente lo que buscan los entrevistadores.

**Recuerda**: La práctica hace la perfección. Implementa estos conceptos en proyectos reales, no solo los memorices para la entrevista.
  