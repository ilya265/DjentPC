function showOrders(){
  $('button')[2].style="color:white;background-color:black"
  $('button')[1].style="color:black;background-color:white"
  $('button')[0].style="color:white;background-color:black"

  $('.products')[0].style="display:none"
  $('.orders')[0].style="display:block"
  $('.reserved_boards')[0].style="display:none"
}

function showProducts(){
  $('button')[0].style="color:black;background-color:white"
  $('button')[1].style="color:white;background-color:black"
  $('button')[2].style="color:white;background-color:black"

  $('.products')[0].style="display:flex"
  $('.orders')[0].style="display:none"
  $('.reserved_boards')[0].style="display:none"
}

function showReservedBoards(){
  $('button')[0].style="color:white;background-color:black"
  $('button')[1].style="color:white;background-color:black"
  $('button')[2].style="color:black;background-color:white"

  $('.products')[0].style="display:none"
  $('.orders')[0].style="display:none"
  $('.reserved_boards')[0].style="display:block"
}

$('#form').submit(function(event) {
    event.preventDefault();

    array = $("#form input")
    validation = true

    for (i=0, len=array.length; i != len; i++){

      $('#form .input')[i].style= ''
      
      if (array[i].validity.valid == false){
        $('#form .input')[i].style= 'border: 3px solid red'

        validation = false
      }
    }

    if (validation == true){
      formData = new FormData(this);
      additionalData = {'action': 1}

      for (var key in additionalData) {
          formData.append(key, additionalData[key]);
      }


      $.ajax({
          type: 'POST',
          url: '',
          data: (formData),
          contentType: false,
          processData: false,
          success: function(response) {
              if (response == 'success'){
                $('.add_item')[0].style.background='lime'
                setTimeout(function() {
                  $('.add_item')[0].style.background = ''
                }, 3000);
              }
              else{
                $('.add_item')[0].style.background='red'
                setTimeout(function() {
                  $('.add_item')[0].style.background = ''
                }, 3000);
              }
          }
      });
    }
});

function clear_form(){
    arr = $('#form input')

    for (i=0, len=arr.length; i != len; i++){
        arr[i].value = ''
    }
}

function changeBoard(id){


  price = $('.product.'+ id + ' input[name="price"]')[0].value
  quantity = $('.product.'+ id + ' input[name="quantity"]')[0].value
  delete_ = $('.product.'+ id + ' input[name="del"]')[0].checked
  data = {
    'price': price,
    "quantity": quantity,
    'delete': delete_,
    'product_id': id,
    'action': 2,
  }
  $.ajax({
    type: 'POST',
    url: '',
    data: data,
    success: function(response) {
        if (response == 'success'){
          $('.product.'+ id)[0].style.background='lime'
          setTimeout(function() {
            $('.product.'+ id)[0].style.background = ''
          }, 3000)
        }else{
          $('.product.'+ id)[0].style.background='red'
          setTimeout(function() {
            $('.product.'+ id)[0].style.background = ''
          }, 3000)
        }

    }
  });
}

function changeOrderStatus(id){

  value = $(".order."+id+ ' select')[0].value
  data={
    'action':3,
    'status':value,
    'order_id': id,
  }
  $(".order."+id)[0].style.opacity= ''

  if (value == ''){
  }

  else if(value == 1){ $(".order."+id)[0].style.background='#8bf78b' }

  else if(value == 2){ $(".order."+id)[0].style.opacity='0.4' }

  else if(value == 3){ $(".order."+id)[0].style.background='#f1f184' }


  $.ajax({
    type: 'POST',
    url: '',
    data: data,
    success: function(response) {
    }
  });
}

function changeReservedStatus(personal_num){
  value = $('.big_wrapper.'+personal_num + ' select')[0].value
  data={
    'action':4,
    'status':value,
    'personal_num': personal_num,
  }

  if (value == 0){}
  else if (value == 1){ $('.big_wrapper.'+personal_num)[0].style.background='#8bf78b' }
  else if (value == 2){
    $('.big_wrapper.'+personal_num)[0].style.background='#f36666'
    $('.big_wrapper.'+personal_num + ' select option[value="1"]')[0].remove();
    $('.big_wrapper.'+personal_num + ' select option[value="3"]')[0].remove();
  }
  else if (value == 3){ $('.big_wrapper.'+personal_num)[0].style.background='#f1f184' }

  $.ajax({
    type: 'POST',
    url: '',
    data: data,
    success: function(response) {
    }
  });
}