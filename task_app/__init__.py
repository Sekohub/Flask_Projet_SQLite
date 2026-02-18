from flask import Blueprint

task_app = Blueprint(
    "task_app",
    __name__,
    template_folder="templates"
)

