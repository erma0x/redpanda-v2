API with FastAPI and Flask server

# USER
    generate_portfolio() 
        ID + Backtest Performance of one portfolio 
        Save into db_portfolio_users.sqlite3 


# ADMIN
    get_portfolio() 
        get the data structure JSON of porfolio from REDIS database
        of one of the best portfolios.

    generate_complete_portfolio() 
        get one of the bests portfolio generated by the algotithm



# ADMIN or MINTER

    generate_model(api_key)   
        GeneticAlgorithm + Backtest -> generate models
        filter out all the acceptable founded from the algorithm

    return (ID_address , Performance, Model ) 



from redpanda-generator as RPG

client = RPG.client(URl_provider='https://my.redpanda.fi' , API_ADDRESS='', API_KEY='')
results = client.generate_model()

client.get_model_performance(id_address)

my_model = results.model_
performance = results.performance_
id_model = results.id_


# USER
    get_model_performance(ID_address)
        return( ID_address , backtest performance of one model ) 
        Save into db_portfolio_users.sqlite3 