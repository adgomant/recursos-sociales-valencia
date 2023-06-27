# Recursos Sociales en Valencia
Nuestra página web es una plataforma diseñada para proporcionar ayuda a personas en situación vulnerable o que requieren asistencia especializada en la ciudad de Valencia. Nuestro objetivo es abordar una amplia gama de necesidades, atendiendo a personas de todas las edades y géneros. En nuestro sitio web, reunimos una amplia variedad de recursos y servicios disponibles en Valencia para brindar ayuda en áreas como adicciones, diversidad funcional, diversidad intelectual, diversidad física, diversidad sensorial, cooperación internacional, personas mayores, migrantes y desplazados, minorías étnicas, apoyo a la mujer, personas privadas de libertad, personas sin hogar y en general, a toda la población.

Todos los datos han sido obtenidos de la página [OpenData de Valencia](https://valencia.opendatasoft.com/explore/?sort=modified&refine.theme=Sociedad+y+Bienestar&disjunctive.features&disjunctive.modified&disjunctive.publisher&disjunctive.keyword&disjunctive.theme&disjunctive.language)  y del apartado de [Recursos Sociales](https://www.valencia.es/web/guest/val/infociutat/-/categories/37663) de la página Infociudad del ayuntamiento de Valencia.

## Acceso a la App
La aplicación final se ha desplegado en [Streamlit Cloud](https://streamlit.io/cloud) y se puede acceder a ella [en el siguiente enlace](https://recursos-sociales-valencia-1c8gxx11vnv.streamlit.app/).

# Funcionalidades Principales
## Buscador
El buscador es la herramienta principal de la aplicación. Permite a los usuarios introducir consultas relacionadas con los recursos sociales que necesitan. A través del uso de la tecnología de búsqueda de texto completo, se utilizan las capacidades de Whoosh, una biblioteca de búsqueda en Python, para realizar búsquedas rápidas y precisas en la base de datos de recursos sociales recopilada. Los resultados se devuelven al usuario, mostrando los recursos más relevantes para su consulta. Además, se utiliza la OpenAI API para generar recomendaciones de servicios sociales basadas en los documentos recopilados.

## Mapa Interactivo
La funcionalidad del mapa interactivo permite a los usuarios explorar los recursos sociales de Valencia visualmente. Se utiliza la biblioteca de visualización de mapas Folium para mostrar los diferentes centros, recursos y asociaciones en el mapa de la ciudad. Los usuarios pueden filtrar los recursos por código postal o tema, lo que les permite encontrar exactamente lo que están buscando. El mapa interactivo brinda una experiencia intuitiva y facilita la localización de recursos cercanos y relevantes.

# Herramientas Utilizadas
En el desarrollo de la aplicación de Recursos Sociales Valencia, se han utilizado las siguientes herramientas:

•	**Streamlit**: Una biblioteca de Python que permite crear interfaces web interactivas de manera rápida y sencilla.

•	**Folium**: Una biblioteca de visualización de mapas en Python utilizada para representar los recursos sociales en un mapa interactivo.

•	**Whoosh**: Una biblioteca de búsqueda en Python utilizada para implementar el motor de búsqueda de la aplicación, permitiendo indexar y buscar rápidamente en grandes cantidades de texto.

•	**OpenAI API**: Se integra la OpenAI API para generar recomendaciones de servicios sociales basadas en los documentos recopilados, mejorando la funcionalidad del buscador.

Estas herramientas han sido fundamentales para ofrecer una experiencia fluida y eficiente a los usuarios, permitiendo el acceso a la información y recursos sociales relevantes de manera intuitiva.
