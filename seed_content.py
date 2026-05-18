import os
import django
from django.utils.text import slugify

# Load .env file
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                try:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
                except ValueError:
                    pass

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "is_homepage.settings.dev")
django.setup()

from wagtail.models import Page
from is_homepage.apps.home.models import HomePage
from is_homepage.apps.news.models import NewsIndexPage, NewsDetailPage
from is_homepage.apps.case_studies.models import CaseStudiesIndexPage, CaseStudiesDetailPage
from is_homepage.apps.innovation_guides.models import InnovationGuidesIndexPage, InnovationGuidesStagePage, InnovationGuidesDetailPage
from is_homepage.apps.innovation_guides.snippets import InnovationGuidesStageSnippet
from is_homepage.apps.generic.models import GenericPage

def get_or_create_index(parent, model, title, slug):
    index = model.objects.first()
    if not index:
        index = model(
            title=title,
            slug=slug,
            search_description=f"Dummy {title} index page",
        )
        parent.add_child(instance=index)
        index.save_revision().publish()
        print(f"Created {title} Index Page")
    else:
        print(f"{title} Index Page already exists")
    return index

def generate_content():
    # 1. Get Home Page
    home = HomePage.objects.first()
    if not home:
        print("Home page not found!")
        home = Page.objects.get(id=3) # Typical ID for Home
        if not home:
            print("Root page (id=3) not found!")
            return

    # 2. News
    news_index = get_or_create_index(home, NewsIndexPage, "News", "news")
    for i in range(1, 11):
        title = f"Dummy News Article {i}"
        slug = slugify(title)
        if not NewsDetailPage.objects.filter(slug=slug).exists():
            detail = NewsDetailPage(title=title, slug=slug, search_description=f"Dummy description for news {i}")
            news_index.add_child(instance=detail)
            detail.save_revision().publish()
            print(f"Created: {title}")

    # 3. Case Studies
    cs_index = get_or_create_index(home, CaseStudiesIndexPage, "Case Studies", "case-studies")
    for i in range(1, 11):
        title = f"Dummy Case Study {i}"
        slug = slugify(title)
        if not CaseStudiesDetailPage.objects.filter(slug=slug).exists():
            detail = CaseStudiesDetailPage(title=title, slug=slug, search_description=f"Dummy description for case study {i}")
            cs_index.add_child(instance=detail)
            detail.save_revision().publish()
            print(f"Created: {title}")

    # 4. Innovation Guides
    ig_index = get_or_create_index(home, InnovationGuidesIndexPage, "Innovation Guides", "innovation-guides")
    
    # Need a snippet for the stage
    stage_snippet, _ = InnovationGuidesStageSnippet.objects.get_or_create(name="Dummy Stage", defaults={"sort_order": 1})
    
    # Need a stage page
    stage_page = InnovationGuidesStagePage.objects.first()
    if not stage_page:
        stage_page = InnovationGuidesStagePage(
            title="Dummy Stage Page",
            slug="dummy-stage-page",
            search_description="Dummy stage description",
            stage=stage_snippet
        )
        ig_index.add_child(instance=stage_page)
        stage_page.save_revision().publish()
        print("Created Innovation Guides Stage Page")
    
    for i in range(1, 11):
        title = f"Dummy Innovation Guide {i}"
        slug = slugify(title)
        if not InnovationGuidesDetailPage.objects.filter(slug=slug).exists():
            detail = InnovationGuidesDetailPage(
                title=title, 
                slug=slug, 
                search_description=f"Dummy description for guide {i}",
                stage=stage_snippet
            )
            stage_page.add_child(instance=detail)
            detail.save_revision().publish()
            print(f"Created: {title}")

    # 5. Generic Pages
    for i in range(1, 11):
        title = f"Dummy Generic Page {i}"
        slug = slugify(title)
        if not GenericPage.objects.filter(slug=slug).exists():
            detail = GenericPage(title=title, slug=slug, search_description=f"Dummy description for generic page {i}")
            home.add_child(instance=detail)
            detail.save_revision().publish()
            print(f"Created: {title}")

if __name__ == "__main__":
    generate_content()
