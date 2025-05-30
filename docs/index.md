# Internal Actions Marketplace

<style>
.cards {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1rem;
}
.card {
  background: #0d1117;
  padding: 1rem;
  width: 250px;
  border-radius: 10px;
  border: 1px solid #444;
  color: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.card h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
}
.card p {
  font-size: 0.9rem;
  color: #ccc;
}
.card a {
  color: #58a6ff;
  text-decoration: none;
  font-weight: bold;
}
.card a:hover {
  text-decoration: underline;
}
</style>

<div class="cards">
  <div class="card">
    <h4>Compile C Code</h4>
    <p>Compiles a given C source file using GCC.</p>
    <p><a href="actions/compile/">View Action</a></p>
  </div>

  <div class="card">
    <h4>Static Code Analysis</h4>
    <p>Runs cppcheck on a given C file.</p>
    <p><a href="actions/cppcheck/">View Action</a></p>
  </div>
</div>
