from app import app, socketio

socketio.run(app, host="0.0.0.0", port=80,use_reloader=1,debug=1)