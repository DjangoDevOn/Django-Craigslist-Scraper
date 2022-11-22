
from django.db import IntegrityError
from django.views import generic
from django.shortcuts import redirect, render
from .models import *
from bs4 import BeautifulSoup
import requests
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
import csv





def download_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"' # your filename

    writer = csv.writer(response)
    writer.writerow(['Business Name','Phone', 'Address', 'URL'])

    courses = Account.objects.all().values_list('biz_name','phone', 'address', 'link')

    for course in courses:
        writer.writerow(course)


    return response




class UserSignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'the_app/signup.html'
    success_url = reverse_lazy('dashboard')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,"Username or Password is not correct.")
    return render(request, 'the_app/login.html',{})



def signout(request):
    logout(request)
    return redirect('login')


def dashboard(request):
    # show all posts
    current_prospects = Prospect.objects.all().order_by('-id')
    count = len(current_prospects)
    return render(request, 'the_app/dashboard.html', {'count':count,'current_prospects':current_prospects})

def user(request):
    # show just user posts
    prospects = Prospect.objects.all()
    my_prospects = []
    for prospect in prospects:
        settings = prospect.settings.filter(user=request.user)
        for x in settings:
            my_prospects.append(prospect)
    count = len(my_prospects)
    return render(request, 'the_app/user.html', {'count':count,'my_prospects':my_prospects})

def delete(request, pk):
    prospect = Prospect.objects.get(id=pk)
    settings = prospect.settings.filter(user=request.user)
    for setting in settings:
        prospect.settings.remove(setting)
    prospect.save()

    prospect.users.remove(request.user)
    prospect.save()

    return redirect('user')


def contacted(request, pk):
    settings = Settings.objects.create(
        user=request.user,
        contacted=True,
    )

    public_prospect = Prospect.objects.get(id=pk)
    public_prospect.settings.add(settings)
    public_prospect.save()

    public_prospect.users.add(request.user)
    public_prospect.save()

    return redirect('dashboard')

 

class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Prospect.objects.all()
        query = request.GET.get('q')
        if query:
            object_list = queryset.filter(
                Q(link__icontains=query) |
                Q(post_title__icontains=query)
            ).distinct()

        current_prospects = Prospect.objects.all()
        count = len(current_prospects)
        search_count = len(object_list)

        context = {
            'search_count':search_count,
            'query':query,
            'object_list': object_list,
            'current_prospects':current_prospects,
            'count':count,
        }
        return render(request, 'the_app/dashboard.html', context)




