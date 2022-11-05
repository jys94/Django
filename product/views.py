
from django.shortcuts import render, redirect
from .models import Product, Review
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
            b = Product.objects.filter(product__startswith=kw)
        elif cate == "sel":
            from acc.models import User
            try:
                u = User.objects.get(username=kw)
                b = Product.objects.filter(seller=u)
            except:
                b = Product.objects.none()
        elif cate == "con":
            b = Product.objects.filter(content__contains=kw)
        else:
            b = Product.objects.none()
    else:
        b = Product.objects.all()

    pag = Paginator(b, 5)
    obj = pag.get_page(pg)
    context = {
        "bset": obj,
        "cate": cate,
        "kw": kw,
        "b": b
    }
    return render(request, "product/index.html", context)




def update(request, bpk):
    b = Product.objects.get(id=bpk)

    if b.seller != request.user:
        return redirect("product:index")

    if request.method == "POST":
        s = request.POST.get("prod")
        sc = request.POST.get("scon")
        c = request.POST.get("con")
        b.product = s
        b.content = c
        b.shortcon = sc
        b.save()
        return redirect("product:detail", bpk)
    context = {
        "b":b
    }
    return render(request, "product/update.html", context)

def create(request):
    if request.method == "POST":
        p = request.POST.get("prod")
        ct = request.POST.get("cate")
        sc = request.POST.get("scon")
        c = request.POST.get("con")
        pi = request.FILES.get("pic")
        pr = request.POST.get("price")
        # cate = Product.objects.get(name=cate)
        # print(Product.cate_choice)
        Product(product=p, price=pr, cate = ct,  content=c, picture=pi, shortcon= sc,
        seller=request.user, pubdate=timezone.now()).save()
        # print(Product.objects.all())
        return redirect("product:index")
    cate = Product.category_choice
    context = { 
        "cate" : cate
    }
    print(context)
    return render(request, "product/create.html", context)

def delete(request, bpk):
    b = Product.objects.get(id=bpk)
    if request.user == b.seller:        
        b.picture.delete()
        b.delete()
    else:
        pass 
    return redirect("product:index")



def dreview(request, bpk, rpk):
    c = Review.objects.get(id=rpk)
    if c.replyer == request.user:
        c.delete()
    else:
        pass 
    return redirect("product:detail", bpk)


def creview(request, bpk):
    p = Product.objects.get(id=bpk)
    c = request.POST.get("com")
    Review(product=p, replyer=request.user, comment=c).save()
    return redirect("product:detail", bpk)


def detail(request, bpk):
    b = Product.objects.get(id=bpk)
    c = b.review_set.all()
    context = {
        "b": b,
        "cset" : c
    }
    b.viewcount += 1
    b.save()
    return render(request, "product/detail.html", context )