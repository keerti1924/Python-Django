from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from coder.models import *

from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from razorpay.errors import SignatureVerificationError
from django.db.models import Sum
from .settings import *
from time import time
import razorpay

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def BASE(request):
    return render(request, 'base.html')


def Home(request):
    category = Categories.objects.all().order_by('id')[0:8]
    course = Course.objects.filter(status='PUBLISH').order_by('id')

    context = {
        'category': category,
        'course': course,
    }

    return render(request, 'index.html', context)


def About(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }

    return render(request, 'main/about.html', context)


def Contact_us(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        messages.success(request, 'Thanks for Contact us !')
        return redirect('contact')

    return render(request, 'main/contact.html')


def instructor(request):
    return render(request, 'main/instructor.html')


def form(request):
    return render(request, 'main/form.html')


def courses(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    Free_Course_count = Course.objects.filter(price=0).count()
    Paid_Course_count = Course.objects.filter(price__gte=1).count()

    context = {
        'category': category,
        'level': level,
        'course': course,
        'Free_Course_count': Free_Course_count,
        'Paid_Course_count': Paid_Course_count,
    }
    return render(request, 'main/courses.html', context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')

    if price == ['pricefree']:
        course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
        course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
        course = Course.objects.all()
    elif category:
        course = Course.objects.filter(
            category__id__in=category).order_by('-id')
    elif level:
        course = Course.objects.filter(
            level__id__in=level).order_by('-id')
    else:
        course = Course.objects.all().order_by('-id')

    context = {
        'course': course,
    }

    t = render_to_string('ajax/course.html', context)
    return JsonResponse({'data': t})


def testimonial(request):
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'main/testimonial.html', context)


@login_required(login_url='login')
def create_review(request):
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'main/create_review.html', context)


@login_required(login_url='login')
def add_review(request):

    if request.method == 'POST':
        re = Review()
        re.name = request.POST.get('name')
        re.review = request.POST.get('review')

        re.save()
        messages.success(request, 'Thanks for your Review !')
        return redirect('testimonial')

    return render(request, "main/testimonial.html")


def team(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }

    return render(request, 'main/team.html', context)


def pagenotfound(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category': category,
    }

    return render(request, 'error/404.html', context)


def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    category = Categories.get_all_category(Categories)

    context = {
        'course': course,
        'category': category,
    }
    return render(request, 'search/search.html', context)


@login_required(login_url='login')
def course_details(request, slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(
        course__slug=slug).aggregate(sum=Sum('time_duration'))

    course_id = Course.objects.get(slug=slug)
    course = Course.objects.filter(slug=slug)
    course_comment = get_object_or_404(Course, slug=slug)
    comments = Comment.objects.filter(course=course_comment)
    try:
        check_enroll = UserCourse.objects.get(
            user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    if course.exists():
        course = course.first()
    else:
        return redirect('404')

    context = {
        'course': course,
        'category': category,
        'time_duration': time_duration,
        'check_enroll': check_enroll,
        'comments': comments,
    }

    return render(request, 'course/course_details.html', context)


@login_required(login_url='login')
def checkout(request, slug):
    course = Course.objects.get(slug=slug)
    action = request.GET.get('action')
    order = None

    if course.price == 0:
        course = UserCourse(
            user=request.user,
            course=course,
        )
        course.save()
        messages.success(request, 'Course is successfully Enrolled !.')
        return redirect('my-course')
    elif action == 'create_payment':
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            amount = (course.price * 100)
            currency = 'INR'
            notes = {
                'name': f'{first_name} {last_name}',
                'country': country,
                'address': f'{address1} {address2}',
                'city': city,
                'state': state,
                'postcode': postcode,
                'phone': phone,
                'email': email,
                'order_comments': order_comments,
            }
            receipt = f"SecretCoder-{int(time())}"
            order = client.order.create({
                'receipt': receipt,
                'notes': notes,
                'currency': currency,
                'amount': amount,
            })
            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
            )
            payment.save()

    context = {
        'course': course,
        'order': order,
    }

    return render(request, 'checkout/checkout.html', context)


@csrf_exempt
def verify_payment(request):
    payment = Payment.objects.all()
    if request.method == "POST":
        data = request.POST
        print(data)
        try:
            client.utility.verify_payment_signature(data)
            razorpay_order_id = data['razorpay_order_id']
            razorpay_payment_id = data['razorpay_payment_id']

            payment = Payment.objects.get(order_id=razorpay_order_id)
            payment.payment_id = razorpay_payment_id
            payment.status = True

            usercourse = UserCourse(
                user=payment.user,
                course=payment.course,
            )

            usercourse.save()
            payment.user_course = usercourse
            payment.save()

            context = {
                'data': data,
                'payment': payment,
            }
            return render(request, 'verify_payment/success.html', context)
        except SignatureVerificationError as e:
            print(f"Signature Verification Error: {e}")
            return render(request, 'verify_payment/fail.html')
        except Payment.DoesNotExist:
            return HttpResponse("Invalid request method")


@login_required(login_url='login')
def my_course(request):
    course = UserCourse.objects.filter(user=request.user)
    category = Categories.get_all_category(Categories)

    context = {
        'course': course,
        'category': category,
    }

    return render(request, 'course/my_course.html', context)


@login_required(login_url='login')
def watch_course(request, slug):
    lecture = request.GET.get('lecture')
    course = Course.objects.filter(slug=slug)

    if lecture is None:
        lecture = 1
    video = Video.objects.get(id=lecture)

    try:
        if course.exists():
            course = course.first()
        else:
            return redirect('404')
    except UserCourse.DoesNotExist:
        return redirect('404')

    context = {
        'course': course,
        'video': video,
        'lecture': lecture,

    }

    return render(request, 'course/watch_course.html', context)


@login_required(login_url='login')
def add_comment(request, id):
    course = Course.objects.get(id=id)
    if request.method == 'POST':
        rating = request.POST['rating']
        content = request.POST['content']
        Comment(course_id=course.id, user_id=request.user.id,
                rating=rating, content=content).save()
        messages.success(request, 'Thanks for your review!.')
        return redirect("my-course")


@login_required(login_url='login')
def editor(request):
    return render(request, 'main/editor.html')


def tc(request):
    return render(request, 'footer/t&c.html')


def faq(request):
    return render(request, 'footer/faq.html')


def privacy_policy(request):
    return render(request, 'footer/privacy.html')


@login_required(login_url='login')
def success(request):
    payment = Payment.objects.all()
    context = {
        'payment': payment,
    }
    return render(request, 'verify_payment/success.html', context)


@login_required(login_url='login')
def subscriber(request):
    if request.method == 'POST':
        subs = Subscriber()
        email = request.POST.get('email')

        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already exists!')
            return redirect('home')

        subs.email = email
        subs.save()
        messages.success(request, 'Thanks for Subscribing us !')
        return redirect('home')
