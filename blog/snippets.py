{% url 'user-posts' post.author.username %}
{% url 'post-detail' post.id %}

{% for comment in post.comments.all %}
      
          <img class="rounded-circle article-img" src="{{comment.author.profile.image.url}}">
          <div class="media-body">
            <div class="article-metadata">
              <a class="mr-2" href="{% url 'user-posts' comment.author.username %}">{{ comment.author }}</a>
              <small class="text-muted">{{ comment.date_posted|date:'d N Y' }}</small>
            </div>
            <p class="article-content">{{ comment.content }}</p>
          </div>
        
      {% endfor %}

{% url 'user-posts' comment.author.username %}

      {% url 'post-create'%}
      {% url 'profile'%}
      {% url 'logout'%}