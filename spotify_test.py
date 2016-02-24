# This module uses the Spotify API to find artists related to an artist
# specified by the user. There are currently two functions:
# find_ra() - finds all artists related to x
# find_ra_intersect() - finds all artists related to a, b, ..., AND z
#
# NOTE: This module uses the "spotipy" Python library for the Spotify Web API
# written by plamere: https://github.com/plamere/spotipy
#
# Author: Jeremy Dennen

import spotipy
import json
spotify = spotipy.Spotify()

# find_ra() will print a list of all artists related to the searched artist.
# this function will loop until the user tells it to stop.
#
# NOTE: currently, the function uses the first artist returned in the search
# result obtained by the Spotify API
def find_ra():
    loop_bool = True
    while loop_bool:
        search_term = raw_input('Enter an artist to search:\n')
        search_results = spotify.search(q='artist:' + search_term, type='artist')
        artist_id = search_results['artists']['items'][0]['id']

        artist_result = spotify.artist(artist_id=artist_id)
        related_artists = spotify.artist_related_artists(artist_id=artist_id)
        related_artists_list = related_artists['artists']
        print '\nArtists related to %s:' % (search_term)
        # print json.dumps(related_artists, indent=1)
        related_artists_list = set(artist['name'] for artist in related_artists_list)
        print '\n'.join(related_artists_list)

        keep_going = raw_input('\nWould you like to continue?\n')

        if keep_going in ('n', 'no', 'nope', 'hell nah'):
            loop_bool = False

# find_ra_intersect() will print a list of all artists related to ALL of the
# searched artist(s). Initially, this list is just the artists related to the
# first that was specified -- however, with each iteration, the list is narrowed
# down by means of a set intersection.
# This function will keep looping until the user tells it to stop, OR there are
# no more relationships.
#
# Example: user searches for "FIDLAR", "Wavves", and gets a set containing
# "Ty Segall" (among others)
#
# NOTE: currently, the function uses the first artist returned in the search
# result obtained by the Spotify API
def find_ra_intersect():
    flag = True
    # set of all searched artists
    search_terms = []
    intersection_related_artists = set()
    while flag:
        search_term = raw_input('Enter an artist to search:\n')
        search_results = spotify.search(q='artist:' + search_term, type='artist')
        search_terms.append(search_results['artists']['items'][0]['name'])
        artist_id = search_results['artists']['items'][0]['id']

        artist_result = spotify.artist(artist_id=artist_id)
        related_artists = spotify.artist_related_artists(artist_id=artist_id)
        related_artists_list = related_artists['artists']
        related_artists_set = set(artist['name'] for artist in related_artists_list)

        if intersection_related_artists:
            intersection_related_artists.intersection_update(related_artists_set)
        else:
            intersection_related_artists = related_artists_set

        if intersection_related_artists:
            print '\nArtists related to %s:' % (', '.join(search_terms))
            print '\n'.join(intersection_related_artists)
        else:
            print '\nLooks like there aren\'t any artists related to ALL of the following: \n%s\n' % (', '.join(search_terms))
            return False

        # check if user wants to keep looking for relationships
        keep_going = raw_input('\nWould you like to continue?\n')
        if keep_going in ('N', 'NO', 'n', 'no', 'nope', 'hell nah'):
            flag = False


# running this module will run the find_ra() function, unless 'intersect' is
# specified as an argument
if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'intersect':
        find_ra_intersect()
    else:
        find_ra()
