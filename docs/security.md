# Seguridad y Protección de Datos

## 1. Análisis de los datos usados
En esta prueba técnica se consumen datos de un portal público (Spaceflight News API).

Estos datos **Contiene información personal sensible** unicamente en los nombres de los autores, ya que son nombres reales. Por otra parte, no hay mas datos sensibles como direcciones, correos electrónicos ni identificadores únicos de ciudadanos.

La mayoría son información pública de carácter científico/técnico (NASA).  

---

## 2. Riesgos detectados
Se identifican posibles riesgos:

1. **Exposición innecesaria de endpoints de actualización**  
   - Si no se protege, cualquiera podría reejecutar el ETL y alterar la base.  

2. **Inyección de consultas / abuso de la API**  
   - El endpoint de búsqueda (`/search?q=`) podría ser vulnerable si se usara SQL sin validación.  
   - Posible uso abusivo (muchas requests en poco tiempo).  

3. **Datos futuros**  
   - Si en una versión real se integraran fuentes con información personal (p. ej. registros médicos, datos ciudadanos), existiría riesgo de exposición de datos sensibles.  

---

## 3. Medidas de mitigación
1. **Protección de endpoints sensibles**  
   - El endpoint `/update` ya se protegió con **token simple / autenticación básica / API Key**.  
   - Para un entorno real: usar JWT o OAuth2.  

2. **Anonimización (si hubiera datos sensibles)**  
   - En caso de incluir usuarios reales, se podrían anonimizar nombres, correos y ubicaciones específicas.  

3. **Seguridad de la base de datos**  
   - No subir nunca `db_kitsune.db` al repositorio.  
   - Usar rutas relativas para evitar exposición fuera del entorno controlado.  

4. **HTTPS obligatorio**  
   - En un despliegue productivo, solo permitir tráfico encriptado (TLS).  

---