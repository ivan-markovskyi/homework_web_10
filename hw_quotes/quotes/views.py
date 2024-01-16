from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from .utils import get_mongodb
from .models import Tag, Author
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

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_authors = Author.objects.filter(
                fullname__in=request.POST.getlist("authors")
            )
            for author in choice_authors.iterator():
                new_quote.author.add(author)

            return redirect(to="quotes:root")
        else:
            return render(
                request, "quotes/quote.html", {"authors": authors, "form": form}
            )

    return render(
        request, "quotes/quote.html", {"authors": authors, "form": QuoteForm()}
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
