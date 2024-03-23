# SEMI1_Practica2

**Integrantes del Proyecto:**

* **Jefferson Molina:** 201945242
* **Walther Andrée Corado Paiz:** 201313861
* **Xhunik Nikol Miguel Mutzutz:** 201900462

**Introducción:**

Este documento describe el proyecto de una aplicación web de almacenamiento de fotos que se mejorará mediante la integración de tecnologías de inteligencia artificial (IA). La aplicación ofrecerá una mejor experiencia de usuario con nuevas funcionalidades como un chatbot y un analizador de imágenes.


**Tecnologías a Implementar:**

* **Amazon Web Services (AWS):** Plataforma de servicios en la nube que ofrece potencia de cómputo, almacenamiento de bases de datos, entrega de contenido y otras funcionalidades.
* **Inteligencia Artificial (IA):** Tecnologías para el desarrollo de un chatbot y un analizador de imágenes.

**Funcionalidades:**

* **Almacenamiento de fotos:** La aplicación permitirá a los usuarios almacenar sus fotos en la nube.
* **Chatbot:** Un chatbot con IA estará disponible para ayudar a los usuarios con preguntas y tareas relacionadas con la aplicación.
* **Analizador de imágenes:** La aplicación utilizará IA para analizar las fotos almacenadas y ofrecer diferentes funcionalidades:
    * **Reconocimiento de objetos:** La aplicación podrá identificar objetos dentro de las fotos.
    * **Etiquetado automático:** La aplicación podrá etiquetar automáticamente las fotos con palabras clave relevantes.
    * **Búsqueda por imágenes:** Los usuarios podrán buscar fotos por contenido visual similar.

**Beneficios:**

* **Mejor experiencia de usuario:** La IA proporcionará una experiencia más intuitiva y personalizada para los usuarios.
* **Mayor eficiencia:** La automatización de tareas mediante IA permitirá a los usuarios ahorrar tiempo y esfuerzo.
* **Organización optimizada:** Las funcionalidades de IA facilitarán la organización y búsqueda de fotos.

**Requisitos:**

* **Servidor:** Se requiere un servidor con las capacidades para ejecutar las nuevas funcionalidades de IA. El lenguaje de programación del servidor queda a elección del equipo.
* **Tecnologías de IA:** Se seleccionarán las tecnologías de IA más adecuadas para el desarrollo del chatbot y el analizador de imágenes.

**Próximos Pasos:**

* **Diseño y desarrollo del chatbot:** Se definirá la personalidad, las capacidades y la interfaz del chatbot.
* **Desarrollo del analizador de imágenes:** Se implementarán los algoritmos de IA para el reconocimiento de objetos, etiquetado automático y búsqueda por imágenes.
* **Integración con AWS:** Se configurarán los servicios de AWS necesarios para la aplicación.
* **Pruebas y evaluación:** Se realizarán pruebas exhaustivas para asegurar la calidad y el buen funcionamiento de la aplicación.




## Índice

