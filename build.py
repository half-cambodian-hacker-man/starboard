# Build script for the static site

from starboard.db import list_starred_projects
import sqlite3
import os
import shutil

import datetime


source_directory_name = "static"
output_directory_name = "static_out"


def generate_homepage(ctx, template_context):
    templating = ctx.ext("templating")
    return templating.from_file("./static/templates/index.html.j2").render(
        **template_context
    )


def generate_add_star_page(ctx):
    templating = ctx.ext("templating")
    return templating.from_file("./static/templates/star_project.html.j2").render()


def build(ctx):
    templating = ctx.ext("templating")
    templating.set_base_directory("./static/templates/")

    minification = ctx.ext("minification")
    direct_render = ctx.ext("direct_render")

    db = sqlite3.connect(os.environ["STARBOARD_DATABASE"])
    projects = list(list_starred_projects(db))
    project_timestamps = {
        project: datetime.datetime.fromisoformat(project.timestamp)
        for project in projects
    }

    template_context = {"projects": projects, "project_timestamps": project_timestamps}

    homepage_html = generate_homepage(ctx, template_context)
    ctx.write_text("index.html", minification.minify_html(homepage_html))

    star_project_html = generate_add_star_page(ctx)
    ctx.write_text("star/index.html", minification.minify_html(star_project_html))

    direct_render.run(ctx, "rss.xml.py", projects=projects)

    shutil.copytree(
        f"{source_directory_name}/assets",
        f"{output_directory_name}/assets",
        dirs_exist_ok=True,
    )
