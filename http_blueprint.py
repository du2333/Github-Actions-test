import azure.functions as func
import json
import os
from Spotify_API import get_recommendation, search, get_token

bp = func.Blueprint()

client_id = os.environ.get("Client_ID")
client_secret = os.environ.get("Client_Secret")


@bp.route(route="recommendation")
def recommendation_function(req: func.HttpRequest) -> func.HttpResponse:
    id = req.params.get("song")
    token = get_token(client_id, client_secret)

    if id:
        recommendation_list = get_recommendation(token, id)
        return func.HttpResponse(
            json.dumps(recommendation_list), mimetype="application/json"
        )
    else:
        error_response = {"error": "Missing parameters", "status_code": 400}
        return func.HttpResponse(
            json.dumps(error_response), mimetype="application/json", status_code=400
        )


@bp.route(route="search")
def search_function(req: func.HttpRequest) -> func.HttpResponse:
    query = req.params.get("q")
    token = get_token(client_id, client_secret)
    if not query:
        error_response = {"error": "Missing query parameter", "status_code": 400}
        return func.HttpResponse(
            json.dumps(error_response), mimetype="application/json", status_code=400
        )

    search_type = req.params.get("type", "track")
    limit = req.params.get("limit", 5)

    search_results = search(token, query, search_type, limit)

    return func.HttpResponse(json.dumps(search_results), mimetype="application/json")
