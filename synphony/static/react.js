import React,{Component} from react;
// import '/CSS/additional.css'
class App extends Component {
    render() {
        return (
            <div className="App">
                <!DOCTYPE html>
<html lang="en">

<head>
  {% block js %}
  <script src="https://code.jquery.com/jquery-3.4.1.min.js"
    integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/js-cookie@beta/dist/js.cookie.min.js"></script>

  {% endblock %}
  {% load static %}
  <script type="text/javascript" src="{% static 'js/playMusic.js' %}"></script>
  {% block extrajs %}
  {% endblock %}
  <meta charset="utf-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
 
  <title>{% block title %}Synphony{% endblock title %}</title>
  {% load static %}
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    crossorigin="anonymous">
  <link type="text/css" rel="stylesheet" href="{% static 'CSS/additional.css' %}" />
  {% block navbar %}
  <ul class="ul-base">
    {% if not request.user.is_anonymous %}
    <li class="navbar"><a href="{% url 'logout' %}">Logout</a></li>
    <li class="navbar"><a href="#">{{request.user}}</a></li>
    <li class="navbar"><a href="{% url 'studio' %}">Create Studio</a></li>
    {% else %}
    <li class="navbar"><a href="{% url 'login' %}">Login</a></li>
    {% endif %}
  </ul>
  {% endblock %}
</head>

<body>
  <h1 class='text-center'>Synphony</h1>
  <div class="container d-flex h-100">
    <div class="row justify-content-center">
        {% block main %}

        {% endblock %}
      </div>
    </div>
  </div>
</body>

{% block footer %}
<footer>
  <div class="footer text-center">
    <h6>©
      <script>
        document.write(new Date().getFullYear())
      </script>
      , made by Alan / Nicole / Mia / Suqi
    </h6>
  </div>
</footer>
{% endblock %}

</html>
            </div>
        );
    }
}
export default App;