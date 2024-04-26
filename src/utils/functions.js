import { authenticationAxiosInstance } from "../api";

export async function isUserLoggedIn() {
  try {
    await authenticationAxiosInstance.get("/api/v1/is_logged_in");
    return true;
  } catch (error) {
    return false;
  }
}
export async function logoutUser() {
  try {
    await authenticationAxiosInstance.post("/api/v1/auth/logout");
    localStorage.removeItem("jwt_token");
    window.location.href = "/login";
  } catch (error) {
    console.log(error);
  }
}

export async function redirectLoggedInUser() {
  if (await isUserLoggedIn()) {
    window.location.href = "/explore";
  }
}

export async function redirectLoggedOutUser() {
  if (!(await isUserLoggedIn())) {
    window.location.href = "/login";
  }
}
