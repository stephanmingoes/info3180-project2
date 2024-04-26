<template>
  <header>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <div class="container-fluid">
        <a class="navbar-brand logo-font text-lg font-bold" href="/"
          >Photogram</a
        >
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore">Explore</RouterLink>
            </li>
            <li class="nav-item" @click="logout">
              <a class="nav-link lo">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { useRouter } from "vue-router";
import { authenticationAxiosInstance } from "../api";
import { onMounted } from "vue";

const router = useRouter();

async function logout() {
  try {
    await authenticationAxiosInstance.post("/api/v1/auth/logout");
    localStorage.removeItem("jwt_token");
    router.push("/login");
  } catch (error) {
    console.log(error);
  }
}

onMounted(async () => {});
</script>

<style>
.lo {
  cursor: pointer;
}
</style>
