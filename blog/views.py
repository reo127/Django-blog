from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComments
from django.contrib import messages
from django.contrib.auth.models import User
from blog.templatetags import extras

# Create your views here.

def blogHome(request):
    allPost = Post.objects.all()
    context = {"allPost":allPost}
    return render(request, 'blog/blogHome.html', context)



def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()

    comments = BlogComments.objects.filter(post=post, parent=None)
    replies = BlogComments.objects.filter(post=post).exclude(parent=None)
    repyDict = {}
    for reply in replies:
        if reply.parent.sno not in repyDict.keys():
            repyDict[reply.parent.sno] = [reply]
        else:
            repyDict[reply.parent.sno].append(reply)

    context = {'post':post, 'comments':comments, 'user': request.user, 'repyDict':repyDict}
    return render(request, 'blog/blogPost.html', context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno =request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)

        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComments(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")

        else:
            parent = BlogComments.objects.get(sno=parentSno)
            comment = BlogComments(comment= comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    
        
    return redirect(f"/blog/{post.slug}")

