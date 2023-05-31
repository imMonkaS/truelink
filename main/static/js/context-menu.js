window.onload = function () {
    document.querySelector("#open_menu").addEventListener("click", function (e) {
        e.preventDefault();
        if (document.querySelector("#open_menu").classList.contains('is-active')) {
            document.querySelector("#open_menu").classList.remove("is-active");
            document.querySelector('.context-menu').style.display = "none";

        }
        else {
            document.querySelector("#open_menu").classList.add("is-active");
            document.querySelector('.context-menu').style.display = "block";

        }
    });
}