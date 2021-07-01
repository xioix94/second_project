from django.shortcuts import render
from app.models import Board, Board_Comment

# Create your views here.
def board(request):
    boards = Board.objects.select_related('user')

    return render(request, "app/board.html", {
        'boards': boards
    })