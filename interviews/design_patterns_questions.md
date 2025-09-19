# 50 Preguntas sobre Patrones de Diseño - SOLID y Design Patterns

## **Principios SOLID**

Los principios SOLID son cinco principios fundamentales de la programación orientada a objetos que ayudan a crear software más mantenible, flexible y escalable.

### **S - Single Responsibility Principle (SRP)**
Una clase debe tener una sola razón para cambiar, es decir, debe tener una sola responsabilidad.

### **O - Open/Closed Principle (OCP)**
Las entidades de software deben estar abiertas para extensión pero cerradas para modificación.

### **L - Liskov Substitution Principle (LSP)**
Los objetos de una superclase deben ser reemplazables por objetos de sus subclases sin alterar la funcionalidad del programa.

### **I - Interface Segregation Principle (ISP)**
Los clientes no deben depender de interfaces que no usan. Es mejor tener muchas interfaces específicas que una interfaz general.

### **D - Dependency Inversion Principle (DIP)**
Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

---

## **Preguntas sobre Principios SOLID (15 preguntas)**

**1. ¿Qué significa el Single Responsibility Principle y por qué es importante?**
El SRP establece que una clase debe tener una sola razón para cambiar. Es importante porque reduce el acoplamiento, hace el código más fácil de entender y mantener, y facilita las pruebas unitarias. Una clase que hace demasiadas cosas es difícil de modificar sin romper otras funcionalidades.

**2. Da un ejemplo de violación del SRP.**
```javascript
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
  
  // Violación: responsabilidad de validación
  validateEmail() {
    return this.email.includes('@');
  }
  
  // Violación: responsabilidad de persistencia
  saveToDatabase() {
    // código para guardar en BD
  }
  
  // Violación: responsabilidad de notificación
  sendWelcomeEmail() {
    // código para enviar email
  }
}
```

**3. ¿Cómo refactorizarías el ejemplo anterior siguiendo SRP?**
```javascript
class User {
  constructor(name, email) {
    this.name = name;
    this.email = email;
  }
}

class EmailValidator {
  static validate(email) {
    return email.includes('@');
  }
}

class UserRepository {
  save(user) {
    // código para guardar en BD
  }
}

class EmailService {
  sendWelcomeEmail(user) {
    // código para enviar email
  }
}
```

**4. ¿Qué significa el Open/Closed Principle?**
Las clases deben estar abiertas para extensión pero cerradas para modificación. Esto significa que podemos agregar nueva funcionalidad sin cambiar el código existente, típicamente usando herencia, composición o interfaces.

**5. Da un ejemplo del Open/Closed Principle.**
```javascript
// Cerrado para modificación, abierto para extensión
class Shape {
  area() {
    throw new Error('Must implement area method');
  }
}

class Rectangle extends Shape {
  constructor(width, height) {
    super();
    this.width = width;
    this.height = height;
  }
  
  area() {
    return this.width * this.height;
  }
}

class Circle extends Shape {
  constructor(radius) {
    super();
    this.radius = radius;
  }
  
  area() {
    return Math.PI * this.radius * this.radius;
  }
}

class AreaCalculator {
  calculate(shapes) {
    return shapes.reduce((total, shape) => total + shape.area(), 0);
  }
}
```

**6. ¿Qué es el Liskov Substitution Principle?**
Los objetos de una clase base deben poder ser reemplazados por objetos de sus clases derivadas sin alterar el comportamiento correcto del programa. Las subclases deben cumplir el contrato establecido por la clase padre.

**7. Da un ejemplo de violación del LSP.**
```javascript
class Bird {
  fly() {
    console.log('Flying');
  }
}

class Duck extends Bird {
  fly() {
    console.log('Duck flying');
  }
}

// Violación del LSP
class Penguin extends Bird {
  fly() {
    throw new Error('Penguins cannot fly!');
  }
}

function makeBirdFly(bird) {
  bird.fly(); // Falla con Penguin
}
```

**8. ¿Cómo solucionarías la violación del LSP del ejemplo anterior?**
```javascript
class Bird {
  constructor(name) {
    this.name = name;
  }
}

class FlyingBird extends Bird {
  fly() {
    console.log(`${this.name} is flying`);
  }
}

class Duck extends FlyingBird {
  constructor() {
    super('Duck');
  }
}

class Penguin extends Bird {
  constructor() {
    super('Penguin');
  }
  
  swim() {
    console.log('Penguin is swimming');
  }
}
```

