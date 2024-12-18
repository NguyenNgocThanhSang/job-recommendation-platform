from django.http import HttpResponse
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
import json
from .forms import *
from .firebase import UserResourceManager
from .helpers import AuthHelper, CVHelper, JobHelper, ChatBotHelper
from .serializers import *
from .authenticate import FirebaseAuthentication

class SignUpView(APIView):
  '''
  Sign up with email and password
  '''
  http_method_names = ['post', 'options']

  def post(self, request):
    # Get data from request
    try:
      form = SignUpForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )

    # Register user
    try:
      AuthHelper.sign_up(form.data['email'], form.data['password'], form.data['username'])
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )
    return Response(
      data={
        "success": True, 
        "message": "User registered successfully"
      }, 
      status=201
    )
  
class SignInView(APIView):
  '''
  Sign in with email and password
  '''
  http_method_names = ['post', 'options']
  
  def post(self, request):
    # Get data from request
    try:
      form = SignInForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    # Sign user in
    data = AuthHelper.sign_in(email=form.data['email'], password=form.data['password'])
    if data is None:
      return Response(
        data={
          "success": False, 
          "message": "Invalid email or password."
        }, 
        status=401
      )
    
    user_data, token = data
    return Response(
      data={
        "success": True,
        "message": "User signed in successfully",
        "data": user_data,
        "token": token,
      }, 
    )

class ForgotPasswordView(APIView):
  '''
  Send password reset email to user
  '''
  http_method_names = ['post', 'options']

  def post(self, request):
    # Get data from request
    try:
      form = ForgotPasswordForm(json.loads(request.body))
      if not form.is_valid():
        raise Exception(form.errors.as_data())
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    # Send password reset email
    try:
      AuthHelper.forgot_password(form.data['email'])
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )
    return Response(
      data={
        "success": True, 
        "message": "Password reset email sent successfully."
      }, 
    )

class UserCVView(APIView):
  '''
  Upload and get user's own CV
  '''
  http_method_names = ['get', 'post', 'options']
  authentication_classes = [FirebaseAuthentication]

  def get(self, request):
    try:
      file_info = CVHelper.get_cv_file_info(request.user.uid)
    except Exception as e:
      return Response(
        data = {
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
    if file_info is None:
      return Response(
        data = {
          "success": False, 
          "message": "CV file not found."
        }, 
        status=404
      )
    return Response(
      data={
        "success": True,
        "data": CVFileInfoSerializer(file_info).data
      },
      status=200
    )

  def post(self, request):
    try:
      if 'file' not in request.FILES:
        raise Exception("No file uploaded.")
      cv_file = request.FILES['file']
      file_info = CVHelper.upload_and_process_cv(cv_file, request.user.uid, request.auth)
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    return Response({
      "success": True, 
      "message": "File uploaded successfully.",
      "data": CVFileInfoSerializer(file_info).data
    })
  
class UserAvatarView(APIView):
    '''
    Serve user's avatar directly
    '''
    http_method_names = ['get', 'options']
    authentication_classes = [FirebaseAuthentication]

  def get(self, request):
    try:
      download_url = UserResourceManager.get_url("avatar.svg", request.user.uid, request.auth)
      return HttpResponseRedirect(download_url)
    except Exception as e:
      return Response(
        data = {
          "success": False, 
          "message": str(e)
        }, 
        status=400
      )
    
class PostJobView(APIView):
    '''
    Post a job to the data/jobs.json file
    '''
    http_method_names = ['post', 'options']
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        try:
            # Define the file path
            base_dir = os.getcwd()
            data_dir = os.path.join(base_dir, "data", "jobs.json")
            file_path = data_dir

            # Load existing job data
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        jobs = json.load(file)
                    except json.JSONDecodeError:
                        jobs = []
            else:
                jobs = []

            # Get new job data from the request
            new_job_data = request.data  # Expect a single job entry
            print("New job data:", new_job_data)  # Debugging

            # Validate required fields for the new job
            required_fields = [
                "job_title", "job_url", "company_name", "company_url", "company_img_url",
                "location", "post_date", "due_date", "fields", "salary", "experience",
                "position", "benefits", "job_description", "requirements"
            ]
            missing_fields = [field for field in required_fields if field not in new_job_data]
            if missing_fields:
                return Response(
                    data={
                        "success": False,
                        "message": f"Missing required fields: {', '.join(missing_fields)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Append the new job to the list of existing jobs
            jobs.append(new_job_data)

            # Save the updated job list back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(jobs, f, ensure_ascii=False, indent=4)

            return Response(
                data={
                    "success": True,
                    "message": "Job posted successfully!",
                    "data": jobs
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                data={
                    "success": False,
                    "message": str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    
class JobView(APIView):
  '''
  Get jobs details
  '''
  http_method_names = ['get', 'options']
  authentication_classes = [FirebaseAuthentication]

  def get(self, request):
    try:
      request_data = request.query_params
      form = GetJobsForm(data=request_data)
      if not form.is_valid():
        return Response(
          data={
            "success": False, 
            "message": form.errors.as_data()
          }, 
          status=400
        )
      page = int(form.data.get('page', 1))
      jobs, total = JobHelper.get_recommended_jobs(request.user.uid, page)
      return Response(
        status=200,
        data={
          "total": total,
          "page": page,
          "data": JobSerializer(jobs, many=True).data
      })
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )

class ChatBotView(APIView):
  '''
  Get chatbot response
  '''
  http_method_names = ['post', 'options']
  authentication_classes = [FirebaseAuthentication]

  def post(self, request):
    try:
      form = ChatBotForm(json.loads(request.body))
      if not form.is_valid():
        return Response(
          data={
            "success": False, 
            "message": form.errors.as_data()
          }, 
          status=400
        )
      return Response(
        data={
          "success": True, 
          "message": ChatBotHelper.send_message(request.user.uid, form.data['job_id'], form.data['message'])
        }, 
        status=200
      )
    except Exception as e:
      return Response(
        data={
          "success": False, 
          "message": str(e)
        }, 
        status=500
      )