select title_keywords.tconst, PrimaryName FROM
	(SELECT * FROM title_principals Natural join name_basics) as names
		right outer join
	title_keywords on names.tconst = title_keywords.tconst