**9. ¿Qué es el Interface Segregation Principle?**
Los clientes no deben ser forzados a depender de interfaces que no usan. Es mejor tener múltiples interfaces específicas que una interfaz monolítica. Esto reduce el acoplamiento y hace el código más flexible.

**10. Da un ejemplo del Interface Segregation Principle.**
```javascript
// Mal: interfaz monolítica
class Worker {
  work() {}
  eat() {}
  sleep() {}
}

// Bien: interfaces segregadas
class Workable {
  work() {
    throw new Error('Must implement work');
  }
}

class Eatable {
  eat() {
    throw new Error('Must implement eat');
  }
}

class Sleepable {
  sleep() {
    throw new Error('Must implement sleep');
  }
}

class Human extends Workable {
  work() { console.log('Human working'); }
}

class Robot extends Workable {
  work() { console.log('Robot working'); }
  // No necesita eat() ni sleep()
}
```

**11. ¿Qué es el Dependency Inversion Principle?**
Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones. Además, las abstracciones no deben depender de detalles; los detalles deben depender de abstracciones.

**12. Da un ejemplo de violación del DIP.**
```javascript
// Violación: clase de alto nivel depende de clase concreta
class MySQLDatabase {
  save(data) {
    console.log('Saving to MySQL');
  }
}

class UserService {
  constructor() {
    this.database = new MySQLDatabase(); // Dependencia directa
  }
  
  createUser(userData) {
    this.database.save(userData);
  }
}
```

**13. ¿Cómo aplicarías el DIP al ejemplo anterior?**
```javascript
// Abstracción
class Database {
  save(data) {
    throw new Error('Must implement save method');
  }
}

// Implementación concreta
class MySQLDatabase extends Database {
  save(data) {
    console.log('Saving to MySQL');
  }
}

class MongoDatabase extends Database {
  save(data) {
    console.log('Saving to MongoDB');
  }
}

// Clase de alto nivel depende de abstracción
class UserService {
  constructor(database) {
    this.database = database; // Inyección de dependencia
  }
  
  createUser(userData) {
    this.database.save(userData);
  }
}

// Uso
const userService = new UserService(new MySQLDatabase());
```

**14. ¿Cómo se relacionan los principios SOLID entre sí?**
Los principios SOLID trabajan juntos para crear código más mantenible:
- SRP hace que las clases sean cohesivas
- OCP permite extensibilidad sin modificar código existente
- LSP asegura que las jerarquías sean correctas
- ISP evita dependencias innecesarias
- DIP invierte las dependencias para mayor flexibilidad

**15. ¿Cuáles son los beneficios de aplicar los principios SOLID?**
- **Mantenibilidad**: Código más fácil de modificar y depurar
- **Extensibilidad**: Fácil agregar nuevas funcionalidades
- **Testabilidad**: Componentes más fáciles de probar unitariamente
- **Reutilización**: Componentes más reutilizables
- **Flexibilidad**: Mayor adaptabilidad a cambios de requisitos

---

## **Patrones Creacionales (10 preguntas)**

**16. ¿Qué es el patrón Singleton y cuándo lo usarías?**
El Singleton asegura que una clase tenga una sola instancia y proporciona acceso global a ella. Útil para: loggers, configuraciones, conexiones de BD, caches.

```javascript
class Singleton {
  constructor() {
    if (Singleton.instance) {
      return Singleton.instance;
    }
    Singleton.instance = this;
    return this;
  }
  
  static getInstance() {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}
```

**17. ¿Cuáles son los problemas del patrón Singleton?**
- Dificulta las pruebas unitarias (estado global)
- Viola el Single Responsibility Principle
- Puede crear problemas de concurrencia
- Hace el código más acoplado
- Considerado un anti-patrón por muchos developers

**18. ¿Qué es el patrón Factory Method?**
Crea objetos sin especificar la clase exacta. Define una interfaz para crear objetos, pero las subclases deciden qué clase instanciar.

