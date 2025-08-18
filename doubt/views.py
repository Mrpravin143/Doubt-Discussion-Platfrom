from django.shortcuts import render,redirect,get_object_or_404
from doubt.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden




def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').capitalize()
        last_name = request.POST.get('last_name', '').capitalize()
        email = request.POST.get('email', '').lower()
        role = request.POST.get('role', '').capitalize()
        course = request.POST.get('course', '').capitalize()
        division = request.POST.get('division', '')
        year = request.POST.get('year', '').capitalize()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Validation

        if year == "":
            year = None
        else:
            year = int(year)

        if not all([first_name, last_name, email, role,password, confirm_password]):
            messages.error(request, "All fields are required!")
            return redirect('/Registration/')

        if '@' not in email or '.' not in email:
            messages.error(request, "Invalid email format!")
            return redirect('/Registration/')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('/Registration/')

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters.")
            return redirect('/Registration/')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('/Registration/')

        # User creation
        user_obj = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role,
            course=course,
            division=division,
            year=year
        )
        user_obj.set_password(password)  
        user_obj.save()

        messages.success(request, "Registration successful!")
        return redirect('/Login_user/')

    return render(request, 'register.html')





def login_user(request):
    if request.method == "POST":
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')

       

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return redirect('/Login_user/')
        
        user = authenticate(request, username=email, password=password)


        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            if hasattr(user, 'role'):
                
                if user.role.lower() == "admin":
                    if not user.is_superuser:
                        user.is_staff = True
                        user.save()
                    
                    return redirect('/admin/')
                

                elif user.role == "Student":
                    return redirect("/")

                elif user.role == "Teacher":
                    return redirect("/teacher/doubts/")

                else:
                    messages.error(request, "Unknown user role.")
                    return redirect('/Login_user/')
            else:
                messages.error(request, "User role not set.")
                return redirect('/Login_user/')

        else:
            messages.error(request, "Invalid credentials!")
            return redirect('/Login_user/')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "LogOut Success. Thank You!")
    return redirect('/Login_user/')  # Change this to your actual login URL


    
# @login_required
def student_dashboard(request): 
    suport = Coordinator.objects.all() 
    logo = Logo.objects.all() 
    team = DevlopmentTeam.objects.all() 
    features = Features.objects.all()

    # recent doubts order by doubt_name (descending)
    recent_doubts = AskDoubts.objects.all().order_by('-doubt_name')

    students_count = CustomUser.objects.filter(role='Student').count()
    teachers_count = CustomUser.objects.filter(role='Teacher').count()
    resolved_doubts_count = DoubtAnswer.objects.filter(status=True).count()
    
    # decrypting each doubt field
    for doubt in recent_doubts:
        doubt.decrypted_name = doubt.get_decrypted_name()
        doubt.decrypted_description = doubt.get_decrypted_description()

   

    context = {
        'coordinators': suport,
        'team': team,
        'features': features,
        'doubts': recent_doubts,
        'logo': logo,
        'students_count':students_count,
        'teachers_count':teachers_count,
        'resolved_doubts_count':resolved_doubts_count,
    }

    return render(request, "student_dashboard.html", context)


@login_required
def ask_doubts(request):
    if request.method == "POST":
        doubt_name = request.POST.get('doubt')
        doubt_description = request.POST.get('description')
        teacher_select = request.POST.get('teacher')
        subject_select = request.POST.get('subject')
        doubt_image = request.FILES.get('image')

        # validations are here
        if doubt_name == "":
            messages.error(request,"'Your Doubt' Field Dont Keep Empty ! ")
            return redirect('/Ask_Doubts/')

        # save data in database table
        AskDoubts.objects.create(
            doubt_name=doubt_name,
            doubt_description=doubt_description,
            teacher_select=teacher_select,
            subject_select=subject_select,
            doubt_image=doubt_image,
            user = request.user,
        )

        messages.success(request, "Your doubt has been submitted successfully!")
        return redirect('/Ask_Doubts/')
    
    all_users = CustomUser.objects.all()

    status_Updation = DoubtAnswer.objects.all().order_by('-created_at')

    subject_select = AskDoubts.SUBJECT_CHOICE

    user_doubts = AskDoubts.objects.filter(user=request.user).order_by('created_at')


    for doubt in user_doubts:
        doubt.decrypted_name = doubt.get_decrypted_name()
        doubt.decrypted_description = doubt.get_decrypted_description()


    context={
        'subject_select':subject_select,
        'all_Users':all_users,
        'doubts':user_doubts,
        'status_Updation':status_Updation,
    }    
    
    return render(request,'ask_doubt.html',context)




def profile_view(request):
    user = request.user  

    # Always get or create profile safely
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        interest = request.POST.get('interest')
        future_goals = request.POST.get('future_goals')
        about_me = request.POST.get('about_me')
        skills = request.POST.get('skills')

        # Update User model
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        # Update Profile model
        profile.intrest = interest  # Check spelling: should it be `interest`?
        profile.future_goals = future_goals
        profile.about_me = about_me
        profile.Skills = skills
        profile.save()

        return redirect('/Profile/') 

    return render(request, 'user_profile.html', {'user': user, 'profile': profile})



# teacher side ------------>

@login_required
def teacher_doubts(request):
    if request.user.role != "Teacher":
        return HttpResponseForbidden("You are not authorized")

    doubts = AskDoubts.objects.filter(teacher_select=request.user.first_name)  # Or subject mapping
    return render(request, "teacher_doubt.html", {"doubts": doubts})



@login_required
def answer_doubt(request, doubt_id):
    if request.user.role != "Teacher":
        return HttpResponseForbidden("Not allowed")

    doubt = get_object_or_404(AskDoubts, id=doubt_id)

    if request.method == "POST":
        answer_text = request.POST.get("answer_text")
        answer_file = request.FILES.get("answer_file")

        DoubtAnswer.objects.create(
            doubt=doubt,
            teacher=request.user,
            answer_text=answer_text,
            answer_file=answer_file
        )
        return redirect("teacher_doubts")

    return render(request, "teacher_answer.html", {"doubt": doubt})


@login_required
def my_doubts(request):
    if request.user.role != "Student":
        return HttpResponseForbidden("You are not authorized")

    doubts = AskDoubts.objects.filter(user=request.user).prefetch_related("answers")
    return render(request, "student_answer_dash.html", {"doubts": doubts})
