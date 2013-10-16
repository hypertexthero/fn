
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from .views import AskLinkList, LinkList, LinkCreate, LinkDetail, CommentList,\
RssFeed, AtomFeed


urlpatterns = patterns("",
    url("^$",
        LinkList.as_view(),
        name="home"),
    url("^new/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_latest"),
    url("^ask/$",
        AskLinkList.as_view(),
        name="link_list_ask"),
    url("^comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_latest"),
    url("^best/$",
        CommentList.as_view(),
        name="comment_list_best"),
    url("^link/create/$",
        login_required(LinkCreate.as_view()),
        name="link_create"),
    # url("^link/(?P<slug>.*)/$",
    # changing to pk so that users can leave link field blank to ask questions
    url("^link/(?P<pk>\d+)/$",
        LinkDetail.as_view(),
        name="link_detail"),
    url("^users/(?P<username>.*)/links/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/links/$",
        LinkList.as_view(), {"by_score": False},
        name="link_list_user"),
    url("^users/(?P<username>.*)/comments/$",
        CommentList.as_view(), {"by_score": False},
        name="comment_list_user"),

    # Feeds
    url(r"^rss/$", RssFeed()),
    url(r"^atom/$", AtomFeed()),
    
    # Robots
    url(r"^robots\.txt$", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
)