```javascript
class Animal {
  speak() {
    throw new Error('Must implement speak');
  }
}

class Dog extends Animal {
  speak() {
    return 'Woof!';
  }
}

class Cat extends Animal {
  speak() {
    return 'Meow!';
  }
}

class AnimalFactory {
  static createAnimal(type) {
    switch(type) {
      case 'dog': return new Dog();
      case 'cat': return new Cat();
      default: throw new Error('Unknown animal type');
    }
  }
}
```

**19. ¿Qué es el patrón Abstract Factory?**
Proporciona una interfaz para crear familias de objetos relacionados sin especificar sus clases concretas.

```javascript
class GUIFactory {
  createButton() {}
  createCheckbox() {}
}

class WindowsFactory extends GUIFactory {
  createButton() {
    return new WindowsButton();
  }
  createCheckbox() {
    return new WindowsCheckbox();
  }
}

class MacFactory extends GUIFactory {
  createButton() {
    return new MacButton();
  }
  createCheckbox() {
    return new MacCheckbox();
  }
}
```

**20. ¿Qué es el patrón Builder?**
Construye objetos complejos paso a paso. Permite crear diferentes representaciones del mismo objeto usando el mismo proceso de construcción.

```javascript
class Pizza {
  constructor() {
    this.size = '';
    this.crust = '';
    this.toppings = [];
  }
}

class PizzaBuilder {
  constructor() {
    this.pizza = new Pizza();
  }
  
  setSize(size) {
    this.pizza.size = size;
    return this;
  }
  
  setCrust(crust) {
    this.pizza.crust = crust;
    return this;
  }
  
  addTopping(topping) {
    this.pizza.toppings.push(topping);
    return this;
  }
  
  build() {
    return this.pizza;
  }
}

// Uso
const pizza = new PizzaBuilder()
  .setSize('large')
  .setCrust('thin')
  .addTopping('pepperoni')
  .addTopping('cheese')
  .build();
```

**21. ¿Qué es el patrón Prototype?**
Crea objetos clonando una instancia existente en lugar de crear nuevas instancias desde cero.

```javascript
class Prototype {
  clone() {
    throw new Error('Must implement clone method');
  }
}

class ConcretePrototype extends Prototype {
  constructor(value) {
    super();
    this.value = value;
  }
  
  clone() {
    return new ConcretePrototype(this.value);
  }
}
```

**22. ¿Cuándo usarías Factory vs Builder vs Prototype?**
- **Factory**: Cuando necesitas crear objetos simples de diferentes tipos
- **Builder**: Para objetos complejos con muchos parámetros opcionales
- **Prototype**: Cuando clonar es más eficiente que crear desde cero

**23. ¿Qué ventajas tiene el patrón Builder?**
- Construcción paso a paso de objetos complejos
- Control fino sobre el proceso de construcción
- Permite diferentes representaciones del mismo objeto
- Código más legible con method chaining
- Validación durante la construcción

**24. ¿Cómo implementarías un Singleton thread-safe en Java?**
```java
public class Singleton {
    private static volatile Singleton instance;
    
    private Singleton() {}
    
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

**25. ¿Qué es el patrón Object Pool?**
Mantiene un conjunto de objetos reutilizables para evitar la creación/destrucción costosa. Útil para conexiones de BD, threads, objetos gráficos.

```javascript
class ObjectPool {
  constructor(createFn, resetFn, maxSize = 10) {
    this.createFn = createFn;
    this.resetFn = resetFn;
    this.maxSize = maxSize;
    this.pool = [];
    this.used = new Set();
  }
  
  acquire() {
    let obj;
    if (this.pool.length > 0) {
      obj = this.pool.pop();
    } else {
      obj = this.createFn();
    }
    this.used.add(obj);
    return obj;
  }
  
  release(obj) {
    if (this.used.has(obj)) {
      this.used.delete(obj);
      this.resetFn(obj);
      if (this.pool.length < this.maxSize) {
        this.pool.push(obj);
      }
    }
  }
}
```

---

## **Patrones Estructurales (10 preguntas)**

**26. ¿Qué es el patrón Adapter?**
Permite que clases con interfaces incompatibles trabajen juntas. Actúa como un wrapper que traduce las llamadas de una interfaz a otra.

```javascript
// Sistema existente
class OldPrinter {
  oldPrint(text) {
    console.log(`Old printer: ${text}`);
  }
}

