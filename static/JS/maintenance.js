function show_popup(){
    $('.popup')[0].style=('display: flex')
    setTimeout(function(){
        $('.popup .window')[0].style=('top: 0')
    },1)
}


$("#button").click(function(event) {
    event.preventDefault()
})

function popupFormHide(){

    input_arr = $('input')
    valid = true

    outer:
    for (len=input_arr.length, i=0; i != len; i++){
        // validation
        input_arr[i].style.border=''
        if (input_arr[i].validity.valid == false){
            input_arr[i].style.border='3px red solid'
            $('.not_valid')[0].style.display = 'block';
            valid = false;
            break 
        }
    }

    if (valid == true){

        formData = $('#form').serialize();

        $.ajax({
            type: "POST",
            url: "",
            data: formData,
            success: function(response) {

            if (response == 'error'){
                $('.window h3')[0].innerText = "Error. Please try later"
                $('.window h3')[0].style.color = 'red'
                }
            },
        })

        $('form')[0].style.opacity='0'
        $('.window h3')[0].style.opacity='0'
        $('.window p')[0].style.opacity='0'

        setTimeout(function(){
            $('form')[0].style.display='none'
            $('.window h3')[0].style.display='none'
            $('.window p')[0].style.display='none'
            $('.window h2')[0].style.display='block'
        },500)

        setTimeout(function(){
            $('.window h2')[0].style='display: block; opacity: 1'
        },800)
    }

}