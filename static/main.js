const form = document.querySelector("#user_form");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/users");
  const data = await response.json();
  users = data;
  renderUsers(users);
});
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = form["username"].value;
  const email = form["email"].value;
  const password = form["password"].value;

  if (!editing) {
    const response = await fetch("/api/users", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        email,
        password,
      }),
    });
    const data = await response.json();
    users.push(data);
  } else {
    const response=await fetch(`/api/users/${userId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username,
            email,
            password,
        }),
    });
    const updatedUser = await response.json();
    users=users.map(user=>user.id===updatedUser.id?updatedUser:user);
    editing=false;
    userId=null;
  }
  renderUsers(users);
  window.location.reload();
  form.reset();
});

const renderUsers = (users) => {
  const user_list = document.querySelector("#users_list");

  users.forEach((user) => {
    user_list.innerHTML += `
        <div class="user">
          <div class="container-buttons">
            <button onclick="editUser(${user.id})" class="edit">Edit</button>
            <button onclick="deleteUser(${user.id})" class="delete">Delete</button>
          </div>
          <div>
            <h4>${user.username}</h4>
            <h4>${user.email}</h4>
            <h4 class="truncate">${user.password}</h4>
          </div>
        </div>
        `;
  });
};
const deleteUser = async (id) => {
  const response = await fetch(`/api/users/${id}`, {
    method: "DELETE",
  });
  const data = await response.json();

  window.location.reload();
};
const editUser = async (id) => {
  const response = await fetch(`/api/users/${id}`, {
    method: "GET",
  });
  const data = await response.json();
  form["username"].value = data.username;
  form["email"].value = data.email;

  editing = true;
  userId = id;
};
