from django.shortcuts import render, redirect
from scrapping.scrap_script import scap_rightmove
from scrapping.models import ResultProperty
import threading


def home_page(request):
    # print(request.session.get("first_name", "Unknown"))
    # request.session['first_name']

    results_objs = ResultProperty.objects.all()
    context = {
        "results":results_objs,

    }

    return render(request, "index.html", context)




def run_search(request):
    search_link = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=1200&minPrice=900&radius=3.0&includeLetAgreed=false&dontShow=houseShare'
    #search_link = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=1200&minPrice=900&radius=3.0&index=744&includeLetAgreed=false&dontShow=houseShare'
    search_link = 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E87490&minBedrooms=2&maxPrice=1200&minPrice=900&includeLetAgreed=false&dontShow=houseShare'
    t = threading.Thread(target=scap_rightmove, args=(search_link,), kwargs={})
    t.setDaemon(True)
    t.start()
    return redirect('/')


def update_favourites(request):
    print("Updating favourites")
    if request.method == 'POST':
        results_objs = ResultProperty.objects.all()
        for result in results_objs:
            if 'favourite_' + str(result.property_id) in request.POST:
                result.favourite = True
            else:
                result.favourite = False
            if 'best_' + str(result.property_id) in request.POST:
                result.best = True
            else:
                result.best = False

            result.save()

    return redirect('/')

