# from Dawn till Dusk
creating a streamlit webpage showing race data for the 'from Dawn till Dusk' event.

It retrievs data from a google spreadsheet and displays it in different charts.
A logic based on the date, determins what to show. I.e. only show the plots at the day or later, not before.


## deployment with Azure CLI

Install Azure CLI, then do the following:
```
az login
az account set --subscription "<SUBSCRIPTION>"
az acr build --registry <ACR-NAME> --image <IMAGE-NAME>:v0.01 .
```
Second command is only necessary when there are several subsciptions.
Third command requires an ACR, this is set up easiest in portal.azure.com

After that, go to portal.azure.com, create a wep app, choose docker based, ACR and choose your image.
Et voilà, your webapp is running.

This one is running on:
```
https://dawntilldusk.azurewebsites.net/
```
