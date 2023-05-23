# Actividad 4 
Ejemplo headers TCP: Para esta actividad debe definir una estructura para sus headers. Una forma de definir sus headers (sin usar directamente bytes) es la siguiente.

[SYN]|||[ACK]|||[FIN]|||[SEQ]|||[DATOS]

Aquí los datos necesarios del header se encuentran definidos con strings divididos por una secuencia "|||". Las variables [SYN], [ACK] y [FIN] corresponden a flags cuyo valor es 0 en caso de no estar siendo utilizadas, y en 1 en caso de ser utilizadas. La variable [SEQ] corresponde al número de secuencia. De esta forma un mensaje SYN-ACK se podría ver como:

 SYN-ACK -> 1|||1|||0|||8|||

Mientras que una secuencia de datos con su respectivo ACK podría verse como:

 Datos   -> 0|||0|||0|||98|||Mensaje de prueba

 ACK     -> 0|||1|||0|||115|||

