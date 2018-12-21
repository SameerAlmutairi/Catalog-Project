from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify
from sqlalchemy import create_engine
from catalog_DB import Base, Catalog, Items, User, ItemPhotos
from flask import session as login_session
import random, string, httplib2, json, requests
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from sqlalchemy.orm import sessionmaker, joinedload

app = Flask(__name__)
engine = create_engine('sqlite:///catalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Juventus Store Catalog"

# Helpers
def getUserID(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user


def createUser(login_session):
    username = login_session['username']
    email = login_session['email']
    # if login_session['picture'] is not None:
    #     photo = login_session['picture']
    newUser = User(name = username,
                   email = email,
                   photo = 'https://dl6bglhcfn2kh.cloudfront.net/php3zs1aw.png?version=1467129384')
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = email).one()
    return user.id

@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    print(state)
    login_session['state'] = state
    return render_template('sectionTemplate.html', state=state, page='catalog')
    # return render_template('login.html', state=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'], 'success')
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        response = '<h1>Successfully disconnected !</h1> '
        # response = make_response(json.dumps('Successfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        # return response
        flash('Successfully disconnected')
        return redirect(url_for('showAllCatalogs'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Main Page that has all Catalogs
@app.route('/')
# @app.route('/catalog/')
def showAllCatalogs():
    list_of_catalogs = session.query(Catalog).all()
    # catalog_count = list_of_catalogs.count()
    return render_template('sectionTemplate.html', list_of_catalogs=list_of_catalogs, page='catalog')


# Show Catalog Items Page
@app.route('/catalog/<int:catalog_id>', methods=['GET', 'POST'])
def showCatalog(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(Items).filter_by(catalog_id=catalog_id).all()
    return render_template('sectionTemplate.html', catalog=catalog, item=item, page='catalogItems')


# it should be modal fade
# SHOW ITEM DETAILS
@app.route('/catalog/<int:catalog_id>/<int:item_id>/details', methods=['GET', 'POST'])
def showItem(catalog_id, item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    item = session.query(Items).filter_by(catalog_id=catalog_id, id=item_id).one()
    item_photos = session.query(ItemPhotos).filter_by(item_id=item_id).all()
    return render_template('sectionTemplate.html',
                           catalog=catalog, item=item, item_photos=item_photos, page='itemDetails')


# add new item
@app.route('/catalog/<int:catalog_id>/newItem', methods=['GET', 'POST'])
def newCatalogItem(catalog_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    if request.method == 'POST':
        if 'username' not in login_session:
            return redirect('/login')
        newItem = Items(name=request.form['name'],
                        description=request.form['description'],
                        price=request.form['price'],
                        catalog_id=catalog_id,
                        user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        for i in request.form.getlist('image[]'):
            newItemPhotos = ItemPhotos(photo_url=i, item_id=newItem.id, catalog_id=catalog_id)
            session.add(newItemPhotos)
            session.commit()
        flash('New Item Successfully Created')
        return redirect(url_for('showCatalog', catalog_id=catalog_id))
    else:
        return render_template('sectionTemplate.html', catalog, catalog_id=catalog_id, page='catalogItems')


# Edit specific item
@app.route('/catalog/<int:catalog_id>/<int:item_id>/edit', methods=['GET', 'POST'])
def editItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    editeditem = session.query(Items).filter_by(catalog_id=catalog_id, id=item_id).one()
    editItemPhotos = session.query(ItemPhotos).filter_by(item_id=item_id).all()
    if login_session['user_id'] != editeditem.user_id:
        return "<script>function myFunction() " \
               "{alert('You are not authorized to edit this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editeditem.name = request.form['name']
        if request.form['description']:
            editeditem.description = request.form['description']
        if request.form['price']:
            editeditem.price = request.form['price']
        session.add(editeditem)
        session.commit()
        for index, i in enumerate(editItemPhotos):
            i.photo_url = request.form.getlist('image[]')[index]
        # session.add(editItemPhotos)
        # session.commit()
        # send message that 'Item details have been updated'
        flash("Item details have been updated")
        return redirect(url_for('showItem', catalog_id=catalog_id, item_id=item_id))
    else:
        return render_template('sectionTemplate.html', catalog=catalog, item=editeditem,page='itemDetails')


# Delete specific item
@app.route('/catalog/<int:catalog_id>/<int:item_id>/delete', methods=['GET', 'POST'])
def deleteItem(catalog_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    deletedItem = session.query(Items).filter_by(id=item_id).one()
    deletedPhotoItems = session.query(ItemPhotos).filter_by(item_id=item_id, catalog_id=catalog_id).all()
    if login_session['user_id'] != deletedItem.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this item.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        session.delete(deletedItem)
        session.commit()
        print("photos has been deleted")
        flash("Item has been deleted")
        return redirect(url_for('showCatalog', catalog_id=catalog_id))
    else:
        print('Item not Deleted')
        return render_template('deleteItem.html', catalog=catalog, item=deletedItem)


# JSON APIs
@app.route('/catalog/JSON')
def catalogJSON():
    catalog = session.query(Catalog).options(joinedload(Catalog.items)).all()
    return jsonify(catalog=[dict(c.serialize,
                           items=[dict(i.serialize,
                                   images=[g.serialize for g in i.item_photos])for i in c.items])for c in catalog])


@app.route('/catalog/<int:catalog_id>/<int:item_id>/JSON')
def categoryItemJSON(catalog_id,item_id):
    catalog = session.query(Catalog).filter_by(id=catalog_id).one()
    items = session.query(Items).filter_by(id=item_id,catalog_id=catalog.id)
    return jsonify(items=[dict(i.serialize,images=[g.serialize for g in i.item_photos])for i in items])


# Main part runs if there is no exceptions, from python interpretur
if __name__ == '__main__':
    app.secret_key = 'super_secure'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
