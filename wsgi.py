from battleforcastile_match_recorder import create_app

app = create_app(config_filename='development_config.py')


if __name__ == '__main__':
    app.run()
