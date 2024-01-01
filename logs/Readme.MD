# Logs

Logs are output to this directory.

## Example log

```log
INFO : main -> main :: Run started at: 2024-01-01 16:24:33.617510.
INFO : main -> main :: Working directory - root of the project: /home/mjancic/Documents/XCompNotify
DEBUG : Scrapper -> __init__ :: Initialized scrapper.
INFO : Scrapper -> scrap_all_sources :: Scrapping all sources.
DEBUG : scrapping_helper -> scrap_civlcomps :: Requesting data from CIVL.
DEBUG : scrapping_helper -> scrap_civlcomps :: Obtained data from CIVL.
DEBUG : scrapping_helper -> scrap_pwca :: Requesting data from PWCA.
DEBUG : scrapping_helper -> scrap_pwca :: Obtained data from PWCA. Now parsing.
DEBUG : scrapping_helper -> scrap_pwca :: Parsing PWCA completed.
DEBUG : scrapping_helper -> scrap_airtribune :: Requesting data from AIRTRIBUNE.
DEBUG : scrapping_helper -> scrap_airtribune :: Obtained data from AIRTRIBUNE. Now parsing.
DEBUG : scrapping_helper -> scrap_airtribune :: Parsing AIRTRIBUNE completed.
INFO : Filter -> __init__ :: Initialize filter class.
INFO : utils -> load_old_comps :: Loading competitions already known to me from 'data/old_comps.json'.
INFO : Filter -> get_new_comps :: Searching for new competitions, previously unknown to me.
INFO : main -> main :: No new comps found.
INFO : main -> main :: Run finished at: 2024-01-01 16:24:50.883804.
DEBUG : main -> main :: Duration: 0:00:17.266294.
```