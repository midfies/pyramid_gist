from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.security import remember, forget
from pyramid_gist.security import check_credentials

from ..models import User


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    try:
        query = request.dbsession.query(User)
        this_user = query.filter(User.username == 'testUser').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'this_user': this_user}


@view_config(route_name='login', renderer='../templates/login.jinja2', permission=NO_PERMISSION_REQUIRED)
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("home"),
                headers=auth_head
            )
    return {}


@view_config(route_name='logout')
def logout_view(request):
    auth_head = forget(request)
    return HTTPFound(request.route_url('login'), headers=auth_head)


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    try:
        query = request.dbsession.query(User)
        this_user = query.filter(User.username == 'testUser').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'this_user': this_user}


@view_config(route_name='register', renderer='../templates/register.jinja2')
def register_view(request):
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_gist_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
