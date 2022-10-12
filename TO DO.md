# IN PROGRESS

[] aggiungi indicatori di pandas_ta
    su generator.py compute_financial_indexes()
    e su params.py available_indicators_dictionary

    testa gli indicatori con valori reali su tester.ipynb
    e scopri quanti, massimo e minimo dei parametri
    
    ed infine testali importandoli da random_indicators() su tester.ipynb

    tester.ipynb -> params.py -> generator.py -> tester.ipynb

[] 


# To Do

[] aggiungi derivate al generatore di matematica

[] aggiungi integrali al generatore di matematica

[] OTTIENI DATI EURUSD 1m 2002 to TODAY 4 10 bucks

[] save_model(model) # fix per nuova architettura e controlla la giusta formattazione per json

[] aggiungi MUTATE( ) nell algoritmo

[] aggiungi CROSS_OVER( ) nell algoritmo

[] aggiungi SELECT( ) nell algoritmo

[] SIGNAL COUNTER open: segnale che rappresenta la chiusura del segnale di opening, per prevenire che stia aperto nei momenti sbagliati

[] aprire un conto IBKR

[] sapere se posso fare piu subaccounts oppure solo un accoount su ibkr

[] utilizza l api per entrare a mercato

[] utilizza l api per entrare pendante

[] utilizza l api per mettere tp e sl

### **Done**
[x] aggiungi la possibilita di mettere il prezzo e i volumi nelle equazioni generate

[x] aggiungi nuovi metodi di normalizzazione
altri 10 nuovi metodi di normalizzazione

[x] REPORT aggiungi il segnale da visualizzares
    # OTTENUTO con data stream dei dati del prezzo che veniva convertito a segnale
    matplotlib .ion() che permette lo streaming continuo sotto il ciclo while True

[x] save_model(model)
    # DA FIXXARE

[x] from txt to py.  Trasforma un file txt con il modello salvato in un file .py che e' possibile lanciare con le api di IBKR e farci trading
    RISOLTO IN PARTE: manca solo da fare partire il trade effettivo

[x] data_stream.py salva i dati EURUSD ogni minuto in un database
    RISOLTO IN PARTE: il data provider free mi ha staccato dallo scraping

[x] fitness = get_fitness(model['performances']) # float: single abstract value 
    # eseguito con un semplice dizionario['chiave']

[x] model['performances'] = backtest(df_signal,df_price) #with PIP backtrader.py

[x] pop.append(model)

[x] run GA with initial population (from the 2#)

[x] shape rateo

[x] beta

[x] equation's family metadata for the generator

[x] normalization generator:

[x] logic generator:

[x] df_price: get price data

[x] equation generator

[x] df_indicators: compute df_ta 

[x] df_indicators : compute df_sympy

[x] df_indicators : normalize

[x] logic_string : create logic_string with df_indicators

[x] eval(logic_string): eval logic_string with df_sympy

[x] df_signal : OK** return signal over time

[x] alpha

[x] backtest(df_signal,df_price) ->  my backtester