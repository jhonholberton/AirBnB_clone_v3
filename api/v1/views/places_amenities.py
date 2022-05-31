#!/usr/bin/python3
"""function to create the route status"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
import os
import json


@app_views.route('/places/<place_id>/amenities')
def amenities_place(place_id):
    """get amenities with his place_id"""
    if os.environ.get('HBNB_TYPE_STORAGE') != "db":
        for val in storage.all("Place").values():
            if val.id == place_id:
                return jsonify(list(map(lambda v: v.to_dict(),
                                        val.amenity_ids)))
    else:
        for val in storage.all("Place").values():
            if val.id == place_id:
                return jsonify(list(map(lambda v: v.to_dict(), val.amenities)))
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def amenities_delete_place(place_id, amenity_id):
    """delete a obj with his id"""
    amenity = storage.get("Amenity", amenity_id)
    place = storage.get("Place", place_id)
    if amenity is None or place is None:
        abort(404)

    if os.environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity not in place.amenity_ids:
            abort(404)
        place.amenity_ids.pop(amenity)
    storage.save()
    storage.close()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def amenitie_create(place_id, amenity_id):
    """create amenitie object"""
    amenity = storage.get("Amenity", amenity_id)
    place = storage.get("Place", place_id)
    if place is None or amenity is None:
        abort(404)

    if os.environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity.id in list(map(lambda x: x.id, place.amenities)):
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity.id in list(map(lambda x: x.id, place.amenity_ids)):
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity)

    return jsonify(amenity.to_json()), 201
