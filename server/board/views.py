from django.shortcuts import render
from app.models import Board, Board_Comment

# Create your views here.
def board(request):
    boards = Board.objects.select_related('user')

    return render(request, "app/board.html", {
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