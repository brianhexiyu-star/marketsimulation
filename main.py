from website.init import create_app, db


app = create_app()

with app.app_context():
    db.drop_all()     # delete all tables
    db.create_all()   # recreate tables
    print("Database reset successfully!")

if __name__ == "__main__":
    app.run(debug=True)
