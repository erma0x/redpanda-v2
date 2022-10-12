# MODEL 
    LOGIC                       A > B
    EQUATIONS                   A : X+1
    NORMALIZATION               A : N1
    PERFORMANCE                 
        SHAPE_RATEO
        ALPHA
        BETA

    MUTATED : TRUE
    TAKE_PROFITS
    STOP_LOSSES


# TIPI DI MUTAZIONI
1. logic
2. equations
3. normalization methods
4. TP / SL



1. LOGIC

prendi un elemento a caso della logica e lo sostituisci con un altro

    A > B   ->   A > C

OPPURE

cambia a caso i simboli delle disequazioni

    A > B   ->   A < B


2. EQUATIONS
modifica poco l'equazione prendendo una qualsiasi cifra e cambiala con un altra cifra

A : X + 1 -> A : X + 9

modifica molto l'equazione rigenerandola da zero.

A : X + 1 -> A: generate_math() -> A : X**3


3. NORMALIZATION METHOD
scegli un altro metodo di normalizzazione fra quelli disponibili

A : n1 -> A : n3


4.  TP / SL
modifica di poco aggiungendo un valore casuale compreso in una normale con media TP
e con SD pari a TP/10


TP : 0.05 ->  TP : np.normal(mean = TP, sd = TP/10 ,  n = 1)


4. scambio di LONG SHORT

A) LONG     ->   SHORT