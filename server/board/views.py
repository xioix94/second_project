from app.models import Category, User
from .forms import BoardForm
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
    if not request.session['email']:
        return redirect('/login')

    if request.method == "GET":
        form = BoardForm()

    elif request.method == "POST":
        form = BoardForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('user')
            user = User.objects.get(pk = user_id)
            new_board = Board(
                user = user,
                category = form.cleaned_data['category'],
                title = form.cleaned_data['title'],
                content = form.cleaned_data['contents'],
                time =  timezone.now()
            )
            new_board.save()
            return redirect('/board/')

    return render(request, 'app/freewrite.html', {'form' :form})