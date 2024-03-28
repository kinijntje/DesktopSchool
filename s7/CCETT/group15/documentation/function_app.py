import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="ragehub",
                               connection="/subscriptions/b5f54a75-18a3-45c1-9626-7911b04ffe43/resourceGroups/Anti-Rage/providers/Microsoft.EventHub/namespaces/Anti-RageEventHub/eventhubs/ragehub") 
def RageHubTest(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
