# azurebucket

azurebucket is an internal REST API that I developed for my company to let internal users to be able to query the information about the resources on our Azure cloud environment. e.g. VM, storage and network etc.

Why?
----
While Azure provides similar REST API to allow you to query cloud resources info, there are number of good reasons  using this internal API over calling Azure API directly.

First off, users can get cloud VM information internally without the need of accessing to Azure cloud directly and perform any external authentication. Typically, to make a REST API call to Azure, you either need a user access to Azure or service principals created, that means you need to submit SR in order to get access to Azure. 

Secondly, the latency of sending to API call to Azure directly to retrieve VM info from Azure is often high, (>1 sec). This latency is mostly caused by network latency and the throttling mechanism introduced by Azure . This internal API provides high speed access to VM information, the average response/call time of API call is ~20-30ms.

Last and mostly importantly, unlike Azure API which provides nested data(object) structure in API response, the inventory API provides VM information in a simple flat structure format. This greatly reduces the burden of developer and system admin for understanding the complexity data structure when they are working with data returned by the API.

How does it work?
----

Usage
----

````shell
export DJANGO_ENV=DEV |PROD
export AZURE_TENANT_ID=<azure_tenant_id>
export AZURE_CLIENT_ID=<azure_client_id>
export AZURE_CLIENT_SECRET=<azure_client_secret>

docker-compose up -d

````

