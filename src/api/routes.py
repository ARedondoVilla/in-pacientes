"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import datetime

from flask import Flask, request, jsonify, url_for, Blueprint, abort
from api.models import db, Users, Diseases, Posts, Comments, Donations, Follows, Relationships
from api.utils import generate_sitemap, APIException


api = Blueprint('api', __name__)



def get_one_or_404(model, id):
    row = model.query.filter_by(id=id, deleted_at=None).first()

    if not row:
        abort(404)
        # return "{} not found".format(model), 404 # PENDIENTE DE CONCATENAR EL NOMBRE DE LA TABLA
        
    return jsonify(row.serialize()), 200


def get_all_from_models(model):
    newList = []

    for item in model.query.filter_by(deleted_at=None).all():
        newList.append(item.serialize())

    return jsonify(newList), 200


def delete_one_from_models(model):
    row = model.query.filter_by(id=id, deleted_at=None).first()

    if not row:
        abort(404)

    row.deleted_at = datetime.datetime.utcnow()

    db.session.add(row)
    db.session.commit()

    return jsonify(row.serialize()), 200

####################################### USERS #######################################

@api.route("/users", methods=["GET"])
def handle_list_all_users():
    
    return get_all_from_models(Users)


@api.route("/users/<int:id>", methods=["GET"])
def handle_get_user(id):
    
    return get_one_or_404(Users, id)

    

@api.route("/users", methods=["POST"])
def handle_create_user():
    payload= request.get_json()

    required = ['first_name', 'email', 'nickname', 'password']

    types = {
        'first_name': str, 
        'email': str, 
        'nickname': str,
        'password': str
    }

    for key, value in payload.items():
        if key in types and not isinstance(value, types[key]):
            abort(400, f"{key} is not {types[key]}")
    
    for field in required:
        if field not in payload or payload[field] is None:
            abort(400)

    user = Users(**payload)
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.serialize()), 201


@api.route("/users/<int:id>", methods=["PUT"])
def handle_update_user(id):
    user = Users.query.filter_by(id=id, deleted_at=None)

    if not user or user.deleted_at is not None:
        return "User not found", 404

    payload = request.get_json()

    if "first_name" in payload:
        user.first_name = payload["first_name"]

    if "last_name" in payload:
        user.last_name = payload["last_name"]

    if "email" in payload:
        user.email = payload["email"]

    if "nickname" in payload:
        user.nickname = payload["nickname"]

    if "avatar" in payload:
        user.avatar = payload["avatar"]

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 200


@api.route("/users/<int:id>", methods=["DELETE"])
def handle_delete_user(id):
    user = Users.query.filter_by(id=id, deleted_at=None).first()

    if not user:
        return "User not found", 404

    user.deleted_at = datetime.datetime.utcnow()

    db.session.add(user)
    db.session.commit()

    return jsonify(user.serialize()), 200
    # return delete_one_from_models(Users)

######################################## Diseases #######################################

@api.route("/diseases", methods=["GET"])
def handle_list_all_diseases():

    return get_all_from_models(Diseases)


@api.route("/diseases/<int:id>", methods=["GET"])
def handle_get_disease(id):

    return get_one_or_404(Diseases, id)


@api.route("/diseases", methods= ["POST"])
def handle_create_disease():

    payload = request.get_json()

    required = ['scientific_name', 'slug', 'title']
    # owner_id required??

    types = {
        'scientific_name': str, 
        'slug': str, 
        'title': str,
    }

    for key, value in payload.items():
        if key in types and not isinstance(value, types[key]):
            abort(400, f"{key} is not {types[key]}")
    
    for field in required:
        if field not in payload or payload[field] is None:
            abort(400)

    disease = Diseases(**payload)

    db.session.add(disease)
    db.session.commit()

    return jsonify(disease.serialize()), 201


@api.route("/diseases/<int:id>", methods=["PUT"])
def handle_update_disease(id):

    disease = Diseases.query.filter_by(id=id, deleted_at=None).first()
    
    if not disease or disease.deleted_at is not None:
        return "disease not found", 404 

    payload = request.get_json()

    # Añadido un if para cada clave del payload
    if "title" in payload:
        disease.title = payload['title']

    if "scientific_name" in payload:
        disease.scientific_name = payload['scientific_name']

    if "description" in payload:
        disease.description = payload['description']

    if "slug" in payload:
        disease.slug = payload['slug']

    db.session.add(disease)
    db.session.commit()

    return jsonify(disease.serialize()), 200
    

@api.route("/diseases/<int:id>", methods=["DELETE"])
def handle_delete_disease(id):

    disease = Diseases.query.filter_by(id=id, deleted_at=None).first()

    if not disease:
        return "Disease not found", 404

    disease.deleted_at = datetime.datetime.utcnow()

    db.session.add(disease)
    db.session.commit()

    return jsonify(disease.serialize()), 200
   

######################################## Posts  #######################################

@api.route("/users/<int:id>/posts", methods=["GET"])
def handle_list_posts_from_user(id):
    user = Users.query.get(id)
    posts = []

    if not user:
        return "User not found", 404

    for post in user.posts:
        posts.append(post.serialize())
        
    return jsonify(posts), 200


@api.route("/diseases/<int:id>/posts", methods=["GET"])
def handle_list_posts_from_disease(id):
    
    Posts.query.filter_by(
        user_id=id,
        deleted_at=None
    ).all()


    disease = Diseases.query.get(id)
    posts = []

    if not disease:
        return "Disease not found", 404

    for post in disease.posts:
        posts.append(post.serialize())
        
    return jsonify(posts), 200


