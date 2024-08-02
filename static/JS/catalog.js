

function showFilters(){
    $('.catalog .search_panel')[0].style="left: 0"
    $('.catalog .close_panel')[0].style="display: block"
}

function closeFilters(){
    $('.catalog .search_panel')[0].style="left: -284px"
    $('.catalog .close_panel')[0].style="display: none"
}

//8 zeros cus 8 possible filters (processor,frequency,socket, etc...)
arrowsArray = [0,0,0,0,0,0,0]  

function changeArrow(index){
    if (arrowsArray[index] == 0){
    
    $(".arrow")[index].classList.remove('arrow_up')
    $(".arrow")[index].classList.add('arrow_down')
    $(".div_for_hide")[index].style="display: none"
    arrowsArray[index] = 1
    }
    else{
    $(".arrow")[index].classList.remove('arrow_down')
    $(".arrow")[index].classList.add('arrow_up')
    $(".div_for_hide")[index].style="display: hide"
    arrowsArray[index] = 0
    }
}

selectedFilters = 0
function reviewSelectedFilters(){
    checkboxesArr = $('input[type=checkbox]')
    index = 0
    checkedBoxesArr={'processor':'','frequency':'','socket':'','cores':'','threads':'','ram_size':'','ram_type':''}
    while (index < checkboxesArr.length){
        if (checkboxesArr[index].checked == true){
            $('.apply_filters')[0].style='display:block'
            index2 = 0
            if (checkboxesArr[index].attributes.key.value == "processor"){
                checkedBoxesArr.processor += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "frequency"){
                checkedBoxesArr.frequency += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "socket"){
                checkedBoxesArr.socket += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "cores"){
                checkedBoxesArr.cores += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "threads"){
                checkedBoxesArr.threads += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "ram_size"){
                checkedBoxesArr.ram_size += checkboxesArr[index].value + ','
            }

            if (checkboxesArr[index].attributes.key.value == "ram_type"){
                checkedBoxesArr.ram_type += checkboxesArr[index].value + ','
            }
        }
        index += 1
    }

    filters_is_on = false
    arr = $("input[type='checkbox']")
    for (i = arr.length - 1; i != -1; i--) {
    
        if (arr[i].checked == true) {
            filters_is_on = true
        }
    }
    if (filters_is_on == false){
        $('.apply_filters')[0].style.display = 'none'
    }

    requestStr =  "catalog?filters=1&"
    if (checkedBoxesArr.processor != ''){
        requestStr += "processor=" + checkedBoxesArr.processor + "&"
    }
    if (checkedBoxesArr.frequency != ''){
        requestStr += "frequency=" + checkedBoxesArr.frequency + "&"
    }
    if (checkedBoxesArr.socket != ''){
        requestStr += "socket=" + checkedBoxesArr.socket + "&"
    }
    if (checkedBoxesArr.cores != ''){
        requestStr += "cores=" + checkedBoxesArr.cores + "&"
    }
    if (checkedBoxesArr.threads != ''){
        requestStr += "threads=" + checkedBoxesArr.threads + "&"
    }
    if (checkedBoxesArr.ram_size != ''){
        requestStr += "ram_size=" + checkedBoxesArr.ram_size + "&"
    }
    if (checkedBoxesArr.ram_type != ''){
        requestStr += "ram_type=" + checkedBoxesArr.ram_type
    }
    $('.apply_filters')[0].attributes.href.value = requestStr
}


basket_arr = []
function addToBasket(product_id){
    product_id *= 1
    button = $('.product[value=' + product_id + '] button')[0]
    if (basket_arr.indexOf(product_id) == -1){
        button.style=('background-color:white;color:black;')
        button.textContent = "In cart"

        basket_arr.push(product_id)
    }
    else{
        button.style=('background-color:black;color:white;')
        button.textContent = "Add to cart"

        basket_arr.splice(basket_arr.indexOf(product_id), 1)
        
    }
}


products_arr = $('.product')
function showBasket(){

    if ($('.basket')[0].value == 'open'){

        for (length = products_arr.length, i = 0; i != length; i++) {
            products_arr[i].style.display = '';
        }

        $('.basket')[0].value = 'closed'
        $('.basket')[0].innerText='Cart'

        $('.empty')[0].style.display='none'
        $('.empty')[1].style.display='none'
        $('.trade_button')[0].style.display='none'
        $('.personal_num')[0].style.display = 'none'

    }
    else{

        if (pulledTradeButton == 0){
            $('.trade_button')[0].style.display='block'
        }
        else{
            $('.personal_num')[0].style.display = 'block'
        }

        if (basket_arr.length == 0){
            for (length = products_arr.length, i = 0; i != length; i++) {
                products_arr[i].style.display = 'none';
            }

            $('.trade_button')[0].style.display='none'
            $('.empty')[0].style.display='block'
            $('.empty')[1].style.display='block'
        }
        else{
            products_arr = $('.product')
            for (length = products_arr.length, i = 0; i != length; i++) {
                products_arr[i].style.display = 'none';
            }
            for (length = basket_arr.length, i = 0; i != length; i++) {
                $('.product[value=' + basket_arr[i] + ']')[0].style.display=''
            }
        }
        $('.basket')[0].value = 'open'
        $('.basket')[0].innerText='Products'

        
    }
}


//variable for basket button. Button pulled once and hide forever
pulledTradeButton = 0;
function reserveOrder(){

    $.ajax({
        type: 'POST',
        url: '/reserved_board',
        data: JSON.stringify(basket_arr),
        contentType: 'application/json',
        dataType: 'json',
        success: function(response) {
          $('.personal_num')[0].innerText = 'ORDER ID: ' + response.personal_num
        },
      });


    $('.trade_text')[0].style.display= 'block'
    $('.trade_button')[0].style.display ='none'

    $('.personal_num')[0].style.display = 'block'
    pulledTradeButton = 1
}