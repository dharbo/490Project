// const sqlite3 = require('sqlite3').verbose();

// let db = new sqlite3.Database('../../database.db', (err) => {              <= doesn't work, require needs other downloads
//     if (err) {
//       console.error(err.message);
//     }
//     console.log('Connected to the database.');
//   });
// console.log('Hello there')

// function getElt() {
//     return document.getElementById("create-category").innerText
// }


document.getElementById("create-category").addEventListener("click", ()=> {
    // open modal
    console.log("Open modal...")

    modal = document.getElementById("create-category-modal")
    modal.classList.remove("hidden")
    modal.classList.add("visible")

    console.log("It work!!!")

    return
  });

