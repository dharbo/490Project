// TODO: Add for transactions modals
const closeModalBtns = document.querySelectorAll("#close-create-category-modal, #close-update-category-modal, #close-delete-category-modal, #close-add-transaction-modal")

console.log(closeModalBtns)

closeModalBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    console.log(btn.getAttribute("id"))

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
    } else if (btn.getAttribute("id") === "close-add-transaction-modal") {
      modal = document.getElementById("add-transaction-modal")
      modal.classList.remove("visible")
      modal.classList.add("hidden")
    }

    return
  })
});

// Open create-category-modal
document.getElementById("create-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("create-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});

// Open update-category-modal
document.getElementById("update-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("update-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});

// Open delete-category-modal
document.getElementById("delete-category").addEventListener("click", ()=> {
  // open modal
  console.log("Open modal...")

  modal = document.getElementById("delete-category-modal")
  modal.classList.remove("hidden")
  modal.classList.add("visible")

  console.log("It work!!!")

  return
});

// Open add-transaction-modal
const openAddTransactionModalBtns = document.getElementsByClassName("bg-[#85bb65] px-4 h-7 rounded border border-black hover:text-white hover:scale-125")
for (let btn of openAddTransactionModalBtns) {
  console.log(btn.id)
  // console.log(btn.id.split("add-transaction-").filter(item => item)[0])
  btn.addEventListener("click", () => {
    modal = document.getElementById("add-transaction-modal")
    // modal.dataset.categoryName = btn.id.split("add-transaction-").filter(item => item)[0]
    modal.classList.remove("hidden")
    modal.classList.add("visible")
  })
};