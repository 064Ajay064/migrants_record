from app import app, db, User

def main():
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        username = "admin"
        email = "admin@example.com"
        password = "Admin@123"
        user = User.query.filter_by(username=username).first()
        if user:
            print("Admin already exists. Username:", username)
            return
        user = User(username=username, email=email, role="admin")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        print("Admin created.")
        print("Username:", username)
        print("Password:", password)

if __name__ == "__main__":
    main()


