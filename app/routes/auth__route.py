from flask import Blueprint

from ..controllers.auth__controller import create__user__registration , create__user__login,refresh__token
auth__bp = Blueprint('auth', __name__)

auth__bp.route('/register', methods=['POST'])(create__user__registration)
auth__bp.route('/login', methods=['POST'])(create__user__login)
auth__bp.route('/refresh-token', methods=['POST'])(refresh__token)