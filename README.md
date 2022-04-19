# PythonFlaskMiniTwitter

## Pre-requisites
* Pycharm
* Python 3.8 or superior 
* MySQLDatabase (Local or remote) configured according to script contained under "./database" folder

## Local run
On project root folder execute:
* mkdir lib
* python -m pip install -r requirements.txt --target=./lib
* mark lib directory as sources root on PyCharm
* Replace database attributes on main.py

  

## Critique
* Enhancements
  * Setup an ORM to manage database queries and prevent SQL injections
  * Exchange query parameter "quote" to request body on route "/repost/<id_post>/user/<user_id>"
  * Optimize all repost validations
  * Create generic repository layer
  * Create more validations and/or custom messages for different cenarios and bugs that might occur in the future
  * Better treatments for boolean query parameters
* Scaling
  * The main bottleneck for this first version would be the amount of validation queries used for the repost 
route and service. Given a scenario where many people are reposting, there's a huge possibility that some of these 
request would fail due to data integrity issues. One of the main strategies would be using a CQRS strategy and 
separating queries and commands into separate microservices, where the command side would be reading from a message 
queue to prevent these issues. Infrastructure-wise I would expose this API either on a serverless technology or a managed
container registry.