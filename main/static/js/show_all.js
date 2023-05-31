$('p.more').hide()
$('label.showmemore').click(function(){
    if (this.classList.contains('is-active'))
    {
        this.classList.remove("is-active");
        $(this).html("Скрыть");
    }
    else
    {
        this.classList.add("is-active");
        $(this).html("Показать полностью");
    }
    $(this).prev('p').slideToggle(300);
})