// Nueva interfaz esperada
class PrinterAdapter {
  constructor(oldPrinter) {
    this.oldPrinter = oldPrinter;
  }
  
  print(text) {
    this.oldPrinter.oldPrint(text);
  }
}

// Uso
const oldPrinter = new OldPrinter();
const adapter = new PrinterAdapter(oldPrinter);
adapter.print('Hello World'); // Funciona con la nueva interfaz
```

**27. ¿Qué es el patrón Decorator?**
Añade nuevas funcionalidades a objetos dinámicamente sin alterar su estructura. Proporciona una alternativa flexible a la herencia.

```javascript
class Coffee {
  cost() {
    return 2;
  }
  
  description() {
    return 'Simple coffee';
  }
}

class MilkDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }
  
  cost() {
    return this.coffee.cost() + 0.5;
  }
  
  description() {
    return this.coffee.description() + ', milk';
  }
}

class SugarDecorator {
  constructor(coffee) {
    this.coffee = coffee;
  }
  
  cost() {
    return this.coffee.cost() + 0.2;
  }
  
  description() {
    return this.coffee.description() + ', sugar';
  }
}

// Uso
let coffee = new Coffee();
coffee = new MilkDecorator(coffee);
coffee = new SugarDecorator(coffee);
console.log(coffee.description()); // "Simple coffee, milk, sugar"
```

**28. ¿Qué es el patrón Facade?**
Proporciona una interfaz simplificada a un subsistema complejo. Oculta la complejidad del sistema y facilita su uso.

```javascript
class SubsystemA {
  operationA() {
    return 'SubsystemA operation';
  }
}

class SubsystemB {
  operationB() {
    return 'SubsystemB operation';
  }
}

class SubsystemC {
  operationC() {
    return 'SubsystemC operation';
  }
}

class Facade {
  constructor() {
    this.subsystemA = new SubsystemA();
    this.subsystemB = new SubsystemB();
    this.subsystemC = new SubsystemC();
  }
  
  simpleOperation() {
    const results = [];
    results.push(this.subsystemA.operationA());
    results.push(this.subsystemB.operationB());
    results.push(this.subsystemC.operationC());
    return results.join(' + ');
  }
}
```

**29. ¿Qué es el patrón Proxy?**
Proporciona un placeholder o sustituto para otro objeto para controlar el acceso a él. Útil para lazy loading, caching, logging, control de acceso.

```javascript
class RealSubject {
  request() {
    return 'RealSubject: Handling request';
  }
}

class Proxy {
  constructor(realSubject) {
    this.realSubject = realSubject;
  }
  
  request() {
    if (this.checkAccess()) {
      const result = this.realSubject.request();
      this.logAccess();
      return result;
    }
    return 'Access denied';
  }
  
  checkAccess() {
    console.log('Proxy: Checking access');
    return true;
  }
  
  logAccess() {
    console.log('Proxy: Logging request');
  }
}
```

**30. ¿Qué es el patrón Composite?**
Compone objetos en estructuras de árbol para representar jerarquías parte-todo. Permite tratar objetos individuales y composiciones de manera uniforme.

```javascript
class Component {
  add(component) {}
  remove(component) {}
  operation() {}
}

class Leaf extends Component {
  constructor(name) {
    super();
    this.name = name;
  }
  
  operation() {
    return this.name;
  }
}

class Composite extends Component {
  constructor(name) {
    super();
    this.name = name;
    this.children = [];
  }
  
  add(component) {
    this.children.push(component);
  }
  
  remove(component) {
    const index = this.children.indexOf(component);
    if (index > -1) {
      this.children.splice(index, 1);
    }
  }
  
  operation() {
    const results = [this.name];
    for (const child of this.children) {
      results.push(child.operation());
    }
    return results.join(' -> ');
  }
}
```

**31. ¿Cuándo usarías Adapter vs Facade?**
- **Adapter**: Cuando necesitas hacer que dos interfaces incompatibles trabajen juntas
- **Facade**: Cuando quieres simplificar el uso de un sistema complejo proporcionando una interfaz más simple

**32. ¿Qué es el patrón Bridge?**
Separa una abstracción de su implementación para que ambas puedan variar independientemente.

```javascript
class Abstraction {
  constructor(implementation) {
    this.implementation = implementation;
  }
  
