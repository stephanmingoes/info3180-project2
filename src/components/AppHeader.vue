<template>
  <header>
    <nav class="bg-primary fixed-top text-white p-3">
      <div class="flex flex-row justify-between items-center">
        <a class="logo-font text-lg font-bold" href="/">Photogram</a>

        <div class="flex flex-row justify-center items-center">
          <ul class="navbar-nav me-auto flex flex-row gap-4">
            <li class="nav-item" v-if="!isLoggedIn">
              <RouterLink to="/" class="nav-link">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/explore" v-if="isLoggedIn"
                >Explore</RouterLink
              >
            </li>
            <li class="nav-item" @click="goToMyProfile" v-if="isLoggedIn">
              <a class="nav-link lo">My Profile</a>
            </li>
            <li class="nav-item" @click="logout" v-if="isLoggedIn">
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
import { ref } from "vue";
import { isUserLoggedIn } from "../utils/functions";
const router = useRouter();
const isLoggedIn = ref(false);
async function logout() {
  try {
    await authenticationAxiosInstance.post("/api/v1/auth/logout");
    localStorage.removeItem("jwt_token");
    window.location.href = "/login";
  } catch (error) {
    console.log(error);
  }
}

async function goToMyProfile() {
  const { data } = await authenticationAxiosInstance.get("/api/v1/user");
  window.location.href = `/users/${data.id}`;
}

onMounted(async () => {
  isLoggedIn.value = await isUserLoggedIn();
});
</script>

<style>
.lo {
  cursor: pointer;
}
.color-white {
  color: white;
}
.nav-container {
  padding: 1rem;
}
</style>
