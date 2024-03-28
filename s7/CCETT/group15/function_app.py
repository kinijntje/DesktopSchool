import azure.functions as func
import logging
import time

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Initialize a list to store timestamps
key_press_timestamps = []

@app.route(route="KeyboardpressTrigger")
def KeyboardpressTrigger(req: func.HttpRequest) -> func.HttpResponse:
    global key_press_timestamps

    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        # Add the current timestamp to the list
        key_press_timestamps.append(time.time())

        # Remove timestamps older than 5 seconds
        key_press_timestamps = [ts for ts in key_press_timestamps if time.time() - ts <= 5]

        # Check if there are more than 5 key presses in the last 5 seconds
        if len(key_press_timestamps) > 10:
            return func.HttpResponse(f"Special message: More than 5 key presses received in the last 5 seconds.")
        else:
            return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

@app.route(route="AzureSad", auth_level=func.AuthLevel.FUNCTION)
def AzureSad(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )