import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

// ### Create and assign all routes below to their respective pages

// - [ ]  `/` - Display the homepage of the web application.
// - [ ]  `/register` - Accepts user information and saves it to the database.
// - [ ]  `/login` - Accepts login credentials as username and password.
// - [ ]  `/logout` - Logout a user.
// - [ ]  `/explore` - View/Explore all posts by all users.
// - [ ]  `/users/{user_id}` - View user profile info as well as all Posts by that user.
// - [ ]  `/posts/new` - Allow the user to add a new post.

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/register",
      name: "register",
      component: () => import("../views/RegisterView.vue"),
    },
    {
      path: "/login",
      name: "login",
      component: () => import("../views/LoginView.vue"),
    },
    {
      path: "/logout",
      name: "logout",
      component: () => import("../views/LogoutView.vue"),
    },
    {
      path: "/explore",
      name: "explore",
      component: () => import("../views/ExploreView.vue"),
    },
    {
      path: "/users/:user_id",
      name: "users",
      component: () => import("../views/UsersView.vue"),
    },
    {
      path: "/posts/new",
      name: "newpost",
      component: () => import("../views/NewPostView.vue"),
    },
  ],
});

export default router;
