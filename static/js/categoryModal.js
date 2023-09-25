// TODO: Add for transactions modals
const closeModalBtns = document.querySelectorAll("#close-create-category-modal, #close-update-category-modal, #close-delete-category-modal")

console.log(closeModalBtns)

closeModalBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    console.log(modal)

    if (btn === document.getElementById("close-create-category-modal")) {
      modal = document.getElementById("create-category-modal")
      modal.classList.remove("visible")
      modal.classList.add("hidden")
    } else if (btn === document.getElementById("close-update-category-modal")) {
      modal = document.getElementById("update-category-modal")
      modal.classList.remove("visible")
      modal.classList.add("hidden")
    } else if (btn === document.getElementById("close-delete-category-modal")) {
      modal = document.getElementById("delete-category-modal")
      modal.classList.remove("visible")
      modal.classList.add("hidden")
    }

    return
  })
});

document.getElementById("create-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("create-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});

document.getElementById("update-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("update-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});

document.getElementById("delete-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("delete-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});