from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    favorites = db.relationship('Favorite', backref='user')
    

    def __repr__(self):
        return f'{self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class Galaxy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    coordinate_center_x = db.Column(db.Float, nullable=False) 
    coordinate_center_y = db.Column(db.Float, nullable=False)        
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.String(240))

    # OBLIGATORIO para establecer la relación
    galaxy_id = db.Column(db.Integer, db.ForeignKey('galaxy.id'), nullable=False)
    galaxy = db.relationship('Galaxy')

    
    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        } 
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(240))
    

    def __repr__(self):
        return f'{self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
        }   
    

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)

    planet = db.relationship('Planet', foreign_keys=[planet_id])
    character = db.relationship('Character', foreign_keys=[character_id])



    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet': self.planet.serialize() if self.planet else None,
            'character': self.character.serialize() if self.character else None,
        }
        