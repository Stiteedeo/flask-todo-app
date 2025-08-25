from app import create_app, db
from app.models import Task,User

app = create_app()


with app.app_context():
    print(User.query.all)
    print(Task.query.all)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
