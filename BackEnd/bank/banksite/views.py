# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, Http404
from banksite.models import User
import json

def login_page(request):
    return render_to_response('banksite/login.html', context_instance=RequestContext(request))


def check_user(request):
    post = request.POST
    try:
        user = User.objects.get(uid=post['uid'])
    except (Exception):
        return {
            'success': False,
            'msg': 'The User ID you entered is not correct.'
        }
    else:
        if user.password != post['password']:
            return {
                'success': False,
                'msg': 'The Password you entered is not correct.'
            }
        return {
            'success': True
        }


def login_check(request):
    return HttpResponse(json.dumps(check_user(request)), mimetype='application/json')


def login(request):
    check_result = check_user(request)
    if not check_result['success']:
        raise Http404
    uid = request.POST['uid']
    request.session['uid'] = uid
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return redirect('accounts')


def accounts(request):
    return render_to_response('banksite/accounts.html', {'uid': request.session['uid']},
        context_instance=RequestContext(request))


def logout(request):
    try:
        del request.session['uid']
    except KeyError:
        pass
    return redirect('login_page')