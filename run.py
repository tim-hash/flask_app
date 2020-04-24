from flask_blog import create_app


app = create_app()  # could pass a config here

if __name__ == '__main__':
    app.run(debug=True)  # This allows us to refresh directly the site without shuting it down