  operation() {
    return this.implementation.operationImpl();
  }
}

class RefinedAbstraction extends Abstraction {
  operation() {
    return 'Refined: ' + this.implementation.operationImpl();
  }
}

class ConcreteImplementationA {
  operationImpl() {
    return 'Implementation A';
  }
}

class ConcreteImplementationB {
  operationImpl() {
    return 'Implementation B';
  }
}
```

**33. ¿Qué es el patrón Flyweight?**
Minimiza el uso de memoria compartiendo eficientemente grandes cantidades de objetos similares.

```javascript
class Flyweight {
  constructor(intrinsicState) {
    this.intrinsicState = intrinsicState;
  }
  
  operation(extrinsicState) {
    return `Intrinsic: ${this.intrinsicState}, Extrinsic: ${extrinsicState}`;
  }
}

class FlyweightFactory {
  constructor() {
    this.flyweights = new Map();
  }
  
  getFlyweight(intrinsicState) {
    if (!this.flyweights.has(intrinsicState)) {
      this.flyweights.set(intrinsicState, new Flyweight(intrinsicState));
    }
    return this.flyweights.get(intrinsicState);
  }
  
  getSize() {
    return this.flyweights.size;
  }
}
```

**34. ¿Cuáles son las diferencias entre Decorator y Proxy?**
- **Decorator**: Añade funcionalidades sin cambiar la interfaz, se enfoca en la extensión
- **Proxy**: Controla acceso y puede cambiar el comportamiento, se enfoca en el control

**35. ¿Cómo se relacionan los patrones estructurales con la composición vs herencia?**
Los patrones estructurales favorecen la composición sobre la herencia:
- Proporcionan mayor flexibilidad
- Permiten cambio de comportamiento en runtime
- Evitan jerarquías complejas de herencia
- Facilitan la reutilización de código

---

## **Patrones Comportamentales (15 preguntas)**

**36. ¿Qué es el patrón Observer?**
Define una dependencia uno-a-muchos entre objetos, de manera que cuando un objeto cambia su estado, todos sus dependientes son notificados automáticamente.

```javascript
class Subject {
  constructor() {
    this.observers = [];
  }
  
  attach(observer) {
    this.observers.push(observer);
  }
  
  detach(observer) {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
    }
  }
  
  notify() {
    this.observers.forEach(observer => observer.update(this));
  }
}

class ConcreteSubject extends Subject {
  constructor() {
    super();
    this.state = '';
  }
  
  getState() {
    return this.state;
  }
  
  setState(state) {
    this.state = state;
    this.notify();
  }
}

class Observer {
  update(subject) {
    console.log(`Observer updated with state: ${subject.getState()}`);
  }
}
```

**37. ¿Qué es el patrón Strategy?**
Define una familia de algoritmos, los encapsula y los hace intercambiables. Permite que el algoritmo varíe independientemente de los clientes que lo usan.

```javascript
class Strategy {
  execute(data) {
    throw new Error('Must implement execute method');
  }
}

class ConcreteStrategyA extends Strategy {
  execute(data) {
    return data.sort();
  }
}

class ConcreteStrategyB extends Strategy {
  execute(data) {
    return data.reverse();
  }
}

class Context {
  constructor(strategy) {
    this.strategy = strategy;
  }
  
  setStrategy(strategy) {
    this.strategy = strategy;
  }
  
  executeStrategy(data) {
    return this.strategy.execute(data);
  }
}

// Uso
const context = new Context(new ConcreteStrategyA());
console.log(context.executeStrategy([3, 1, 2])); // [1, 2, 3]
```

**38. ¿Qué es el patrón Command?**
Encapsula una petición como un objeto, permitiendo parametrizar clientes con diferentes peticiones, hacer cola de peticiones y soportar operaciones de deshacer.

```javascript
class Command {
  execute() {}
  undo() {}
}

class ConcreteCommand extends Command {
  constructor(receiver, action) {
    super();
    this.receiver = receiver;
    this.action = action;
  }
  
  execute() {
    this.receiver[this.action]();
  }
  
  undo() {
    // Lógica para deshacer
  }
}

