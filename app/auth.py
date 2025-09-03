USE_GOOGLE_LOGIN = False  # Toggle later

if USE_GOOGLE_LOGIN:
    import firebase_admin
    from firebase_admin import credentials, auth
    from fastapi import Depends, HTTPException, Header

    cred = credentials.Certificate("firebase-service-account.json")
    firebase_admin.initialize_app(cred)

    def verify_token(authorization: str = Header(...)):
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization header")
        token = authorization.split(" ")[1]
        try:
            decoded = auth.verify_id_token(token)
            return decoded
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
else:
    def verify_token():
        return {"user": "anonymous"}  # Bypass for MVP
