Moves Timetracker
=================

### How to use:

1. Download moves data using [moves-export](http://moves-export.herokuapp.com/) to `moves.json`

2. Run `python moves_tt.py`

    The python script will output a list of places sorted by the time you've spent there. 
    
    For example, I spend some time at home, some at work (Sync Labs), and some more time at Cafes (West End Deli)

    ```
	Places:
	 - Home (578.90h)
	 - Sync Labs (137.74h)
	 - West End Deli (103.19h)
	 - Cranked (15.73h)
	 ...
	```

3. Run the python script again with the name of your work: `python moves_tt.py "Sync Labs"`

	This generates an ascii timesheet for that location. For example, on Tuesday, week 5 of 2015 I was at Sync Labs from 9:12am to 6:40pm = 9.5 hours.


	```
	--------------------
	Week 5
	--------------------
	Tuesday 2015/01/27
	09:12:32 - 18:40:42 = 9.5
	Wednesday 2015/01/28
	09:17:04 - 17:29:00 = 8.2
	Friday 2015/01/30
	09:14:38 - 18:15:48 = 9.0
	
	...
	```
	
	
### TODO:

- Detect and remove duplicate data
- Show lunch breaks
- Turn into web dashboard with oauth