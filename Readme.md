This repository is an attempt to follow [Ruslan Spivak's](https://github.com/rspivak/) series called [Let’s Build A Web Server](https://ruslanspivak.com/lsbaws-part1/), I would recommend to visit the original blog post.

## What is a web server?
A web server is a network server that is based on a physical server.

## What is a network socket?
According to wikipedia *A network socket is a software structure within network node of computer that serves as an endpoint for sending and receiving data across the network*
![](https://media.geeksforgeeks.org/wp-content/uploads/20220330131350/StatediagramforserverandclientmodelofSocketdrawio2-448x660.png)

## How a basic web server works?
A web server uses a network socket to communicate with the client or in other word to serve the client. A client and a server uses HTTP protocol to talk to each other. A web server at the beginning opens up a socket connection and starts listening to a particular port for incoming requests. When it detects a request it then reads the request gives back response in the form of a HTTP response.
![A typical http request and response body](https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages/httpmsgstructure2.png)


## How to Run 
### Create virtual environment
Create: `python3 -m venv <directory>`

Activate: `source <directory>/bin/activate`

Install : `pip install django flask pyramid`

Run: `python webserver1.py` for webserver1 `python webserver2.py djangoapp:app` for webserver2
