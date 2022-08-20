from weedly import app, config

if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.DEBUG)
