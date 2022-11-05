
from django.shortcuts import render, redirect
from .models import Live, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.


def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")

    if kw:
        if cate == "prod":
            b = Live.objects.filter(product__startswith=kw)
        elif cate == "sel":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Live.objects.filter(liseller=u)
            except:
                b = Live.objects.none()
        elif cate == "con":
            b = Live.objects.filter(content__contains=kw)
        else:
            b = Live.objects.none()
    else:
        b = Live.objects.all()

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "bset": obj,
        "cate": cate,
        "kw": kw,
        "b": b
    }
    return render(request, "live/index.html", context)




def update(request, bpk):
    b = Live.objects.get(id=bpk)

    if b.seller != request.user:
        return redirect("live:index")

    if request.method == "POST":
        s = request.POST.get("prod")
        sc = request.POST.get("scon")
        c = request.POST.get("con")
        b.title = s
        b.content = c
        b.shortcon = sc
        b.save()
        return redirect("live:detail", bpk)
    context = {
        "b":b
    }
    return render(request, "live/update.html", context)

def create(request):
    if request.method == "POST":
        t = request.POST.get("prod")
        ct = request.POST.get("cate")
        sc = request.POST.get("scon")
        c = request.POST.get("con")
        pi = request.FILES.get("pic")
        pr = request.POST.get("price")
        # cate = Product.objects.get(name=cate)
        # print(Product.cate_choice)
        Live(title=t, price=pr, cate = ct,  content=c, video=pi, shortcon= sc,
        seller=request.user, pubdate=timezone.now()).save()
        # print(Product.objects.all())
        return redirect("live:index")
    cate = Live.category_choice
    context = { 
        "cate" : cate
    }
    return render(request, "live/create.html", context)

def delete(request, bpk):
    b = Live.objects.get(id=bpk)
    if request.user == b.seller:        
        b.video.delete()
        b.delete()
    else:
        pass 
    return redirect("live:index")



def dreview(request, bpk, rpk):
    c = Reply.objects.get(id=rpk)
    if c.viewer == request.user:
        c.delete()
    else:
        pass 
    return redirect("live:detail", bpk)


def creview(request, bpk):
    p = Live.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(title=p, viewer=request.user, livecomment=c).save()
    return redirect("live:detail", bpk)


def detail(request, bpk):
    b = Live.objects.get(id=bpk)
    c = b.reply_set.all()
    context = {
        "b": b,
        "cset" : c
    }
    b.viewcount += 1
    b.save()
    
    return render(request, "live/detail.html", context )


def detail2(request):
    return render(request,"live/detail2.html")