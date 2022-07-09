# hangman_solver_spanish

A little python utility to solve hangman game in spanish (it would also work with english words but needs some adaptations and a file with english words)

It uses an adaptation of the Wordle solver by 3blue1brown shown [here](https://www.youtube.com/watch?v=v68zYyaEmEA)

## --------------------------------- Español --------------------------------------

La interfaz es bastante sencilla y algo mediocre la verdad, pero funciona.

Solo tiene que ejecutarse el archivo main.py en la misma ubicación que el achivo CREA_procesado2 (archivo tomado del github de @dadosdelaplace [aquí](https://github.com/dadosdelaplace/blog-R-repo) )

## ----------------------------------- Uso ---------------------------------------

Al ejecutarse el archivo main en la terminal, inicia pidiendo el número de letras de la palabra a adivinar (Por el momento solo funciona con 15 letras o menos ya que requiere algo de preprocesamiento para cada tamaño de palabra (por eso el archivo puntuaciones2a15.json)

Después, muestra las 4 letras que en teoría dan más información y las primeras 5 palabras que coincidan con la información obtenida hasta ahora.

Se pide que se elija una letra y después la información obtenida de esa letra. Ejemplo (palabra de 8 letras):
  Letra elegida:  
  \> l  
  Expresión:  
  \> a....ll.        
  \# Se escribe un punto en los lugares de los que no se tiene información  
  
En caso de haberse equivocado, si escribe \_reg_ en "Expresión > " le dejará volver a escribir la letra y la expresión. 

Dsepués de esto se mostrarán las letras que más información dan usando el método de 3b1b mostrado al principio (u, r, e, b) y se mostrarán las palabras que coinciden con la expresión (argüello, arguello, arquillo, azotillo) y se vuelve a repetir.

Si una palabra no tiene x letra, solo se vuelve a escribir la expresión "......." o "a....so" para eliminar las palabras que contengan esa letra.

### En caso de obtener ZeroDivisionError

Quiere decir que la palabra no se encuentra e el archivo CREA (Esto puede ser porque la palabra no existe o porque está mal escrita la expresión)
