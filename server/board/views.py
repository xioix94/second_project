from django.shortcuts import render
from app.models import Board_Comment

# Create your views here.
def board(request):
    board_comments = Board_Comment.objects.all().select_related()

    return render(request, "app/board.html", {
        'board_comments': board_comments
    })