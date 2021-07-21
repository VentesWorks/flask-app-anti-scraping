from random import randint

from faker import Faker
from flask import Flask, request, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

Faker.seed(0)
fake = Faker()

missing_pids = [5,13,18,25]
companies = {"{:0>4d}".format(i): fake.company() for i in range(1, 1001) if i not in missing_pids}

limiter = Limiter(app, key_func=get_remote_address)


@app.route("/")
def listing():
    links = ''.join(f'<li><a href="/page/{pid}">{pid}</a></li>' for pid in companies.keys())

    resp = make_response("<html><body><ul>" + \
        links + \
        "</ul></body></html>")

    resp.set_cookie("CSRF-Token", value="XYZ")
    return resp, 200


@app.route("/page/<pid>")
@limiter.limit("10/minute;100/hour")
def page_detail(pid):
    user_agent = request.headers.get('User-Agent', '')

    if "Accept-Language" not in request.headers or "Chrome" not in user_agent and "Firefox" not in user_agent:
        return "bot is not allowed", 403

    if 'CSRF-Token' not in ''.join(request.cookies.keys()) and randint(1, 6) == 1:
        return "<html><body><p>Captcha challenge: are you a bot?</p></body></html>", 200

    try:
        company_name = companies[pid]
    except KeyError:
        return "<html><body><p>Company not found</p></body></html>", 404
    else:
        if randint(1, 10) == 1:
            return "server down", 503
        else:
            resp = make_response(f'<html><body><p id="company-id">{pid}</p><p id="company-name">{company_name}</p></body></html>')
            resp.set_cookie("CSRF-Token", value="XYZ")
            return resp, 200