- [Backend](#backend)
- [Frontend](#frontend)
- [Base de Datos](#base-de-datos)
- [Api](#Api)

## Backend


**API para usuarios y fotos**

Este documento describe una API Flask que permite gestionar usuarios y fotos. Utiliza varios servicios de AWS como S3 para almacenamiento, Rekognition para reconocimiento facial y traducción para descripciones multilenguaje.

**Librerías utilizadas:**

* Flask: Framework para desarrollo de APIs web.
* Flask-CORS: Permite peticiones CORS (Cross-Origin Resource Sharing).
* pymysql: Librería para conexión a bases de datos MySQL.
* hashlib: Librería para generación de hash MD5.
* boto3: Librería para interactuar con servicios de AWS.
* dotenv: Permite cargar variables de entorno.

**Variables de entorno:**

* DB_HOST: Host de la base de datos.
* DB_USER: Usuario de la base de datos.
* DB_PASSWORD: Contraseña de la base de datos.
* DB_SCHEMA: Nombre del esquema de la base de datos.
* S3_BUCKET: Nombre del bucket de S3.
* S3_PUBLIC_ACCESS: Clave de acceso pública de S3.
* S3_SECRET_ACCESS: Clave de acceso secreta de S3.
* REKOGNITION_ACCESS_KEY: Clave de acceso de AWS Rekognition.
* REKOGNITION_SECRET_ACCESS: Clave de acceso secreta de AWS Rekognition.
* TRANSLATE_ACCESS_KEY: Clave de acceso de AWS Translate.
* TRANSLATE_SECRET_ACCESS: Clave de acceso secreta de AWS Translate.

**Funciones:**

* `get_db_connection` - Establece la conexión a la base de datos.
* `generate_md5` - Genera un hash MD5 a partir de una cadena de texto.

**Endpoints:**

**Registro de usuario (POST /usuarios/registro):**

Recibe un JSON con los siguientes campos:

* usuario: Nombre de usuario (nickname).
* nombre_completo: Nombre completo del usuario.
* password: Contraseña del usuario (en texto plano).
* photo_base64: Imagen de perfil del usuario codificada en base64.

Almacena la información del usuario en la base de datos y la imagen en S3.

**Login de usuario (POST /usuarios/login):**

Recibe un JSON con al menos uno de los siguientes campos:

* usuario: Nombre de usuario (nickname).
* password: Contraseña del usuario (en texto plano).
* photo_base64: Imagen de perfil del usuario codificada en base64.

Valida el usuario con contraseña o mediante reconocimiento facial con la imagen proporcionada.

**Obtener perfil de usuario (GET /usuarios/perfil/<username>):**

Obtiene la información del perfil de un usuario identificado por su nickname. Incluye la descripción generada por Rekognition a partir de la imagen de perfil.

**Subir foto (POST /fotos):**

Sube una foto a S3 y la registra en la base de datos junto con sus etiquetas obtenidas de Rekognition y su descripción. 

**Actualizar perfil de usuario (PUT /usuarios/perfil/<username>):**

Actualiza la información del perfil de un usuario, incluyendo la contraseña y la imagen de perfil (opcional).

**Obtener fotos de usuario (GET /fotos/<username>):**

Obtiene las fotos publicadas por un usuario identificado por su nickname. Incluye las etiquetas y la descripción traducida a varios idiomas.

**Extraer texto de imagen (POST /extract_text):**

Extrae el texto de una imagen codificada en base64 utilizando Rekognition.

**Ejecución de la aplicación:**

Para ejecutar la aplicación:

1. Configurar las variables de entorno con los valores adecuados.
2. Ejecutar el comando `python app.py`.

La aplicación correrá en el puerto 5000 y escuchará peticiones en la dirección http://0.0.0.0:5000.


## Frontend


El código proporcionado define un módulo de enrutamiento para una sección específica de tu aplicación Angular, probablemente relacionada con una función o área llamada "Dashboard". A continuación, se ofrece un desglose de lo que hace el código:

**1. Importaciones:**

* `NgModule` desde `@angular/core`: Este es un módulo central de Angular que proporciona decoradores y funcionalidades para construir aplicaciones Angular.
* `RouterModule` y `Routes` desde `@angular/router`: Estas importaciones son esenciales para definir rutas y permitir la navegación dentro de tu aplicación Angular.

**2. Definición de rutas:**

* Se define una matriz llamada `routes` para almacenar la configuración de la ruta.
* El objeto de configuración de la ruta tiene dos propiedades:
    * `path`: Esta propiedad especifica la ruta URL que activará esta ruta. En este caso, una ruta vacía (`''`) indica que esta ruta estará activa para la ruta base de la función (por ejemplo, http://localhost:4200/dashboard).
    * `component`: Esta propiedad define el componente que se cargará y mostrará cuando esta ruta esté activa. Aquí, se establece en `DashboardComponent`, probablemente el componente responsable de renderizar la vista del panel de control.

**3. Decorador NgModule:**

* Se utiliza `@NgModule` para definir un módulo Angular llamado `DashboardRoutingModule`. Este módulo tiene el propósito de enrutar dentro de la función "Dashboard".
    * `imports`: Esta propiedad especifica los módulos externos de los que depende este módulo. Aquí, importa `RouterModule.forChild(routes)`.
        * `RouterModule.forChild(routes)`: Esto crea una configuración de enrutamiento específica para este módulo de función. Toma la matriz `routes` definida anteriormente para configurar las rutas dentro de la función.
    * `exports`: Esta propiedad especifica qué módulos o componentes pueden acceder a las funcionalidades proporcionadas por este módulo. Aquí, exporta `RouterModule` para que las funcionalidades de enrutamiento estén disponibles para otros componentes dentro de la función "Dashboard".

En resumen, este código crea un módulo de enrutamiento (`DashboardRoutingModule`) que configura las rutas de navegación para la función "Dashboard" en tu aplicación Angular. Define una ruta para la ruta base de la función (http://localhost:4200/dashboard) que cargará y mostrará el `DashboardComponent`. Este módulo se puede importar a otros módulos dentro de la función "Dashboard" para habilitar la navegación entre diferentes vistas.

**Información adicional:**

* Este código es un ejemplo simple de un módulo de enrutamiento. Puedes encontrar más información sobre el enrutamiento en Angular en la documentación oficial: [https://angular.io/guide/router](https://angular.io/guide/router)
* El componente `DashboardComponent` no se incluye en este código. Deberás definir este componente por separado para renderizar la vista del panel de control.


## Componente LoginComponent en Angular

Este componente (`LoginComponent`) se encarga de gestionar el formulario de inicio de sesión de una aplicación Angular. A continuación se detalla su funcionalidad:

**1. Imports:**

* `Component` y `ViewChild` desde `@angular/core`: Estos decoradores son necesarios para definir componentes y acceder a elementos secundarios dentro de la plantilla.
* `ApiService` desde `../api.service`: Importa el servicio `ApiService` que presumiblemente se encarga de realizar peticiones a la API para tareas como el inicio de sesión.
* `WebcamComponent` desde `../shared/webcam/webcam.component`: Importa el componente `WebcamComponent` que se utiliza para capturar una imagen con la webcam del usuario.
* `Router` desde `@angular/router`: Importa el servicio `Router` para realizar navegaciones entre rutas dentro de la aplicación.

**2. Decorador Component:**

* `selector`: Define el nombre del selector del componente (`app-login`). Este selector se utiliza en la plantilla HTML para identificar dónde se debe insertar el componente.
* `templateUrl`: Define la ruta relativa a la plantilla HTML del componente (`./login.component.html`).
* `styleUrls`: Define la ruta relativa a la hoja de estilos del componente (`./login.component.scss`).

**3. Propiedades del Componente:**

* `@ViewChild(WebcamComponent) webcam!`: Utiliza el decorador `@ViewChild` para obtener una referencia al componente `WebcamComponent` presente dentro de la plantilla. El signo de exclamación (`!`) indica que estamos seguros de que el elemento estará disponible en la vista.
* `username`: Almacena el nombre de usuario ingresado en el formulario (string).
* `password`: Almacena la contraseña ingresada en el formulario (string).
* `photo`: Almacena la imagen capturada con la webcam en formato Base64 (string).

**4. Constructor:**

* Inyecta dependencias del servicio `ApiService` y `Router` para utilizar sus funcionalidades dentro del componente. 

**5. Métodos:**

* `handleCaptureImage(imageDataUrl: string)`: Se llama cuando el componente `WebcamComponent` emite el evento de captura de imagen. Este método recibe la imagen en formato Base64 y la almacena en la propiedad `photo`.
* `submit()`: Se ejecuta al enviar el formulario de inicio de sesión.
    * Toma una captura de imagen con la webcam utilizando el método `capture()` del componente `webcam`.
    * Llama al servicio `ApiService` utilizando el método `login` y le pasa un objeto con los datos del usuario (`username`, `password`, y `photo_base64`).
    * Se suscribe a la respuesta del observable del servicio `ApiService`.
      * En caso de éxito (`next`): Muestra un mensaje con la respuesta recibida de la API y navega a la ruta `/dashboard` incluyendo el nombre de usuario (`this.username`).
      * En caso de error (`error`): Muestra un mensaje con el error recibido de la API.

**Resumen:**

Este componente permite a los usuarios iniciar sesión en la aplicación. Solicita el nombre de usuario, contraseña y captura una imagen opcional con la webcam. Envía los datos del usuario al servicio `ApiService` para realizar el login y en base a la respuesta, muestra un mensaje y redirige a la ruta del dashboard.

**Componente RegisterComponent en Angular**

Este componente (`RegisterComponent`) se encarga de gestionar el formulario de registro de nuevos usuarios en una aplicación Angular. A continuación se describen sus principales características:

**1. Imports:**

* `Component` desde `@angular/core`: Decorador necesario para definir componentes en Angular.
* `ApiService` desde `../api.service`: Importa el servicio `ApiService`, el cual se utiliza para realizar peticiones a la API de la aplicación, como el registro de nuevos usuarios.

**2. Decorador Component:**

* `selector`: Define el nombre del selector del componente (`app-register`). Este selector se utiliza en las plantillas HTML para indicar dónde se debe incluir el componente.
* `templateUrl`: Especifica la ruta relativa al archivo HTML que contiene la plantilla del componente (`./register.component.html`).
* `styleUrls`: Indica la ruta relativa al archivo SCSS que contiene los estilos del componente (`./register.component.scss`).

**3. Propiedades del Componente:**

* `username`: Almacena el nombre de usuario ingresado en el formulario (string).
* `name`: Almacena el nombre completo del usuario ingresado en el formulario (string).
* `password`: Almacena la contraseña ingresada en el formulario (string).
* `photo`: Almacena la imagen capturada por webcam en formato Base64 (string).

**4. Constructor:**

* Inyecta dependencia del servicio `ApiService` para utilizar sus funcionalidades dentro del componente.

**5. Métodos:**

* `handleCaptureImage(imageDataUrl: string)`: Se llama cuando se captura una imagen utilizando la webcam. Recibe la imagen en formato Base64 y la almacena en la propiedad `photo`.
* `submit()`: Se ejecuta al enviar el formulario de registro.
    * Llama al método `register` del servicio `ApiService`, enviando un objeto con los datos del usuario (`usuario`, `nombre_completo`, `password`, y `photo_base64`).
    * Se suscribe a la respuesta del observable del servicio `ApiService`.
      * En caso de éxito (`next`): Muestra un mensaje con la respuesta recibida de la API.
      * En caso de error (`error`): Muestra un mensaje con el error recibido de la API.

**Resumen:**

Este componente permite a los usuarios registrarse en la aplicación. Captura datos como nombre de usuario, nombre completo, contraseña y una imagen opcional con la webcam. Envía los datos al servicio `ApiService` para realizar el registro y, en base a la respuesta, muestra un mensaje al usuario.

## Componente WebcamComponent en Angular

Este componente (`WebcamComponent`) proporciona funcionalidades para acceder a la cámara del usuario y capturar imágenes en una aplicación Angular. A continuación se detalla su funcionamiento:

**1. Imports:**

* Decoradores y funcionalidades de Angular:
    * `Component`: Define el componente.
    * `ElementRef`: Permite acceder a elementos del DOM desde la plantilla del componente.
    * `EventEmitter`: Facilita la comunicación con componentes padre mediante eventos personalizados.
    * `Input`: Define una propiedad para recibir datos desde el componente padre.
    * `Output`: Define un evento personalizado para emitir datos a componentes padre.
    * `ViewChild`: Permite acceder a elementos secundarios dentro de la plantilla del componente.
    * `OnDestroy`: Ciclo de vida del componente para realizar tareas de limpieza.
    * `AfterViewInit`: Ciclo de vida del componente para acciones después de la inicialización de la vista.

**2. Decorador Component:**

* `selector`: Define el nombre del selector del componente (`app-webcam`) para incluirlo en las plantillas HTML.
* `templateUrl`: Ruta relativa a la plantilla HTML del componente (`./webcam.component.html`).
* `styleUrls`: Ruta relativa a la hoja de estilos SCSS del componente (`./webcam.component.scss`).

**3. Propiedades de Entrada (Input):**

* `buttonVisible` (tipo boolean): Permite mostrar u ocultar el botón de captura de imagen a través del componente padre. Por defecto, está visible (`true`).

**4. Propiedades de Salida (Output):**

* `imageCaptured` (tipo `EventEmitter<string>`): Evento personalizado que emite una cadena con la imagen capturada en formato Base64.

**5. Propiedades del Componente:**

* `@ViewChild('videoElement') videoElement!`: Obtiene una referencia al elemento HTML `<video>` dentro de la plantilla usando `@ViewChild`.
* `video`: Almacena una referencia a la etiqueta HTMLVideoElement para manipular el elemento de video.
* `stream` (tipo `MediaStream`): Almacena opcionalmente el flujo de video de la cámara.

**6. Ciclo de Vida - AfterViewInit:**

* `ngAfterViewInit()`: Se ejecuta después de que la vista del componente se haya inicializado.
    * Asigna la referencia del elemento nativo de `videoElement` a la propiedad `video`.
    * Llama al método `initCamera` para inicializar la cámara.

**7. Método initCamera():**

* Verifica si el navegador soporta la API `navigator.mediaDevices.getUserMedia`.
* Solicita acceso a la cámara utilizando `navigator.mediaDevices.getUserMedia({ video: true })`.
    * En caso de éxito:
        * Almacena el flujo de video en la propiedad `stream`.
        * Asigna el flujo de video como fuente del elemento `<video>` (`video.srcObject`).
        * Reproduce el video utilizando `video.play()`.
    * En caso de error:
        * Muestra un mensaje de consola indicando el error.

**8. Método capture():**

* Se encarga de capturar una imagen de la cámara.
* Crea un elemento `<canvas>` para dibujar la imagen del video.
* Configura el tamaño del canvas (`canvas.width` y `canvas.height`) de acuerdo con el video.
* Obtiene el contexto 2D del canvas (`ctx`).
* Dibuja la imagen del video en el canvas utilizando `ctx.drawImage()`.
* Convierte el canvas a una cadena en formato Base64 utilizando `canvas.toDataURL('image/png')`.
* Extrae la parte relevante de la cadena Base64 dividiendo por la coma (`,`) y tomando el segundo elemento del arreglo.
* Emite el valor de la imagen Base64 a través del evento personalizado `imageCaptured`.

**9. Ciclo de Vida - OnDestroy:**

* `ngOnDestroy()`: Se ejecuta cuando el componente se va a destruir.
* Si existe un flujo de video activo (`stream`), detiene todas las pistas del flujo utilizando `stream.getTracks().forEach(track => track.stop())`. 

**Resumen:**

Este componente permite a los usuarios acceder a la cámara y capturar imágenes. Se comunica con el componente padre a través del evento personalizado `imageCaptured` para enviar la imagen Base64 capturada. El componente padre puede utilizar este valor para procesar la imagen o mostrarla en la interfaz.

## Base de Datos
Las instrucciones SQL proporcionadas crean un esquema de base de datos para administrar usuarios, fotos y las etiquetas asociadas a ellas. Aquí un desglose del código:

**1. Creación de la base de datos (si no existe):**

```sql
CREATE DATABASE IF NOT EXISTS FAUNADEX;
USE FAUNADEX;
```

Estas líneas crean una base de datos llamada `FAUNADEX` si aún no existe y luego le indican al servidor MySQL que use esa base de datos para las consultas posteriores.

**2. Creación de las tablas:**

El script luego define tres tablas: `Usuarios` (Usuarios), `Fotos` (Fotos) y `Etiquetas` (Etiquetas), y una cuarta tabla `FotoEtiquetas` (FotoEtiquetas) para la relación de muchos a muchos entre fotos y etiquetas.

* **Tabla Usuarios:**
    * `id`: Un entero auto-incrementable que identifica de manera única a cada usuario. (Clave Primaria)
    * `nickname`: Un valor de cadena que representa el apodo único del usuario (debe ser único).
    * `nombre`: Un valor de cadena que almacena el nombre completo del usuario.
    * `password`: Un valor de cadena que contiene la contraseña del usuario encriptada (posiblemente usando MD5 basado en el código anterior).
    * `rutaFotoPerfil`: Un valor de cadena que especifica la ruta relativa a la imagen de perfil del usuario almacenada en S3 (u otro sistema de almacenamiento).

* **Tabla Fotos:**
    * `id`: Un entero auto-incrementable que identifica de manera única a cada foto. (Clave Primaria)
    * `titulo`: Un valor de cadena que representa el título de la foto.
    * `descripcion`: Un valor de cadena que contiene una descripción de la foto.
    * `rutaFoto`: Un valor de cadena que especifica la ruta relativa a la foto almacenada en S3.
    * `usuarioId`: Un valor entero que hace referencia al usuario que subió la foto. Esto establece una relación de clave foránea con la tabla `Usuarios`, vinculando cada foto a su propietario.

* **Tabla Etiquetas:**
    * `id`: Un entero auto-incrementable que identifica de manera única a cada etiqueta. (Clave Primaria)
    * `etiqueta`: Un valor de cadena que representa la etiqueta en sí (debe ser única).

* **Tabla FotoEtiquetas:**
    * `fotoId`: Un valor entero que hace referencia al ID de la foto (clave foránea que referencia `Fotos.id`).
    * `etiquetaId`: Un valor entero que hace referencia al ID de la etiqueta (clave foránea que referencia `Etiquetas.id`).
    * Esta tabla establece una relación de muchos a muchos entre fotos y etiquetas. Una sola foto puede tener varias etiquetas y una sola etiqueta se puede asociar con varias fotos. La combinación de `fotoId` y `etiquetaId` forma la clave primaria compuesta para esta tabla.

En resumen, este diseño de esquema le permite almacenar información del usuario, sus fotos, descripciones y asociar etiquetas relevantes con cada foto.

## Api

## Servicio ApiService en Angular

Este servicio (`ApiService`) se encarga de realizar peticiones HTTP a la API backend de la aplicación Angular. Proporciona métodos para interactuar con distintas funcionalidades de la API relacionadas con usuarios, fotos y extracción de texto.

**1. Imports:**

* `Injectable` desde `@angular/core`: Decorador para definir un servicio injectable en Angular.
* Interfaces personalizadas: Importa las interfaces creadas para definir la estructura de los datos que se envían y reciben de la API (por ejemplo, `IRegistroRequest`, `IMessageResponse`, etc.).
* `HttpClient` desde `@angular/common/http`: Cliente HTTP para realizar peticiones a la API.
* `Observable` desde 'rxjs': Clase utilizada para manejar flujos de datos asíncronos (observables).

**2. Decorador Injectable:**

* `providedIn: 'root'`: Define que esta clase es un servicio proporcionado a nivel raíz de la aplicación. Esto significa que una única instancia del servicio estará disponible para toda la aplicación.

**3. Propiedades:**

* `baseUrl`: Almacena la URL base de la API (`http://3.88.203.126:5000`).

**4. Constructor:**

* Inyecta la dependencia de `HttpClient` para realizar las peticiones HTTP.

**5. Métodos del Servicio:**

* `register(request: IRegistroRequest)`: Realiza una petición POST a la API para registrar un nuevo usuario. Recibe un objeto de tipo `IRegistroRequest` que contiene los datos del usuario y retorna un observable `IMessageResponse` con la respuesta de la API.
* `login(request: ILoginRequest)`: Realiza una petición POST a la API para iniciar sesión. Recibe un objeto de tipo `ILoginRequest` con los credenciales del usuario y retorna un observable `IMessageResponse` con la respuesta de la API.
* `getProfile(username: string)`: Realiza una petición GET a la API para obtener el perfil de un usuario. Recibe el nombre de usuario (`username`) como parámetro y retorna un observable `IMessageResponse | IGetProfileResponse`. La respuesta puede ser un mensaje de error (`IMessageResponse`) o la información del perfil del usuario (`IGetProfileResponse`).
* `uploadPhoto(request: IUploadPhotoRequest)`: Realiza una petición POST a la API para subir una foto de perfil. Recibe un objeto de tipo `IUploadPhotoRequest` con los datos de la foto y retorna un observable `IMessageResponse` con la respuesta de la API.
* `updateProfile(request: IUpdateProfileRequest, username: string)`: Realiza una petición PUT a la API para actualizar el perfil de un usuario. Recibe dos parámetros: el objeto con los datos actualizados (`IUpdateProfileRequest`) y el nombre de usuario (`username`) y retorna un observable `IMessageResponse` con la respuesta de la API.
* `getPhotos(username: string)`: Realiza una petición GET a la API para obtener las fotos de un usuario. Recibe el nombre de usuario (`username`) como parámetro y retorna un observable de tipo `Array<IGetPhotosResponse>` que contiene un arreglo con las respuestas de las fotos.
* `extractText(request: IExtractTextRequest)`: Realiza una petición POST a la API para extraer texto de una imagen. Recibe un objeto de tipo `IExtractTextRequest` con la imagen en formato Base64 y retorna un observable `IMessageResponse | IExtractTextResponse`. La respuesta puede ser un mensaje de error (`IMessageResponse`) o el texto extraído de la imagen (`IExtractTextResponse`).

**Resumen:**

Este servicio centraliza las peticiones HTTP a la API, permitiendo a otros componentes de la aplicación interactuar con las funcionalidades del backend de forma desacoplada. Utiliza interfaces para definir los datos que se manejan, mejorando la legibilidad y mantenibilidad del código.