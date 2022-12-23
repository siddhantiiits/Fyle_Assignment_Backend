from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments submitted to a teacher"""
    teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id, status='SUBMITTED')
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    """Grades an assignment"""

    graded_assignment = Assignment.grade_assignment(p.student_id,p.teacher_id,incoming_payload['id'],incoming_payload['grade'])
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

    return APIResponse.respond(data=graded_assignment_dump)




