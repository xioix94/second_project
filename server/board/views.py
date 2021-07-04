from django.http.response import HttpResponse, HttpResponseRedirect
from app.models import Category, User
from django.shortcuts import redirect, render
from app.models import Board, Board_Comment
from django.core.paginator import Paginator
from django.utils import timezone

# Create your views here.
def board(request):
    boards = Board.objects.select_related('user')

    page = request.GET.get('page')

    if not page:
        page = '1'
    
    p = Paginator(boards, 10)
    
    u_c = p.page(page)

    start_page = (int(page) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > p.num_pages:
        end_page = p.num_pages

    return render(request, "app/board.html", {
        'u_c' : u_c,
        'pagination' : range(start_page, end_page + 1),
        'boards': boards
    })

def single(request):
    board_id = request.GET.get('id')
    board = Board.objects.select_related().get(id=board_id)
    board_comments = Board_Comment.objects.filter(board_id=board_id).select_related('user')

    return render(request, "app/board_single.html", {
        'board': board,
        'board_comments': board_comments,
    })

def board_write(request):
    if request.method == 'GET':
        if request.session.get('email'):
            return render(request, 'app/freewrite.html', {})
        else:
            return redirect('/login/')
    elif request.method == 'POST':
        user_email = request.session['email']
        user_id = User.objects.get(email=user_email)
        new_board = Board(
            user_id = user_id.id,
            category_id = request.POST['category'],
            title = request.POST['postname'],
            content = request.POST['contents'],
            time =  timezone.now()
        )
        new_board.save() 
        return HttpResponseRedirect('/board/')

    return render(request, 'app/freewrite.html')