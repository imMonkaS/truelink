document.querySelector('.search-field').onfocus = function(){
    document.querySelector('.search').style.border = '#3376F6 solid 1px';
}

document.querySelector('.search-field').onblur = function(){
    document.querySelector('.search').style = '';
}