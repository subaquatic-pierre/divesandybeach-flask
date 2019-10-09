from flaskblog import db

# Create dive site model
class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(100))
    level = db.Column(db.String(100))
    dive_time = db.Column(db.String(100))
    depth = db.Column(db.String(100))
    slug = db.Column(db.String(100))
    distance = db.Column(db.String(100))
    marine_life = db.Column(db.Text)
    description = db.Column(db.Text)
    map_image = db.Column(db.String(100), default='default_map.jpg')


    def __repr__(self):
        return f"Site('{self.name}', '{self.level}', '{self.depth}')"