@api.route("/posts", methods= ["POST"])
def handle_create_post():

    payload = request.get_json()

    required = ['text']
    # publisher_id, creater_id required?

    types = {
        'text': str, 
    }

    for key, value in payload.items():
        if key in types and not isinstance(value, types[key]):
            abort(400, f"{key} is not {types[key]}")
    
    for field in required:
        if field not in payload or payload[field] is None:
            abort(400)

    post = Posts(**payload)

    db.session.add(post)
    db.session.commit()

    return jsonify(post.serialize()), 201
    

@api.route("/posts/<int:id>", methods=["PUT"])
def handle_update_post(id):

    post = Posts.query.filter_by(id=id, deleted_at=None).first()

    if not post or post.deleted_at is not None:
        return "post not found", 404 

    payload = request.get_json()

    # Añadido un if para cada clave del payload
    if "text" in payload:
        post.text = payload['text']
    
    if "publisher_id" in payload:
        post.publisher_id = payload['publisher_id']

    if "disease_id" in payload:
        post.disease_id = payload['disease_id']

    db.session.add(post)
    db.session.commit()
    
    return jsonify(post.serialize()), 200


@api.route("/posts/<int:id>", methods =["DELETE"])
def handle_delete_post(id):
    
    post = Posts.query.get(id)

    if not post:
        return "User not found", 404

    data = post.serialize()

    db.session.delete(post)
    db.session.commit()

    return jsonify(data), 200


######################################## Donations #######################################


@api.route("/donations", methods=["GET"])
def handle_list_all_donations():
    
    donations = []

    for donation in Donations.query.all():
        donations.append(donation.serialize())

    return jsonify(donations), 200

@api.route("/diseases/<int:disease_id>/donations", methods=["GET"])
def handle_get_donation_by_disease(disease_id):
    """ Return the list of donations selected by disease """
    return "Get donation for #{} .".format(disease_id)

@api.route("/users/<int:user_id>/donations", methods=["GET"])
def handle_get_donation_by_user(user_id):
    """ Return the list of donations selected by user"""
    return "Get donation made by #{} user.".format(user_id)

@api.route("/donations", methods=["POST"])
def handle_create_donation():
    """ Create Donation """
    payload= request.get_json()
    print(payload)
    return "Donation created"

######################################## Follows #######################################


@api.route("/follows", methods=["GET"])
def handle_list_all_follows():
    """ Return List of follows"""
    return "List all follows"


@api.route("/diseases/<int:disease_id>/follows", methods=["GET"])
def handle_get_follow_by_disease(disease_id):
    """ Return the list of follows of one disease """
    return "Get the follows of disease #{} .".format(disease_id)


@api.route("/users/<int:user_id>/follows", methods=["GET"])
def handle_get_follow_by_user(user_id):
    """ Return the list of follows of one user """
    return "Get the follows of disease #{} .".format(disease_id)


@api.route("/follows", methods=["POST"])
def handle_create_follow():
    """ Create follow """
    payload= request.get_json()
    print(payload)
    return "follow created"

# Tiene sentido editar un follow? como se marca y se desmarca? es un borrado o un put?:
# @api.route("/follows/<int:user_id>/<int:disease_id>", methods= ["PUT"])
# def handle_update_follow(user_id, disease_id):
#     """ Update existing follow """
#     response = {'message': 'success'}
#     return jsonify(response)


@api.route("/diseases/<int:disease_id>/follows", methods =["DELETE"])
def handle_delete_follow(disease_id):
    """Delete follow"""
    response = {'message': 'success'}
    return jsonify(response)


######################################## Relationships #######################################

@api.route("/relationships", methods=["GET"])
def handle_list_all_roles():
    """ Return List of follows"""
    return "List all follows"


# def handle_list_all_relationships():
#     relationships = []

#     for relationship in Relationships.query.all():
#         relationship.append(user.serialize())
#     return jsonify(relationships), 200

@api.route("/users/<int:user_id>/relationships", methods=["GET"])
def handle_get_user_roles(user_id):
    """ Return the amount of roles of an user"""
    return "Get roles of #{} user.".format(user_id)


# def handle_list_roles_from_user(id):
#     user = Users.query.get(id)
#     relationships = []

#     if not user:
#         return "User not found", 404

#     for relationship in user.relationship:
#         relationships.append(relationship.serialize())
        
#     return jsonify(relationships), 200


@api.route("/diseases/<int:disease_id>/relationships", methods=["GET"])
def handle_get_disease_roles(disease_id):
    """ Return the amount of roles of a disease"""
    return "Get roles of #{} disease.".format(disease_id)
# def handle_list_relationships_from_disease(id):
#     disease = Diseases.query.get(id)
#     relationships = []

#     if not disease:
#         return "Disease not found", 404

#     for relationship in disease.relationships:
#         relationships.append(relationship.serialize())
        
#     return jsonify(relationships), 200

@api.route("/diseases/<int:disease_id>/relationships", methods=["POST"])
def handle_create_role_for_disease():
    """ Create role for disease """
    payload= request.get_json()
    print(payload)
    return "Role created"


@api.route("/diseases/<int:disease_id>/relationships", methods=["PUT"])
def handle_update_role(disease_id):
    """ Update existing role """
    response = {'message': 'success'}
    return jsonify(response)


# @api.route("/diseases/<int:disease_id>/relationships", methods = ["DELETE"])
# def handle_delete_role(id):
#     """Delete Role"""
#     response = {'message': 'success'}
#     return jsonify(response)