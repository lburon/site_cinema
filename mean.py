def weighted_average(ratings, letterboxd):
    lb = None
    imdb = None
    mc = None
    rt = None

    try:
        if letterboxd is not None:
            lb = float(letterboxd) * 20  # sur 100
    except:
        lb = None

    try:
        imdb_str = ratings.get('Internet Movie Database')
        if imdb_str:
            imdb = float(imdb_str.split('/')[0]) * 10
    except:
        imdb = None

    try:
        mc_str = ratings.get('Metacritic')
        if mc_str:
            mc = float(mc_str.split('/')[0])
    except:
        mc = None

    try:
        rt_str = ratings.get('Rotten Tomatoes')
        if rt_str:
            rt = float(rt_str.strip('%'))
    except:
        rt = None

    scores = [score for score in [lb, imdb, mc, rt] if score is not None]

    if scores:
        average_100 = sum(scores) / len(scores)
        average_10 = round(average_100 / 10, 1)
        return average_10
    else:
        return None