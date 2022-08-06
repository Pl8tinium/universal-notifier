# what is this

an unpolished tool for getting notifications from every website. the idea is to integrate every website that doesnt, or not in a satisfying way, present notification abilities into one tool to get all the information in one desired channel. This is currently telegram or the frontend. This could be expanded to basically everything so you can get your notifications where ever you want. 

and because you integrate the websites with js you can also alert yourself e.g. when a certain amazon product falls under a certain price. basically get alerted when a condition on a site changes. 

it depends on your js skills how long your plugin works as the site might change in the future. but IMO its still better to adjust a script than to daily lookup something like in my case

## How to run

- install dependencies
- get telegram bot token (use google) and put into backend.py
- start backend.py
- start frontend (e.g. 'npm run dev')
.. would in theory run without frontend but useful for adjusting plugins

## cool ideas 

- make it not fucking ugly and hacky
- create a tool to create plugins without code, basically a visual pointer editor to tell the tool to watchout for a certain value of the site. would also allow plebs to make use of this tool
- maybe use firefox instead of chrome as it supports headless extensions (useful for auto cookie accept extensions)
- make it dynamic and parameterizable 
- for frontend.. live view of the observed websites in iframe or similar
- refactor almost everything, make it more robust.. catch errors.. handle edge cases
- replace json data persistance storage with database
- put into docker

