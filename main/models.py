from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.db.models.signals import pre_save
from Website_Evaluation_Using_Opinion_Mining.utils import unique_slug_generator
from django.urls import reverse
from operator import itemgetter
from itertools import groupby
from .apps import MainConfig


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    website_url = models.URLField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.author) + ' on ' + str(self.date.date())

    def get_absolute_url(self):
        return reverse('home')


def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(slug_generator, sender=Post)

def classify_comment(comment):
        if 0 <= comment <= 0.2:
            comment_score = 1
        elif 0.2 < comment <= 0.4:
            comment_score = 2
        elif 0.4 < comment <= 0.6:
            comment_score = 3
        elif 0.6 < comment <= 0.8:
            comment_score = 4
        elif 0.8 < comment <= 1:
            comment_score = 5
        else:
            comment_score = 'no sentiment predicted'
        return comment_score

def set_website_Rating(comments_queryset:QuerySet):
    clean_post=[]
    predicted_data=[]
    sentiment_score_data=[]
    sum_comment_classify=[]
    i=0

        
    for comments in comments_queryset.iterator():
        clean_post.append(comments)
    clean_post.sort(key=itemgetter('post'))

    group_comments = []
    for key, items in groupby(clean_post, itemgetter('post')):
        lst = list(items)
        dt = len(lst)
        group_comments.append(lst)
    print(group_comments)
    print('-'*50)
    
    group_comments_size = len(group_comments)
    for item in group_comments:
        if i < group_comments_size:
            comments = group_comments[i]
            i=i+1
        size = len(item)
        total_sum_comment_classify=0
        for comment in comments:
            sentiment_score = MainConfig.textblob_score(comment['body'])
            sentiment_score_dummy = MainConfig.textblob_score_PA(comment['body'])
            print(type(sentiment_score))
            if sentiment_score[0] == 'pos':
                score_to_be_parsed = sentiment_score[1]
            else:
                score_to_be_parsed = sentiment_score[2]
            print(sentiment_score_dummy, sentiment_score[0], score_to_be_parsed)
            comment_classify = classify_comment(score_to_be_parsed)
            total_sum_comment_classify += comment_classify
            id = comment['post']
            sentiment_score_data.append({comment['post']:sentiment_score})
            predicted_data.append({'post': comment['post'], 'body':comment['body'], 'score': sentiment_score, 'comment score': comment_classify})
        average_rating = total_sum_comment_classify / size
        sum_comment_classify.append([ id, average_rating])

    print('-'*50)    
    print(predicted_data)
    print('-'*50)

    return sum_comment_classify


def evaluate_website(comments_queryset: QuerySet, pk):
    
    posts = Comment.objects.filter(post_id = pk).values('post', 'body')
    clean_post=[]
    clean_post_comment=[]
    latest_data={}
    sum_comment_classify=[]
    i=0
    
    for post in posts.iterator():
        clean_post_comment.append(post)

    if len(clean_post_comment):
        latest_data = clean_post_comment[-1]
        
    for comments in comments_queryset.iterator():
        clean_post.append(comments)
    clean_post.sort(key=itemgetter('post'))

    group_comments = []
    dt = 0
    group_ratings={}
    for key, items in groupby(clean_post, itemgetter('post')):
        lst = list(items)
        dt = len(lst)
        group_comments.append(lst)
        group_ratings.update({lst[0]['post']: dt})
    

    old_rating = Rating.objects.values('post', 'rating')
    data_Rating = []

    for rate in old_rating.iterator():
        data_Rating.append(rate)
    
    if len(clean_post_comment):
        update_rating = MainConfig.textblob_score(latest_data['body'])
        new_rating = classify_comment(update_rating[1])
        print(group_ratings[pk] - 1)
        average_rating=0
        for item in data_Rating:
            if item['post'] == pk and group_ratings[pk]:
                sum_rating = (group_ratings[pk] - 1) * item['rating'] + new_rating
                average_rating = sum_rating / group_ratings[pk]
                print('inside', average_rating)
        print('outside', average_rating)
        if Rating.objects.filter(post_id = pk).exists():
            Rating.objects.filter(post_id=pk).update(post_id = pk, rating = average_rating)
        else:
            Rating.objects.create(post_id = pk, rating = average_rating)

    return sum_comment_classify

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' %(self.post.title, self.name)

class Rating(models.Model):
    post = models.ForeignKey(Post,related_name="ratings", on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return '%s' %(self.post.title)
