# Answers to questions
## 4. Identify keys, both primary keys and foreign keys
Primary keys are marked as **BOLD** and foreign keys as *ITALIC*

### Theaters
**t_name**

### Films
**imdb_key**

### Customers
**user_name**

### Performances
**p_id**
*imbd_key*
*t_name*

### Tickets
**t_id**
*p_id*
*user_name*

#### a) Which relations have natural keys?
For films: (title, year)
For theatres: name
performances: have no natural keys
customers have no natural keys
tickets have no natural keys

#### b) Is there a risk that any of the natural keys will ever change?
If movies have different titles in different countries. Or if Star Wars changes to Star Wars episode IV A new hope.
Movie theatres can change names.

#### c) Are there any weak entity sets?
If performances did not have a p_id then it woudl have been weak

#### d) In which relations do you want to use an invented key. Why?
The performance relation between theatre and film in order to reduce redundancy in the tickets table

## 6. Convert the E/R model to a relational model, use the method described during lecture 4.
Describe your model in the following format (i.e., mark primary keys and foreign keys with underscores around primary keys, and a slash around foreign keys)

theatres(_t_name_, capacity)
films(_imbd_key_, title, year, runtime)
custumers(_user_name_, full_name, password)
performances(_p_id_, time, date, /imdb_key/, /t_name/)
tickets(_t_id_, /p_id/, /user_name/)

## 7. There are at least two ways of keeping track of the number of seats available for each performance -- describe them both, with their upsides and downsides

Assuming each theatre only has one screening room.
Check capacity - tickets existing for a specific performance
SELECT capacity - (
  SELECT count()
  from tickets
  Where p_id = 1)
from theatres
join performances
using(t_name)
where p_id = 1

------

SELECT capacity - count()
FROM   theatres
JOIN   performances
USING  (t_name)
JOIN   tickets
USING  (p_id)
WHERE  p_id = 1
