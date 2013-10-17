
from datetime import timedelta

from django.contrib.auth.models import User
from django.contrib.messages import info, error
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.views.generic import ListView, CreateView, DetailView

from mezzanine.conf import settings
from mezzanine.generic.models import ThreadedComment
from mezzanine.utils.views import paginate

from .models import Link
from .utils import order_by_score


class UserFilterView(ListView):
    """
    List view that puts a ``profile_user`` variable into the context,
    which is optionally retrieved by a ``username`` urlpattern var.
    If a user is loaded, ``object_list`` is filtered by the loaded
    user. Used for showing lists of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(UserFilterView, self).get_context_data(**kwargs)
        try:
            username = self.kwargs["username"]
        except KeyError:
            profile_user = None
        else:
            users = User.objects.select_related("profile")
            lookup = {"username__iexact": username, "is_active": True}
            profile_user = get_object_or_404(users, **lookup)
            qs = context["object_list"].filter(user=profile_user)
            context["object_list"] = qs
        context["profile_user"] = profile_user
        context["no_data"] = ("None yet.")
        return context


class ScoreOrderingView(UserFilterView):
    """
    List view that optionally orders ``object_list`` by calculated
    score. Subclasses must defined a ``date_field`` attribute for the
    related model, that's used to determine time-scaled scoring.
    Ordering by score is the default behaviour, but can be
    overridden by passing ``False`` to the ``by_score`` arg in
    urlpatterns, in which case ``object_list`` is sorted by most
    recent, using the ``date_field`` attribute. Used for showing lists
    of links and comments.
    """

    def get_context_data(self, **kwargs):
        context = super(ScoreOrderingView, self).get_context_data(**kwargs)
        qs = context["object_list"]
        context["by_score"] = self.kwargs.get("by_score", True)
        if context["by_score"]:
            qs = order_by_score(qs, self.score_fields, self.date_field)
        else:
            qs = qs.order_by("-" + self.date_field)
        context["object_list"] = paginate(qs, self.request.GET.get("page", 1),
            settings.ITEMS_PER_PAGE, settings.MAX_PAGING_LINKS)
        context["title"] = self.get_title(context)
        return context


class LinkView(object):
    """
    List and detail view mixin for links - just defines the correct
    queryset.
    """
    def get_queryset(self):
        return Link.objects.published().select_related("user", "user__profile")


class LinkList(LinkView, ScoreOrderingView):
    """
    List view for links, which can be for all users (homepage) or
    a single user (links from user's profile page). Links can be
    order by score (homepage, profile links) or by most recently
    created ("new" main nav item).
    """

    date_field = "publish_date"
    score_fields = ("rating_sum", "comments_count")

    def get_title(self, context):
        if context["by_score"]:
            return ""  # Homepage
        if context["profile_user"]:
            return "Links by %s " % context["profile_user"].profile
        else:
            return "Newest Links"


# =todo: refactor into LinkList view =============
class AskLinkView(object):
    """
    View for Links with the link field blank, used for 'Ask FN:'
    Questions. =todo: We can probably refactor this into the LinkList view.
    """
    def get_queryset(self):
        return Link.objects.published().filter(link='').select_related("user", "user__profile")

# =todo: refactor into LinkList view =============
class AskLinkList(AskLinkView, ScoreOrderingView):
    """
    View for Links with the link field blank, used for 'Ask FN:'
    Questions. =todo: We can probably refactor this into the LinkList view.
    """

    date_field = "publish_date"
    score_fields = ("rating_sum", "comments_count")

    def get_title(self, context):
        return "Questions"

        

class LinkCreate(CreateView):
    """
    Link creation view - assigns the user to the new link, as well
    as setting Mezzanine's ``gen_description`` attribute to ``False``,
    so that we can provide our own descriptions.
    """

    form_class = modelform_factory(Link, fields=("title", "link",
                                                 "description"))
    model = Link

    def form_valid(self, form):
        hours = getattr(settings, "ALLOWED_DUPLICATE_LINK_HOURS", None)
        
        # Changed permalinks to pk instead of slug
        # so users can leave the URL field blank and ask questions,
        # so we need to check whether the link field is blank before
        # doing the check for duplicate links.
        if form.instance.link:
            
            if hours:
                lookup = {
                    "link": form.instance.link,
                    "publish_date__gt": now() - timedelta(hours=hours),
                }
                try:
                    link = Link.objects.get(**lookup)
                except Link.DoesNotExist:
                    pass            
                else:
                    error(self.request, "Link exists")
                    return redirect(link)
        form.instance.user = self.request.user
        form.instance.gen_description = False
        info(self.request, "Entry created")
        return super(LinkCreate, self).form_valid(form)
    
    # variables for post to food news bookmarklet
    def get_context_data(self, **kwargs):
        context = super(LinkCreate, self).get_context_data(**kwargs)
        context['u'] = self.request.GET.get('u', '')
        context['t'] = self.request.GET.get('t', '')
        return context


class LinkDetail(LinkView, DetailView):
    """
    Link detail view - threaded comments and rating are implemented
    in its template.
    """
    pass


class CommentList(ScoreOrderingView):
    """
    List view for comments, which can be for all users ("comments" and
    "best" main nav items) or a single user (comments from user's
    profile page). Comments can be order by score ("best" main nav item)
    or by most recently created ("comments" main nav item, profile
    comments).
    """

    date_field = "submit_date"
    score_fields = ("rating_sum",)

    def get_queryset(self):
        return ThreadedComment.objects.visible().select_related("user",
            "user__profile").prefetch_related("content_object")

    def get_title(self, context):
        if context["profile_user"]:
            return "Comments by %s" % context["profile_user"].profile
        elif context["by_score"]:
            return "Best Comments"
        else:
            return "Latest Comments"


# =feeds ===================================

class RssFeed(Feed):
    title = "Food News"
    link = "http://food.hypertexthero.com"
    description = "Links about healthy sustainable food, ranked by readers."
    # description_template = "hth/feed_description.html" # using default for now

    def items(self):
        return Link.objects.filter(status=2).order_by('publish_date')[:30]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish_date

    def item_description(self, item):
        # return smart_truncate(item.body_html)
        return item.description

class AtomFeed(RssFeed):
    feed_type = Atom1Feed
    subtitle = RssFeed.description