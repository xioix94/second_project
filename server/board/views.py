from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from app.models import Category, User
from django.shortcuts import redirect, render
from app.models import Board, Board_Comment
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def board(request):
    # 카테고리 필터
    category = request.GET.get('category')
    if category in ['beer', 'wine', 'cocktail']:
        category = Category.objects.get(name=category)
        Post = Board.objects.filter(category_id=category.id)
        category = category.name
    else:
        category = 'All'
        Post = Board.objects.all()
    
    #성준's 검색필터 적용
    keyword = request.GET.get('keyword')
    if not keyword:
        keyword = ""
    else:
        Post = Board.objects\
            .filter(content__icontains = keyword)

    boards = Post.select_related().order_by('-time')
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
        'category': category,
        'pagination' : range(start_page, end_page + 1),
        'boards': boards,
        'keyword': keyword
    })

@csrf_exempt
def single(request):
    print("views.py board/single")
    
    if request.method == 'GET':
        print("views.py board/single 'GET'")
        board_id = request.GET.get('id')
        print(board_id)
        board = Board.objects.select_related().get(id=board_id)
        board_comments = Board_Comment.objects.filter(board_id=board_id).select_related('user')

        return render(request, "app/board_single.html", {
            'board': board,
            'board_comments': board_comments,
            'board_id': board_id,
        })

    else:
        print("views.py board/single 'POST'")
        if not request.session.get('email'):
            print("views.py board/single 'not email session'")
            return JsonResponse({
                'result': 'Fail',
                'messages': 'go back',
            })
        
        else:
            print("views.py board/single 'email session'")
            comment = request.POST['comment']
            print(comment)

            try:
                print(request)
                board_id = request.GET.get('id')
                print(board_id)
                email = request.session.get('email')
                print(email)
                user = User.objects.get(email=email)
                print(user.id)

                # db에 저장
                board_comment = Board_Comment(content=comment, time=timezone.now(), board_id=board_id, user_id=user.id)
                print(board_comment)
                board_comment.save()

                result = "Success"
                messages = "Board comment save succeeded."
                
                return JsonResponse({'result': result, 'messages': messages})

            except:
                result = "Fail"
                messages = "Board comment save failed."
                return JsonResponse({
                    'result': 'Fail',
                    'messages': 'error',
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
            time =  timezone.now(),
            mainphoto =request.FILES['mainphoto'],
        )
        new_board.save() 
        return HttpResponseRedirect('/board/')

    return render(request, 'app/freewrite.html')

def board_delete(request):
    pass