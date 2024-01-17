from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from .utils import get_mongodb
from .models import Tag, Author, Quote
from .forms import QuoteForm, AuthorForm


def main(request, page=1):
    db = get_mongodb()

    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(
        request,
        "quotes/index.html",
        context={"quotes": quotes_on_page},
    )


def quote(request):
    authors = Author.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            tag_name = request.POST.get("tag")
            Tag.objects.get_or_create(name=tag_name)

            author_name = request.POST.get("author")
            quote = request.POST.get("quote")
            author = Author.objects.get(fullname=author_name)

            instance = Quote.objects.create(author_id=author.id, quote=quote)

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tag"))
            for tag in choice_tags.iterator():
                instance.tags.add(tag)

            return redirect(to="quotes:root")
        else:
            return render(
                request,
                "quotes/quote.html",
                {"authors": authors, "tags": tags, "form": form},
            )

    return render(
        request,
        "quotes/quote.html",
        {
            "authors": authors,
            "tags": tags,
            "form": QuoteForm(),
        },
    )


def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/add_author.html", {"form": form})

    return render(request, "quotes/add_author.html", {"form": AuthorForm()})
