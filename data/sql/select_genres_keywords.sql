SELECT ke.tconst, genres, keywords FROM title_keywords as ke LEFT OUTER JOIN title_basics on ke.tconst = title_basics.tconst