def get_craigslist_prospects(request):
    if request.method == "POST":
        #Defining the getjobpostlinks function
        def getjobpostlinks(webpage):
            response = requests.get(webpage)
            soup = BeautifulSoup(response.content,"html.parser")
            soup_link = soup.findAll("a",{"class":"result-title hdrlnk"})
            soup_meta = soup.findAll("span",{"class":"result-meta"})

            if soup_link:
                for x in range(len(soup_link)):
                    post_title = soup_link[x].text
                    link = soup_link[x]['href']
                    try:
                        meta = soup_meta[x].get_text()
                    except IndexError:
                        meta = ''
                        pass

                    if 'Remote' in post_title:
                        try:
                            prospect = Prospect.objects.create(
                                        link=link,
                                        post_title=post_title,
                                        )
                        except IntegrityError as e:
                            pass

                    if 'home' in post_title:
                        try:
                            prospect = Prospect.objects.create(
                                        link=link,
                                        post_title=post_title,
                                        )
                        except IntegrityError as e:
                            pass


                    if 'work from' in post_title:
                        try:
                            prospect = Prospect.objects.create(
                                        link=link,
                                        post_title=post_title,
                                        )
                        except IntegrityError as e:
                            pass

                    
                    if 'telecommute' in post_title:
                        try:
                            prospect = Prospect.objects.create(
                                        link=link,
                                        post_title=post_title,
                                        )
                        except IntegrityError as e:
                            pass


        cities = [
            "atlanta",
            "austin",
            "boston",
            "chicago",
            "dallas",
            "denver",
            "detroit",
            "houston",
            "lasvegas",
            "losangeles",
            "miami",
            "minneapolis",
            "newyork",
            "orangecounty",
            "philadelphia",
            "phoenix",
            "portland",
            "raleigh",
            "sacramento",
            "sandiego",
            "seattle",
            "sfbay",
            "washingtondc",
            "auburn",
            "bham",
            "columbusga",
            "dothan",
            "shoals",
            "gadsden",
            "huntsville",
            "mobile",
            "montgomery",
            "tuscaloosa",
            "anchorage",
            "fairbanks",
            "kenai",
            "juneau",
            "flagstaff",
            "mohave",
            "phoenix",
            "prescott",
            "showlow",
            "sierravista",
            "tucson",
            "yuma",
            "fayar",
            "fortsmith",
            "jonesboro",
            "littlerock",
            "memphis",
            "texarkana",
            "bakersfield",
            "chico",
            "fresno",
            "goldcountry",
            "hanford",
            "humboldt",
            "imperial",
            "inlandempire",
            "losangeles",
            "mendocino",
            "merced",
            "modesto",
            "monterey",
            "orangecounty",
            "palmsprings",
            "redding",
            "reno",
            "sacramento",
            "sandiego",
            "slo",
            "santabarbara",
            "santamaria",
            "sfbay",
            "siskiyou",
            "stockton",
            "susanville",
            "ventura",
            "visalia",
            "yubasutter",
            "boulder",
            "cosprings",
            "denver",
            "eastco",
            "fortcollins",
            "rockies",
            "pueblo",
            "westslope",
            "newlondon",
            "hartford",
            "newhaven",
            "nwct",
            "allentown",
            "altoona",
            "annapolis",
            "baltimore",
            "cnj",
            "charlottesville",
            "chambersburg",
            "delaware",
            "easternshore",
            "martinsburg",
            "frederick",
            "fredericksburg",
            "harrisburg",
            "harrisonburg",
            "jerseyshore",
            "lancaster",
            "lynchburg",
            "morgantown",
            "norfolk",
            "philadelphia",
            "poconos",
            "reading",
            "richmond",
            "smd",
            "southjersey",
            "pennstate",
            "westmd",
            "williamsport",
            "winchester",
            "york",
            "atlanta",
            "austin",
            "boston",
            "chicago",
            "dallas",
            "detroit",
            "houston",
            "lasvegas",
            "losangeles",
            "miami",
            "minneapolis",
            "orangecounty",
            "portland",
            "raleigh",
            "sandiego",
            "seattle",
            "sfbay",
            "calgary",
            "edmonton",
            "halifax",
            "montreal",
            "ottawa",
            "saskatoon",
            "toronto",
            "vancouver",
            "victoria",
            "winnipeg",
            "longisland",
            "newjersey",
            "scranton",
            "daytona",
            "keys",
            "fortmyers",
            "gainesville",
            "cfl",
            "jacksonville",
            "lakeland",
            "lakecity",
            "ocala",
            "okaloosa",
            "orlando",
            "panamacity",
            "pensacola",
            "sarasota",
            "miami",
            "spacecoast",
            "staugustine",
            "tallahassee",
            "tampa",
            "treasure",
            "albanyga",
            "athensga",
            "augusta",
            "brunswick",
            "macon",
            "nwga",
            "savannah",
            "statesboro",
            "valdosta",
            "boise",
            "eastidaho",
            "lewiston",
            "pullman",
            "spokane",
            "twinfalls",
            "bn",
            "chambana",
            "decatur",
            "lasalle",
            "mattoon",
            "peoria",
            "quadcities",
            "rockford",
            "carbondale",
            "springfieldil",
            "stlouis",
            "quincy",
            "bloomington",
            "evansville",
            "fortwayne",
            "indianapolis",
            "kokomo",
            "tippecanoe",
            "muncie",
            "southbend",
            "terrehaute",
            "ames",
            "cedarrapids",
            "desmoines",
            "dubuque",
            "fortdodge",
            "iowacity",
            "masoncity",
            "omaha",
            "siouxcity",
            "ottumwa",
            "waterloo",
            "kansascity",
            "lawrence",
            "ksu",
            "nwks",
            "salina",
            "seks",
            "swks",
            "topeka",
            "wichita",
            "bgky",
            "cincinnati",
            "eastky",
            "huntington",
            "lexington",
            "louisville",
            "owensboro",
            "westky",
            "batonrouge",
            "cenla",
            "houma",
            "lafayette",
            "lakecharles",
            "monroe",
            "neworleans",
            "shreveport",
            "binghamton",
            "capecod",
            "catskills",
            "newlondon",
            "glensfalls",
            "hudsonvalley",
            "ithaca",
            "nh",
            "nwct",
            "oneonta",
            "plattsburgh",
            "potsdam",
            "southcoast",
            "syracuse",
            "utica",
            "watertown",
            "westernmass",
            "worcester",
            "chambersburg",
            "smd",
            "westmd",
            "capecod",
            "westernmass",
            "worcester",
            "annarbor",
            "battlecreek",
            "centralmich",
            "detroit",
            "flint",
            "grandrapids",
            "holland",
            "jxn",
            "kalamazoo",
            "lansing",
            "muskegon",
            "nmi",
            "porthuron",
            "saginaw",
            "swmi",
            "thumb",
            "up",
            "bemidji",
            "brainerd",
            "duluth",
            "fargo",
            "mankato",
            "minneapolis",
            "rmn",
            "marshall",
            "stcloud",
            "gulfport",
            "hattiesburg",
            "meridian",
            "northmiss",
            "natchez",
            "columbiamo",
            "joplin",
            "kirksville",
            "loz",
            "semo",
            "stjoseph",
            "billings",
            "bozeman",
            "butte",
            "montana",
            "greatfalls",
            "helena",
            "kalispell",
            "missoula",
            "asheville",
            "boone",
            "charlotte",
            "eastnc",
            "greensboro",
            "hickory",
            "outerbanks",
            "raleigh",
            "wilmington",
            "winstonsalem",
            "grandisland",
            "lincoln",
            "northplatte",
            "scottsbluff",
            "elko",
            "lasvegas",
            "cnj",
            "albuquerque",
            "clovis",
            "farmington",
            "lascruces",
            "roswell",
            "santafe",
            "buffalo",
            "chautauqua",
            "elmira",
            "fingerlakes",
            "plattsburgh",
            "potsdam",
            "twintiers",
            "utica",
            "bismarck",
            "grandforks",
            "akroncanton",
            "ashtabula",
            "chillicothe",
            "cleveland",
            "columbus",
            "dayton",
            "limaohio",
            "mansfield",
            "wheeling",
            "parkersburg",
            "sandusky",
            "toledo",
            "tuscarawas",
            "youngstown",
            "zanesville",
            "lawton",
            "enid",
            "oklahomacity",
            "stillwater",
            "texoma",
            "tulsa",
            "bend",
            "corvallis",
            "eastoregon",
            "eugene",
            "klamath",
            "medford",
            "oregoncoast",
            "roseburg",
            "salem",
            "altoona",
            "erie",
            "allentown",
            "meadville",
            "pittsburgh",
            "scranton",
            "charleston",
            "columbia",
            "florencesc",
            "greenville",
            "hiltonhead",
            "myrtlebeach",
            "nesd",
            "csd",
            "rapidcity",
            "siouxfalls",
            "chattanooga",
            "clarksville",
            "cookeville",
            "knoxville",
            "nashville",
            "tricities",
            "abilene",
            "amarillo",
            "beaumont",
            "brownsville",
            "collegestation",
            "corpuschristi",
            "dallas",
            "nacogdoches",
            "delrio",
            "elpaso",
            "galveston",
            "killeen",
            "laredo",
            "lubbock",
            "mcallen",
            "odessa",
            "sanangelo",
            "sanantonio",
            "sanmarcos",
            "bigbend",
            "easttexas",
            "waco",
            "wichitafalls",
            "logan",
            "ogden",
            "provo",
            "saltlakecity",
            "stgeorge",
            "elmira",
            "danville",
            "blacksburg",
            "norfolk",
            "roanoke",
            "swva",
            "bellingham",
            "kpr",
            "moseslake",
            "olympic",
            "seattle",
            "skagit",
            "wenatchee",
            "yakima",
            "martinsburg",
            "swv",
            "wv",
            "appleton",
            "eauclaire",
            "greenbay",
            "janesville",
            "racine",
            "lacrosse",
            "madison",
            "milwaukee",
            "northernwi",
            "sheboygan",
            "wausau",
            "csd",
            "cosprings",
            "eastco",
            "fortcollins",
            "ogden",
            "provo",
            "rapidcity",
            "saltlakecity",
            "scottsbluff"
        ]


        # find all locales and loop through them
        for city in cities:
            # Get City Posts in Each Category I Need
            getjobpostlinks('https://' + city + '.craigslist.org/search/cpg')
            getjobpostlinks('https://' + city + '.craigslist.org/search/sof')
            getjobpostlinks('https://' + city + '.craigslist.org/search/web')
  
        current_prospects = Prospect.objects.all()
        count = len(current_prospects)
        return render(request, 'the_app/get-prospects.html', {'count':count,'current_prospects':current_prospects})

    current_prospects = Prospect.objects.all()
    count = len(current_prospects)
    return render(request, 'the_app/get-prospects.html', {'count':count,'current_prospects':current_prospects})





 