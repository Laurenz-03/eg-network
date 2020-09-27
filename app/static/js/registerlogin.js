const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_in_btn.addEventListener("click", () => {
  //window.history.pushState("page2", "Title", "/login?mode=login");
  history.pushState({}, null, "/login?mode=login");
  container.classList.remove("sign-up-mode");
});

sign_up_btn.addEventListener("click", () => {
    //window.history.pushState("page2", "Title", "/login?mode=register");
    history.pushState({}, null, "/login?mode=register");

  container.classList.add("sign-up-mode");
});
