from django.shortcuts import render,redirect
from doubt.models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


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
                    return redirect("/Student_home/")

                elif user.role == "Teacher":
                    return redirect("/Student_home/")

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

    


def student_dashboard(request):
    teacher_count = CustomUser.objects.filter(role__iexact='teacher').count()
    student_count = CustomUser.objects.filter(role__iexact='student').count()
    solved_answers = 120  

    context = {
        'teacher_count': teacher_count,
        'student_count': student_count,
        'solved_answers': solved_answers,
    }
    return render(request,"student_dashboard.html",context)



