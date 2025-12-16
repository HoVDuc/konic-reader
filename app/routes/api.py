"""API routes - JSON endpoints"""
from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Shared progress tracker
conversion_progress = {}

@api_bp.route('/status/<task_id>')
def get_status(task_id):
    """Get processing status for a task"""
    status = conversion_progress.get(task_id, {'status': 'unknown', 'progress': 0})
    return jsonify(status)

def update_progress(task_id, status, progress, message):
    """Update progress for a task"""
    conversion_progress[task_id] = {
        'status': status,
        'progress': progress,
        'message': message
    }
