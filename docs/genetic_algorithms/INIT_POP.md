
alla fine dell'inizializzazione della popolazione, le successive generazioni dipendono dalla prima.
Gli individui nel tempo possono mutare in diversi modi. Queste mutazioni se avvenute vengono segnate con un POPULATION[i]['mutated'] == True
Ed alla fine per la selezione devono essere ricalcolati tutti i fitness di tutti i modelli che sono stati modificati cosi da avere performance
realistiche.


for i in POPULATION:
    if POPULATION[i]['mutated'] == True:
        POPULATION[i][-1] = backtest(POPULATION[i][-1])
        POPULATION[i][-1]['mutated'] = False

