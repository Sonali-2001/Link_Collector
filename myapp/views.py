from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import Link

def scrape(request):
    if request.method == "POST":
        site = request.POST.get('site', '').strip().strip("'\"")
        try:
            # Ensure valid URL schema
            if not site.startswith('http://') and not site.startswith('https://'):
                site = 'http://' + site

            # Fetch page content
            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')

            # Clear old links (optional)
            Link.objects.all().delete()

            # Extract and store links
            for link in soup.find_all('a'):
                link_address = link.get('href')
                link_text = link.string

                if link_address:  # only save valid links
                    Link.objects.create(
                        address=link_address,
                        name=link_text or "No Text"
                    )

        except Exception as e:
            return render(request, 'myapp/result.html', {
                'data': [],
                'error': f"Error: {e}"
            })

    # Always render data
    data = Link.objects.all()
    return render(request, 'myapp/result.html', {'data': data})


def clear(request):
    Link.objects.all().delete()
    return render(request, 'myapp/result.html', {'data': []})
