const closeModalBtns = document.querySelectorAll("#close-create-category-modal, #close-update-category-modal, \
                                                  #close-delete-category-modal, #close-add-transaction-modal, \
                                                  #close-update-transaction-modal, #close-delete-transaction-modal");

// Add event listeners on each button that closes a modal
closeModalBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (btn === document.getElementById("close-create-category-modal")) {
      modal = document.getElementById("create-category-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    } else if (btn === document.getElementById("close-update-category-modal")) {
      modal = document.getElementById("update-category-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    } else if (btn === document.getElementById("close-delete-category-modal")) {
      modal = document.getElementById("delete-category-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    } else if (btn === document.getElementById("close-add-transaction-modal")) {
      modal = document.getElementById("add-transaction-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    } else if (btn === document.getElementById("close-update-transaction-modal")) {
      modal = document.getElementById("update-transaction-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    } else if (btn === document.getElementById("close-delete-transaction-modal")) {
      modal = document.getElementById("delete-transaction-modal");
      modal.classList.remove("visible");
      modal.classList.add("hidden");
    }
    return;
  })
});

// Open create-category-modal
document.getElementById("create-category").addEventListener("click", () => {
  modal = document.getElementById("create-category-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Open update-category-modal
document.getElementById("update-category").addEventListener("click", () => {
  modal = document.getElementById("update-category-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Open delete-category-modal
document.getElementById("delete-category").addEventListener("click", () => {
  modal = document.getElementById("delete-category-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Open add-transaction-modal
document.getElementById("add-transaction").addEventListener("click", () => {
  modal = document.getElementById("add-transaction-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Open update-transaction-modal
document.getElementById("update-transaction").addEventListener("click", () => {
  modal = document.getElementById("update-transaction-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Open delete-transaction-modal
document.getElementById("delete-transaction").addEventListener("click", () => {
  modal = document.getElementById("delete-transaction-modal");
  modal.classList.remove("hidden");
  modal.classList.add("visible");
  return;
});

// Remove alert message element
document.getElementById("alert-message-btn").addEventListener("click", () => {
  alertMessage = document.getElementById("alert-message");
  alertMessage.remove();
});