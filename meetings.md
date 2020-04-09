# Meeting Notes 04/04/2020

### Ideas 
* Should we focus on logical clustering?
* We could do fuzzy clustering--3 clusters could be different, but how different? How can we capture two clusters that are more similar to eachother than the third cluster?
* Two approaches to clustering:
 	* 1. Look for keywords and list them. Create keyword sequence string per query, and use those to compare against diff queries (try diff text mining techniques)
	* 2. Different grouping criteria (Eg. types of join, number/position of subquery) - ignore other aspects, but focus on this to create smaller subgroups.
* Keyword differences
	* Left outer join vs. left join
	* Full outer join vs. outer join
* Get rid of unneccesary parentheses? Or add required parentheses. (@Sush--can you elaborate?)
* Differentiating aliases from table names. 

### Clarifications (Questions for a professor)
* Should we count AS? What if someone used COUNT(*) multiple times instead of variable name (which you could achieve with AS). 
* Remove ASC/DESC? Assumption--remove asc because it is implied, leave desc for now.
* General clustering algo / specific to CS411 (and other intro-level db courses)
* Should we care about joins vs. commas? Logically, they are the same...
* How specific? What if we want to cluster by a certain thing (the two approaches listed above). For instance, if two queries are essentially the same except for ONE join...they do JOIN vs. natural join? OR, (Students NATURAL JOIN Enrollments), Courses vs. (Students NATURAL JOIN Courses), Enrollments. (Order of joining is different)


# Abdu Meeting 04/08/2020 
- Group by correct answer (dig deeper...simple vs. complex). Good place to start! (Subqueries vs. extras/unncessary conditions!)
- Initial idea (keywords only)--losing important information like table names, etc! Good starting point though--useful! 
- Consider this: what about order of selection? (sID, grade vs. grade sID).
	- Group by, order by, what are you joining by?! 
	- This would be more "rich".
	- Subqueries--are "features"? (1 subquery in FROM, 2 in WHERE? etc etc.)
	- building something insensitive to naming!! 

- Grading by correct vs. incorrect answers? 
	- Blanket approach--cluster all of them + few features 
	- Might be the easiest 

- Should we cluster the schema definition? 
	- If smart: yes
	- But, we could skip 

- Consider queries different if they are grouping by different things (even if its name vs. Id...)
- Cluster by parameters and sensitivity! 
- Parser
	- Eliminate: parenthases without SELECT FROM WHERE 
	- ASC and ORDER BY are the same 

TL;DR: we can start with our simplest text-mining approach (keywords-only) for now. maybe increase sensitivity in each iteration as we go? 
1. add subqueries as features 
2. count table names and variable names
3. sensitivity clustering (choose parameters etc...how picky?)
