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


# TIPI DI CROSS OVER
1. scambia logica
2. scambia logic + equations + normalization methods
3. scambia SHORT e LONG
4. scambia TP / SL


1. LOGICA
 
A > B  ->    A > D 
C > D  ->    B > C

scambiando anche le relative equazioni e metodi di normalizzazione


2. scambio del modello
scambia tutto in maniera intera : Logica + math + normalization methods
unica cosa che rimane quindi del modello è il type (LONG SHORT) ed i valori di TP/SL


k1 = (A>B)  A: x*2, B: x**3   A: n2, B: n3  
k2 = (C>D)  C: x, D: x+3      C: n4, D: n5  

k1 = (C>D)  C: x, D: x+3      C: n4, D: n5  
k2 = (A>B) A: x*2, B: x**3    A: n2, B: n3  


3. scambio di long or short

A) LONG           SHORT
B) SHORT          LONG

4. scambio di take profit o stop loss

A) TP : 0.005           -> TP : 0.01
B) TP : 0.01           -> TP : 0.005
