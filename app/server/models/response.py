#Error response model (same as Nest.js response)
def ErrorResponseModel(code, message, error):
    return {"statusCode":code, "message":message, "error":error}