class Receiver {
  action() {
    console.log('Action executed');
  }
}

class Invoker {
  constructor() {
    this.commands = [];
  }
  
  setCommand(command) {
    this.commands.push(command);
  }
  
  executeCommands() {
    this.commands.forEach(cmd => cmd.execute());
  }
}
```

**39. ¿Qué es el patrón State?**
Permite a un objeto alterar su comportamiento cuando su estado interno cambia. El objeto parecerá cambiar de clase.

```javascript
class State {
  handle(context) {}
}

class ConcreteStateA extends State {
  handle(context) {
    console.log('State A handling');
    context.setState(new ConcreteStateB());
  }
}

class ConcreteStateB extends State {
  handle(context) {
    console.log('State B handling');
    context.setState(new ConcreteStateA());
  }
}

class Context {
  constructor(state) {
    this.state = state;
  }
  
  setState(state) {
    this.state = state;
  }
  
  request() {
    this.state.handle(this);
  }
}
```

**40. ¿Qué es el patrón Template Method?**
Define el esqueleto de un algoritmo en una operación, dejando algunos pasos a las subclases. Permite redefinir ciertos pasos sin cambiar la estructura del algoritmo.

```javascript
class AbstractClass {
  templateMethod() {
    this.stepOne();
    this.stepTwo();
    this.stepThree();
  }
  
  stepOne() {
    console.log('AbstractClass: Step one');
  }
  
  stepTwo() {
    throw new Error('Must implement stepTwo');
  }
  
  stepThree() {
    console.log('AbstractClass: Step three');
  }
}

class ConcreteClass extends AbstractClass {
  stepTwo() {
    console.log('ConcreteClass: Step two');
  }
}
```

**41. ¿Cuándo usarías Strategy vs State?**
- **Strategy**: Cuando tienes diferentes formas de hacer lo mismo y quieres intercambiarlas
- **State**: Cuando el comportamiento de un objeto cambia completamente basado en su estado interno

**42. ¿Qué es el patrón Chain of Responsibility?**
Evita acoplar el emisor de una petición a su receptor dando a más de un objeto la posibilidad de responder a la petición.

```javascript
class Handler {
  setNext(handler) {
    this.nextHandler = handler;
    return handler;
  }
  
  handle(request) {
    if (this.nextHandler) {
      return this.nextHandler.handle(request);
    }
    return null;
  }
}

class ConcreteHandlerA extends Handler {
  handle(request) {
    if (request === 'A') {
      return `Handler A processed ${request}`;
    }
    return super.handle(request);
  }
}

class ConcreteHandlerB extends Handler {
  handle(request) {
    if (request === 'B') {
      return `Handler B processed ${request}`;
    }
    return super.handle(request);
  }
}

// Uso
const handlerA = new ConcreteHandlerA();
const handlerB = new ConcreteHandlerB();
handlerA.setNext(handlerB);
```

**43. ¿Qué es el patrón Mediator?**
Define cómo un conjunto de objetos interactúa entre sí. Promueve el acoplamiento débil evitando que los objetos se refieran explícitamente unos a otros.

```javascript
class Mediator {
  notify(sender, event) {}
}

class ConcreteMediator extends Mediator {
  constructor(component1, component2) {
    super();
    this.component1 = component1;
    this.component1.setMediator(this);
    this.component2 = component2;
    this.component2.setMediator(this);
  }
  
  notify(sender, event) {
    if (event === 'A') {
      this.component2.doC();
    }
    if (event === 'B') {
      this.component1.doD();
    }
  }
}

class Component {
  constructor() {
    this.mediator = null;
  }
  
  setMediator(mediator) {
    this.mediator = mediator;
  }
}
```

**44. ¿Qué es el patrón Visitor?**
Permite definir una nueva operación sin cambiar las clases de los elementos sobre los que opera. Separa el algoritmo de la estructura de datos.

```javascript
class Visitor {
  visitConcreteElementA(element) {}
  visitConcreteElementB(element) {}
}

class ConcreteVisitor extends Visitor {
  visitConcreteElementA(element) {
    console.log('Visiting ConcreteElementA');
  }
  
  visitConcreteElementB(element) {
    console.log('Visiting ConcreteElementB');
  