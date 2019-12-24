#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy import func
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# TODO: connect to a local postgresql database


app = Flask(__name__)
#need to import the flask app from app.py??????????
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Shows', backref="Venue",lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    shows = db.relationship('Shows', backref="Artist",lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
#    name = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id), nullable=False)
    start_time = db.Column(db.Date, nullable=True)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#return babel.dates.format_datetime(date, format, locale='en')


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

#db.create_all()

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  print(Venue.query.all()[0].city)
  # TODO: replace with real venues data.
  return render_template('pages/venues.html', areas = Venue.query.all())
  #       num_shows should be aggregated based on number of upcoming shows per venue.

      #above need to look up the redux for finding something LIKE the search term
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

      #likeSearch = '%' + search_term + '%'
      #print("This is the like search result",likeSearch)
      #response_results = Venue.query.filter_by(Venue.name.like(likeSearch))

@app.route('/venues/search', methods=['POST'])
def search_venues():
    #get the search term from the post request body
    search_term = request.form.get('search_term')
    # set up the response to have jsonified queries of something like the search term
#    response_results = Venue.query.filter_by(name=search_term | ))

    #queryArray = search_term.split(" ")
    #print("the query array is",queryArray)


    #response_results = Venue.query.filter(Venue.name.in_(queryArray))

    likeSearch = '%' + search_term + '%'
    print("This is the like search result",likeSearch)
    response_results = Venue.query.filter(Venue.name.like(likeSearch))


    print("response_results is",response_results)


    response={
    "results": response_results
    }
    #jsoned_response= jsonify(response)

    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)

    data = {
    "id": venue_id,
    "name": venue.name,
    #"genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    #"website": venue.website,
    "facebook_link": venue.facebook_link,
    #"seeking_talent": venue.seeking_talent,
    #"seeking_description": venue.seeking_description,
    #"image_link": venue.image_link,
    #"past_shows": venue.past_shows,
    #"upcoming_shows": venue.upcoming_shows,
    #"past_shows_count": venue.past_shows_count,
    #"upcoming_shows_count": venue.upcoming_shows_count
    }
    return render_template('pages/show_venue.html', venue=data)
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  name = request.form['name']
  address = request.form['address']
  print("This is what we are getting as the address",address)
  phone = request.form['phone']
  genres = request.form['genres']
  city = request.form['city']
  state = request.form['state']

  try:
      newVenue = Venue()
      newVenue.name = name
      print("Venue name is",newVenue.name)
      newVenue.address = address
      newVenue.phone = phone
      newVenue.genres = genres
      newVenue.city = city
      newVenue.state = state
      print("newVenue", newVenue)
      db.session.add(newVenue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
      print("something went wrong")
      db.session.rollback()
      flash('An error occured! Venue ' + request.form['name'] + ' could not be listed')
  finally:
      db.session.close()

  # TODO: modify data to be the data object returned from db insertion


  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')



@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  print(Venue.query.all()[0].city)
  # TODO: replace with real venues data.
  return render_template('pages/artists.html', artists = Artist.query.all())
  #       num_show


@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  likeSearch = '%' + search_term + '%'
  print("This is the like search result",likeSearch)
  artist_results = Artist.query.filter(Artist.name.like(likeSearch))

  print("artist_results is",artist_results)

  count = 0
  for item in artist_results:
      count+=1

  data = []
  for item in artist_results:
      data.append(item)

  print("This is the data",data)
#calculate the count - query for a count of artists that match search_term
#count = db.session.query(func.count())
#get ids of the artists and export their data
  response= {
  "count":count,
  "data": data}

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist_data = Artist.query.get(artist_id)
    data={
    "id": artist_data.id,
    "name": artist_data.name,
    "genres": artist_data.genres,
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    #website": artist_data.website,
    "facebook_link": artist_data.facebook_link,
    #"seeking_venue": artist_data.seeking_venue,
    #"seeking_description": artist_data.seeking_description,
    #"image_link": artist_data.image_link,
    #"past_shows": artist_data.past_shows,
    #"upcoming_shows": artist_data.upcoming_shows,
    #"past_shows_count": artist_data.past_shows_count,
    #"upcoming_shows_count": artist_data.upcoming_shows_count
    }
    return render_template('pages/show_artist.html', artist=data)



  #ata = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artistToEdit = Artist.query.get(artist_id)
  artist={
    "id": artistToEdit.id,
    "name": artistToEdit.name,
    #"genres": artistToEdit.genres,
    "city": artistToEdit.city,
    "state": artistToEdit.state,
    "phone": artistToEdit.phone,
    #"website": artistToEdit.website,
    "facebook_link": artistToEdit.facebook_link,
    #"seeking_venue": True,
    #"seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    #"image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  print("This function's job is to get the venue id's information to begin editing")

  venue = Venue.query.get(venue_id)
  print("This is what it's sending back",venue)
  print("Just tsting that this is working how I am expecting it to",venue.city,venue.state,venue.name)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes


  name = request.form['name']
  address = request.form['address']
  print("This is what we are getting as the address",address)
  phone = request.form['phone']
  genres = request.form['genres']
  city = request.form['city']
  state = request.form['state']

  try:
      venueToEdit = Venue.query.get(venue_id)
      venueToEdit.name = name
      print("Venue name is",venueToEdit.name)
      venueToEdit.address = address
      venueToEdit.phone = phone
      venueToEdit.genres = genres
      venueToEdit.city = city
      venueToEdit.state = state
      print("newVenue", venueToEdit)
      db.session.add(venueToEdit)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
      print("something went wrong")
      db.session.rollback()
      flash('An error occured! Venue ' + request.form['name'] + ' could not be listed')
  finally:
      db.session.close()


  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    print("artist function is running")
    name = request.form['name']
    print("This is the artist's name:",name)
    genres = request.form['genres']
    city = request.form['city']
    print("this is the artist's city",city)
    state = request.form['state']
    print("this is the artist's state",state)

    try:
        print("TRYING!!!")
        newArtist = Artist()
        print("newArtist",newArtist)
        print("Created new artist")
        newArtist.name = name
        print("Artst name is",newArtist.name)
        newArtist.genres = genres
        newArtist.city = city
        print(newArtist.city)
        newArtist.state = state
        print(state)
        db.session.add(newArtist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        print("something went wrong")
        db.session.rollback()
        flash('An error occured! Artist ' + request.form['name'] + ' could not be listed')
    finally:
        db.session.close()

    return render_template('pages/home.html')



  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    showData = Shows.query.all()

    return render_template('pages/shows.html', shows=showData)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()

  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
#    name = request.form['name']
    artist_id = request.form['artist_id']
    print("This is the artist id",artist_id)
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']
    print("This is what we have for the start time",start_time)

    try:
        newShow = Shows()
        print("This is the newShow instance",newShow)
    #    newShow.name = name
        newShow.artist_id = artist_id
        print(newShow.artist_id)
        newShow.venue_id = venue_id
        print(newShow.venue_id)
        newShow.start_time = start_time
        print(newShow.start_time)
        print("Just about to add to database")

        db.session.add(newShow)
        db.session.commit()
        print("Successfully added!")
    except:
        print("an error occured!")
        db.session.rollback()
    finally:
        db.session.close()

    return render_template('pages/home.html')

  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
