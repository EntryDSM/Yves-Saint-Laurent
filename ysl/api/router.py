from flask import Blueprint
from flask_restful import Api

from ysl.api.admin_agency import AgencyInformation, ApplyInterviewerList
from ysl.api.admin import AdminSignup
from ysl.api.interviewer import CheckAgencyCode, InterviewerSignup, Login, Refresh
from ysl.api.admin_interview import CreateInterview, CreateQuestion, InterviewQuestion, EditInterview
from ysl.api.admin_interivew_list import ReadyInterview, DoneInterview
from ysl.api.admin_interviewer import AcceptInterviewer, RejectInterviewer, InterviewerList
from ysl.api.interivew_access import AddAccessInterviewer
from ysl.api.interview import OngoingInterview
from ysl.api.interviewee import SearchInterviewee
from ysl.api.interviewer_agency import JoinedAgencyList, ApplyToAgency
from ysl.api.evaluation import GetQuestionList, EvaluationForInterviewee
from ysl.api.excel import CreateExcel

bp_admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")
api_admin = Api(bp_admin)

bp_interviewer = Blueprint("agency", __name__, url_prefix="/api/v1")
api_interviewer = Api(bp_interviewer)

api_admin.add_resource(AdminSignup, "/signup")
api_admin.add_resource(AgencyInformation, "/agency/<agency_code>")
api_admin.add_resource(ApplyInterviewerList, "/<agency_code>/interviewer")
api_admin.add_resource(CreateInterview, "/<agency_code>/interview")
api_admin.add_resource(EditInterview, "/<agency_code>/<interview_id>")
api_admin.add_resource(CreateQuestion, "/<agency_code>/<interview_id>/question")
api_admin.add_resource(InterviewQuestion, "/<agency_code>/<interview_id>/<question_id>")
api_admin.add_resource(ReadyInterview, "/<agency_code>/ready/interview")
api_admin.add_resource(DoneInterview, "/<agency_code>/done/interview")
api_admin.add_resource(AcceptInterviewer, "/<agency_code>/interviewer/accept")
api_admin.add_resource(RejectInterviewer, "/<agency_code>/interviewer/reject")
api_admin.add_resource(AddAccessInterviewer, "/<agency_code>/<interview_id>/access")
api_admin.add_resource(InterviewerList, "/<agency_code>/join/interviewer")
api_admin.add_resource(CreateExcel, "/<agency_code>/done/<interview_id>/download")

api_interviewer.add_resource(CheckAgencyCode, "/agency/check")
api_interviewer.add_resource(InterviewerSignup, "/interviewer/signup")
api_interviewer.add_resource(Login, "/login")
api_interviewer.add_resource(OngoingInterview, "/<agency_code>")
api_interviewer.add_resource(SearchInterviewee, "/<agency_code>/<interview_id>/search")
api_interviewer.add_resource(JoinedAgencyList, "/agency")
api_interviewer.add_resource(ApplyToAgency, "/agency/apply")
api_interviewer.add_resource(GetQuestionList, "/<agency_code>/<interview_id>/question")
api_interviewer.add_resource(EvaluationForInterviewee, "/<agency_code>/<interview_id>/<student_code>")
api_interviewer.add_resource(Refresh, "/refresh")
