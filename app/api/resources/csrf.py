from flask import render_template

from app.api.resources.authentication import TokenRequiredResource


class CSRFResource(TokenRequiredResource):
    def get(self):
        return render_template("api/auth/csrf.html")
