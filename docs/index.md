<style>
.cards { display: flex; flex-wrap: wrap; gap: 1rem; }
.card {
  background: #0d1117;
  padding: 1rem;
  width: 250px;
  border-radius: 10px;
  border: 1px solid #444;
  color: white;
}
.card a { color: #58a6ff; text-decoration: none; }
</style>

<div class="cards">
  {% for action in config.nav[1]['Actions'] %}
  {% for name, path in action.items() %}
  <div class="card">
    <h4>{{ name }}</h4>
    <p><a href="{{ path }}">View Action</a></p>
  </div>
  {% endfor %}
  {% endfor %}
</div>
