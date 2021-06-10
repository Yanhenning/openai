import logging
import os
from flask import Flask, jsonify
from flask import request

from api.core.accounts.delete_account import delete_account
from api.core.accounts.update_account import update_account
from api.core.request_decorators import error_handler
from api.core.accounts.get_accounts import get_accounts
from api.core.accounts.get_account_by_id import get_account_by_id
from api.core.accounts.create_account import create_account

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apiconfig.json"


@app.get('/accounts')
@error_handler
def get_all_accounts_view():
    accounts = get_accounts()
    return jsonify(accounts), 200


@app.get('/account/<int:account_id>')
@error_handler
def get_account_view(account_id):
    account = get_account_by_id(account_id)
    return account, 200


@app.post('/account')
@error_handler
def create_account_view():
    created_account = create_account(request.json)
    return created_account, 200


@app.put('/account/<int:account_id>')
@error_handler
def edit_account_view(account_id):
    update_account(account_id, request.json or {})
    return {'account_id': account_id}, 204


@app.put('/account/<int:account_id>/delete')
@error_handler
def delete_account_view(account_id):
    delete_account(account_id)
    return f'Account (id: {account_id}) deleted'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return f"""
    An internal error occurred: <pre>{e}</pre>
    See logs for full stacktrace.
    """, 500


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
