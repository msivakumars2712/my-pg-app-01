from database import db
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas.user import UserSchema
from models import UserModel
from passlib.hash import pbkdf2_sha256

blp = Blueprint("User", "__name__", description="Operation for User")


@blp.route("/register")
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError:
            abort(400, message="User with that name already exist")
        except SQLAlchemyError as e:
            abort(500, message=str(e))


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

