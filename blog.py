from flask import Blueprint

blog = Blueprint('blog',__name__,url_prefix='/blog')


@blog.route('/add')
def admin_add():
    return ("blog add")

@blog.route('/del')
def admin_del():
    return ("blog del")