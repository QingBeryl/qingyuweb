from flask import Flask
from bps.index_bp.index_bp import index_bp
from bps.sfs_shared.sfs_bp import sfs_bp
from bps.attendance_bp.attendance_bp import attendance_bp
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "2d2e7199-21c8-476e-a744-8951946a37c0"

app.register_blueprint(index_bp)
app.register_blueprint(sfs_bp)
app.register_blueprint(attendance_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)