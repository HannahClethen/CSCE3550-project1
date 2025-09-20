# This file was completed with assistance from Github Copilot
from fastapi import FastAPI, Request #External libraires needed for api
from fastapi.responses import JSONResponse
from key_manager import KeyManager
from utils import generate_jwt  # function to generate JWT

app = FastAPI() # FASTAPI app instance
km = KeyManager(key_ttl=60)  # set key expiry time

@app.get("/.well-known/jwks.json")
@app.get("/jwks")
def get_jwks():
    # Endpoint to serve the json (jwks)
    return km.get_public_jwks()

@app.post("/auth")
def auth(request: Request):
    # Endpoint to issue JWTs
    try:
        # Check query to see if true
        expired = request.query_params.get("expired", "").lower() == "true"
        # Retrieve key data based on expired param
        key_data = km.get_key(expired=expired)
        if not key_data:
            return JSONResponse({"error": "No key found."}, status_code=404)

        if expired:
            # Issue JWT with expiry in the past (already expired)
            jwt_token = generate_jwt(
                private_key=key_data["private_key"],
                kid=key_data["kid"],
                expiry=-60  
            )
        else:
            # Generate a valid JWT with default expiry time 
            jwt_token = generate_jwt(
                private_key=key_data["private_key"],
                kid=key_data["kid"],
            )
            # Have to return the generate jwt token as json
        return {"token": jwt_token}
    except Exception as e:
        # If key isnt found return 500 error
        return JSONResponse({"error": f"Internal Server Error: {str(e)}"}, status_code=500)
