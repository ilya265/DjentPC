

//header_adaptive ////////////////////////////////////////////////////
function header_adaptive(){
}


menu_btn_status = 0;


function rotateMenuBtn(status){
    if (status == 0){
        document.querySelectorAll('.button div')[0].style="transform:rotate(45deg);top: 7px;"
        document.querySelectorAll('.button div')[1].style="transform:rotate(-45deg);top: -6px;"


        document.querySelectorAll('.drop_down_menu')[0].style="display:block;top: 80px;"
        document.querySelectorAll('.header_flexbox')[0].style="background-color: black"
        menu_btn_status = 1
    }

    else if (status == 1){
        document.querySelectorAll('.button div')[0].style="top: none;transform:rotate(0deg);"
        document.querySelectorAll('.button div')[1].style="top: none;transform:rotate(0deg);"

        document.querySelectorAll('.drop_down_menu')[0].style="top: -70%;"
        document.querySelectorAll('.header_flexbox')[0].style="background-color: rgba(0, 0, 0, 0.5);"
        menu_btn_status = 0
    }

}

function show_popup(){
    document.querySelectorAll('.popup')[0].style=('display: flex')
    setTimeout(function(){
        document.querySelectorAll('.popup .window')[0].style=('top: 0')
    },1)
}

index = 0
productInBasket_arr = []
while (document.querySelectorAll('.product button').length > index){
    productInBasket_arr[index] = 0
    index +=1
    }

function popupFormHide(){
    valid = true
    input_arr = document.querySelectorAll('input')
    index = 0
    while (index < input_arr.length){
        if (input_arr[index].validity.valid == true){
            console.log("валидация прошла")
        }
        else{
            valid = false
            console.log('валидация не прошла')
        }
        index += 1
    }

    if (valid == true){
        document.querySelectorAll('form')[0].style='opacity:0'
        document.querySelectorAll('.window h3')[0].style='opacity:0'
        document.querySelectorAll('.window p')[0].style='opacity:0'

        setTimeout(function(){
            document.querySelectorAll('form')[0].style='display:none'
            document.querySelectorAll('.window h3')[0].style='display:none'
            document.querySelectorAll('.window p')[0].style='display:none'
            document.querySelectorAll('.window h2')[0].style='display:block;'
        },500)

        setTimeout(function(){
            document.querySelectorAll('.window h2')[0].style='display: block; opacity: 1'
        },800)
        input_arr = document.querySelectorAll('form').submit()
    }

}




function addToBasket(index){
    index *= 1
    button = document.querySelectorAll('.product button')[index]
    if (productInBasket_arr[index] == 0){
        button.style=('background-color:white;color:black;')
        button.textContent = "В корзине"
        productInBasket_arr[index] = 1;
    }
    else{
        button.style=('background-color:black;color:white;')
        button.textContent = "Добавить в корзину"
        productInBasket_arr[index] = 0;
    }
}

basket_section_status = 0;
isAnyItemSelected = 0;
//если кнопка прожата, то при нажатии на корзину кнопка заказать больше не появляется
pulledTradeButton = 0;
// requestStr нужен чтобы собрать через запятую все id и положить их в форму под кнопкой заказать
function showBasket(){
    requestStr = ''
    if (basket_section_status == 0){
        document.querySelectorAll('.basket')[0].textContent='Каталог'

        if (pulledTradeButton == 0){
            document.querySelectorAll('.trade_button')[0].style='display:block'
        }
        else{
            document.querySelectorAll('.trade_text')[0].style='display:block'
        }

        index = 0
        isAnyItemSelected = 0
        while (document.querySelectorAll('.product').length > index){

            if (productInBasket_arr[index] == 0){
                document.querySelectorAll('.product')[index].style="display:none"
            }
            else{
                isAnyItemSelected = 1;
            }
            /////
            if (document.querySelectorAll('.product')[index].style.display != 'none'){
                requestStr += document.querySelectorAll('.product input')[index].value + ','
            }
            /////
            index +=1
        }
        if (isAnyItemSelected == 0){
            document.querySelectorAll('.empty')[0].style='display:block'
            document.querySelectorAll('.trade_button')[0].style='display:none'
        }
    basket_section_status = 1;
    document.querySelectorAll('form input')[0].value = requestStr
    }
    else{
        document.querySelectorAll('.basket')[0].textContent='Корзина'
        document.querySelectorAll('.trade_button')[0].style='display:none'
        document.querySelectorAll('.empty')[0].style='display:none'
        document.querySelectorAll('.trade_text')[0].style='display:none'
        index = 0
        while (document.querySelectorAll('.product').length > index){
            document.querySelectorAll('.product')[index].style="display:flex"
            index +=1
        }
        basket_section_status = 0;
    }
    
}

function showTradeText(){
        document.querySelectorAll('.trade_text')[0].style='display: block'
        document.querySelectorAll('.trade_button')[0].style='display:none'
        pulledTradeButton = 1
}

function showFilters(){
        document.querySelectorAll('.catalog .search_panel')[0].style="left: 0"
        document.querySelectorAll('.catalog .close_panel')[0].style="display: block"
}

function closeFilters(){
    document.querySelectorAll('.catalog .search_panel')[0].style="left: -284px"
    document.querySelectorAll('.catalog .close_panel')[0].style="display: none"
}

//8 zeros cus 8 possible filters (processor,frequency,socket, etc...)
arrowsArray = [0,0,0,0,0,0,0]  

function changeArrow(index){
    if (arrowsArray[index] == 0){
    
    document.querySelectorAll(".arrow")[index].classList.remove('arrow_up')
    document.querySelectorAll(".arrow")[index].classList.add('arrow_down')
    document.querySelectorAll(".div_for_hide")[index].style="display: none"
    arrowsArray[index] = 1
    }
    else{
    document.querySelectorAll(".arrow")[index].classList.remove('arrow_down')
    document.querySelectorAll(".arrow")[index].classList.add('arrow_up')
    document.querySelectorAll(".div_for_hide")[index].style="display: hide"
    arrowsArray[index] = 0
    }
}

selectedFilters = 0
function reviewSelectedFilters(){
    checkboxesArr = document.querySelectorAll('input[type=checkbox]')
    index = 0
    checkedBoxesArr={'processor':'','frequency':'','socket':'','cores':'','threads':'','ram_size':'','ram_type':''}
    while (index < checkboxesArr.length){
        if (checkboxesArr[index].checked == true){
            document.querySelectorAll('.apply_filters')[0].style='display:block'
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
    requestStr =  "catalog?"
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
    document.querySelectorAll('.apply_filters')[0].attributes.href.value = requestStr
}
