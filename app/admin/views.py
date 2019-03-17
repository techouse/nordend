from flask import render_template

from . import admin


@admin.route("/", defaults={"path": ""})
@admin.route("/<path:path>")
def catch_all(path):
    return render_template("admin/index.html")
