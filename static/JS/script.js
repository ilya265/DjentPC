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