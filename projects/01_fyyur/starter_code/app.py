# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import datetime
import sys

import dateutil.parser
import babel
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    url_for
)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
from flask_migrate import Migrate

from models import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

# DONE: connect to a local postgresql database
migrate = Migrate(app, db)

db.init_app(app)


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format_dt='medium'):
    date = dateutil.parser.parse(value)
    if format_dt == 'full':
        format_dt="EEEE MMMM, d, y 'at' h:mma"
    elif format_dt == 'medium':
        format_dt="EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format_dt, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Reset to initial data
#  ----------------------------------------------------------------

@app.route('/reset')
def reset_data():
    venue = Venue()
    artist = Artist()
    show = Show()

    # Erasing DB tables
    show.query.delete()
    venue.query.delete()
    artist.query.delete()

    # Filling DB tables with data
    venue.reset_to_initial_data()
    artist.reset_to_initial_data()
    show.reset_to_initial_data()

    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # DONE: replace with real venues data.
    # num_upcoming_shows should be aggregated based on
    # number of upcoming shows per venue.

    data = []
    unique_cities = Venue.query.distinct(Venue.city).all()

    for city in unique_cities:
        venues_in_city = Venue.query.filter_by(state=city.state)
        data_venues = []

        for ven in venues_in_city:
            shows_in_venue = Show.query.filter_by(venue_id=ven.id)
            show_count = 0

            for s in shows_in_venue:
                current_time = datetime.now()
                start_time_dt = datetime.strptime(
                    s.start_time[:-5],
                    '%Y-%m-%dT%H:%M:%S'
                )

                if start_time_dt > current_time:
                    show_count += 1

            data_venues.append({
                'id': ven.id,
                'name': ven.name,
                'num_upcoming_shows': show_count
            })

        data.append({
            'city': city.city,
            'state': city.state,
            'venues': data_venues
        })

    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # DONE: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and
    # "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term')
    venue_search_data = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
    search_count = str(len(venue_search_data))

    response = {
        'count': search_count,
        'data': venue_search_data
    }

    return render_template(
        'pages/search_venues.html',
        esults=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # DONE: replace with real venue data from the venues table, using venue_id

    data = []
    data_venue = Venue.query.all()

    for d in data_venue:
        genres = d.genres[1:-1]
        genres = list(genres.split(','))

        shows_in_venue = Show.query.filter_by(venue_id=d.id)
        upcoming_shows_count = 0
        past_shows_count = 0
        upcoming_shows = []
        past_shows = []

        for s in shows_in_venue:
            current_time = datetime.now()
            start_time_dt = datetime.strptime(
                s.start_time[:-5],
                '%Y-%m-%dT%H:%M:%S'
            )
            artist_in_show = Artist.query.filter_by(id=s.artist_id).first()

            if start_time_dt > current_time:
                upcoming_shows_count += 1
                upcoming_shows.append({
                    'artist_id': s.artist_id,
                    'artist_name': artist_in_show.name,
                    'artist_image_link': artist_in_show.image_link,
                    'start_time': s.start_time
                })
            else:
                past_shows_count +=1
                past_shows.append({
                    'artist_id': s.artist_id,
                    'artist_name': artist_in_show.name,
                    'artist_image_link': artist_in_show.image_link,
                    'start_time': s.start_time
                })

        data.append({
            'id': d.id,
            'name': d.name,
            'genres': genres,
            'address': d.address,
            'city': d.city,
            'state': d.state,
            'phone': d.phone,
            'website': d.website,
            'facebook_link': d.facebook_link,
            'seeking_talent': d.seeking_talent,
            'image_link': d.image_link,
            'past_shows': past_shows,
            'upcoming_shows': upcoming_shows,
            'past_shows_count': past_shows_count,
            'upcoming_shows_count': upcoming_shows_count
        })

    data = list(filter(lambda d: d['id'] == venue_id, data))[0]

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    form_venue = VenueForm(request.form)
    try:
        venue = Venue(
            name=form_venue.name.data,
            city=form_venue.city.data,
            state=form_venue.state.data,
            address=form_venue.address.data,
            phone=form_venue.phone.data,
            image_link=form_venue.image_link.data,
            facebook_link=form_venue.facebook_link.data,
            genres=form_venue.genres.data,
            website=form_venue.website_link.data,
            seeking_talent=form_venue.seeking_talent.data,
            seeking_description=form_venue.seeking_description.data
        )
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + form_venue.name.data + ' was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Venue ' + data.name +
        # ' could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash('An error occurred. Venue ' + form_venue.name.data +
              ' could not be listed')
        logging.exception(f'Failed to create a venue')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # DONE: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record.
    # Handle cases where the session commit could fail.

    error = False
    try:
        venue = Venue.query.get(id=venue_id)
        db.session.delete(venue)
        db.session.commit()
        print(f'Venue {venue_id} deleted successfully')
    except:
        db.session.rollback()
        error = True
        print(f'Error. Venue {venue_id} was not deleted')
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page,
    # have it so that
    # clicking that button delete it from the db
    # then redirect the user to the homepage

    return None


