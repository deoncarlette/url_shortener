# app_exceptions.py

from fastapi import HTTPException


class AppExceptions:

    @staticmethod
    def raise_bad_request(message):
        raise HTTPException(status_code=400, detail=message)

    @staticmethod
    def raise_not_found(request):
        message = f"URL '{request.url}' doesn't exist"
        raise HTTPException(status_code=404, detail=message)

    @staticmethod
    def raise_conflict(message):
        raise HTTPException(status_code=409, detail=message)
