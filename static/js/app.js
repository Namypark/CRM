
// Function to toggle the dropdown
function toggleDropdown() {
    const dropdown = document.getElementById("user-menu");
    dropdown.classList.toggle("hidden");
}


function toggleMobileDropdown() {
    const dropdown = document.getElementById("mobile-menu");
    const closedIcon = document.getElementById("closed-icon");
    const openIcon = document.getElementById("open-icon");

    dropdown.classList.toggle("hidden")
    closedIcon.classList.toggle("hidden");
    openIcon.classList.toggle("hidden");

}


const myModal = new bootstrap.Modal("#myAlert")
document.querySelector(".close").addEventListener("click", () => {
    myModal.hide();
})