#  Artists
#  ----------------------------------------------------------------

@app.route('/artists')
def artists():
    # DONE: replace with real data returned from querying the database
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # DONE: implement search on artists with partial string search.
    # Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado",
    # and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    search_term = request.form.get('search_term')
    artist_search_data = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
    search_count = str(len(artist_search_data))

    response = {
        'count': search_count,
        'data': artist_search_data
    }

    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get('search_term', '')
    )


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # DONE: replace with real artist data from the artist table,
    # using artist_id

    data = []
    data_artist = Artist.query.all()

    for a in data_artist:
        genres = a.genres[1:-1]
        genres = list(genres.split(','))

        shows_in_artist = Show.query.filter_by(artist_id=a.id)
        upcoming_shows_count = 0
        past_shows_count = 0
        upcoming_shows = []
        past_shows = []

        for s in shows_in_artist:
            current_time = datetime.now()
            start_time_dt = datetime.strptime(
                s.start_time[:-5],
                '%Y-%m-%dT%H:%M:%S'
            )
            venue_in_show = Venue.query.filter_by(id=s.venue_id).first()

            if start_time_dt > current_time:
                upcoming_shows_count += 1
                upcoming_shows.append({
                    'venue_id': s.venue_id,
                    'venue_name': venue_in_show.name,
                    'venue_image_link': venue_in_show.image_link,
                    'start_time': s.start_time
                })
            else:
                past_shows_count +=1
                past_shows.append({
                    'venue_id': s.venue_id,
                    'venue_name': venue_in_show.name,
                    'venue_image_link': venue_in_show.image_link,
                    'start_time': s.start_time
                })

        data.append({
            'id': a.id,
            'name': a.name,
            'genres': genres,
            'city': a.city,
            'state': a.state,
            'phone': a.phone,
            'website': a.website,
            'facebook_link': a.facebook_link,
            'seeking_venue': a.seeking_venue,
            'seeking_description': a.seeking_description,
            'image_link': a.image_link,
            'past_shows': past_shows,
            'upcoming_shows': upcoming_shows,
            'past_shows_count': past_shows_count,
            'upcoming_shows_count': upcoming_shows_count
        })

    data = list(filter(lambda d: d['id'] == artist_id, data))[0]

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()

    # DONE: populate form with fields from artist with ID <artist_id>

    artist_to_edit = Artist.query.get(artist_id)

    form.name.data = artist_to_edit.name
    form.genres.data = artist_to_edit.genres
    form.city.data = artist_to_edit.city
    form.state.data = artist_to_edit.state
    form.phone.data = artist_to_edit.phone
    form.website_link.data = artist_to_edit.website
    form.facebook_link.data = artist_to_edit.facebook_link
    form.seeking_venue.data = artist_to_edit.seeking_venue
    form.seeking_description.data = artist_to_edit.seeking_description
    form.image_link.data = artist_to_edit.image_link

    artist = {
        'id': artist_to_edit.id,
        'name': artist_to_edit.name
    }

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # DONE: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    form = ArtistForm(request.form)
    try:
        artist = Artist.query.get(artist_id)

        artist.name = form.name.data
        artist.genres = form.genres.data
        artist.city = form.city.data
        artist.state = form.state.data
        artist.phone = form.phone.data
        artist.website = form.website_link.data
        artist.facebook_link = form.facebook_link.data
        artist.seeking_venue = form.seeking_venue.data
        artist.seeking_description = form.seeking_description.data
        artist.image_link = form.image_link.data

        db. session.add(artist)
        db.session.commit()
        flash('Artist ' + form.name.data + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('Update of  ' + form.name.data + ' went wrong!')
    finally:
        db.session.close()

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()

    # DONE: populate form with values from venue with ID <venue_id>

    venue_to_edit = Venue.query.get(venue_id)

    form.name.data = venue_to_edit.name
    form.genres.data = venue_to_edit.genres
    form.address.data = venue_to_edit.address
    form.city.data = venue_to_edit.city
    form.state.data = venue_to_edit.state
    form.phone.data = venue_to_edit.phone
    form.website_link.data = venue_to_edit.website
    form.facebook_link.data = venue_to_edit.facebook_link
    form.seeking_talent.data = venue_to_edit.seeking_talent
    form.seeking_description.data = venue_to_edit.seeking_description
    form.image_link.data = venue_to_edit.image_link

    venue = {
        'id': venue_to_edit.id,
        'name': venue_to_edit.name
    }

    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # DONE: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes

    form = VenueForm(request.form)
    try:
        venue = Venue.query.get(venue_id)

        venue.name = form.name.data
        venue.genres = form.genres.data
        venue.address = form.address.data
        venue.city = form.city.data
        venue.state = form.state.data
        venue.phone = form.phone.data
        venue.website = form.website_link.data
        venue.facebook_link = form.facebook_link.data
        venue.seeking_talent = form.seeking_talent.data
        venue.seeking_description = form.seeking_description.data
        venue.image_link = form.image_link.data

        db. session.add(venue)
        db.session.commit()
        flash('Venue ' + form.name.data + ' was successfully updated!')
    except:
        db.session.rollback()
        flash('Update of  ' + form.name.data + ' went wrong!')
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
    # called upon submitting the new artist listing form
    # DONE: insert form data as a new Venue record in the db, instead
    # DONE: modify data to be the data object returned from db insertion

    # on successful db insert, flash success
    form_artist = ArtistForm(request.form)
    try:
        artist = Artist(
            name = form_artist.name.data,
            city = form_artist.city.data,
            state = form_artist.state.data,
            phone = form_artist.phone.data,
            image_link = form_artist.image_link.data,
            genres = form_artist.genres.data,
            facebook_link = form_artist.facebook_link.data,
            website = form_artist.website_link.data,
            seeking_venue = form_artist.seeking_venue.data,
            seeking_description = form_artist.seeking_description.data
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + form_artist.name.data + ' was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name +
        # ' could not be listed.')
        db.session.rollback()
        flash('An error occured. Venue ' + form_artist.name.data +
              ' could not be listed')
        logging.exception(f'Failed to create an artist')
    finally:
        db.session.close()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # DONE: replace with real venues data.

    data = []
    show_data = Show.query.all()
    for show in show_data:

        venue_data = Venue.query.filter_by(id=show.venue_id)
        for v in venue_data:
            venue_name = v.name

        artist_data = Artist.query.filter_by(id=show.artist_id)
        for a in artist_data:
            artist_name = a.name
            artist_image_link = a.image_link

        data.append({
            'venue_id': show.venue_id,
            'venue_name': venue_name,
            'artist_id': show.artist_id,
            'artist_name': artist_name,
            'artist_image_link': artist_image_link,
            'start_time': show.start_time
        })

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db,
    # upon submitting new show listing form
    # DONE: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success

    form_show = ShowForm()
    try:
        show = Show(
            artist_id = form_show.artist_id.data,
            venue_id = form_show.venue_id.data,
            start_time = form_show.start_time.data
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
    except:
        # DONE: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Show could not be listed.')
        # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
        db.session.rollback()
        flash('An error occurred. '
              'Show could not be listed. {}'.format(sys.exc_info()))
        logging.exception(f'Failed to create a show')
    finally:
        db.session.close()
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: '
                  '%(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
