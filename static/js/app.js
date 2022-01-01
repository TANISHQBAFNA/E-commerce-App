
// SOCIAL PANEL JS
const floating_btn = document.querySelector('.floating-btn');
const close_btn = document.querySelector('.close-btn');
const social_panel_container = document.querySelector('.social-panel-container');

floating_btn.addEventListener('click', () => {
	social_panel_container.classList.toggle('visible')
});

close_btn.addEventListener('click', () => {
	social_panel_container.classList.remove('visible')
});



    var LoginForm = document.getElementById("LoginForm");
    var RegForm = document.getElementById("RegForm");
    var Indicator = document.getElementById("indicator");

    function register(){
            RegForm.style.transform = "translateX(0px)";
            LoginForm.style.transform = "translateX(0px)";
            Indicator.style.transform = "translateX(100px)"
        };
    function login(){
            RegForm.style.transform = "translateX(300px)";
            LoginForm.style.transform = "translateX(300px)";
            Indicator.style.transform = "translateX(0px)"

        };



 $('button.cartbtn').click(function(){
     var cart_url = $(this).attr("data-ajax-url");
     var item_id = $(this).attr("data-item-id");
     $.ajax({

         // The URL for the request
         url: cart_url,
    // The data to send (will be converted to a query string)
    data: {
        item_id: item_id
    },

    // Whether this is a POST or GET request

 type: "POST",
    // The type of data we expect back
    dataType : "json",
    headers:{'X-CSRFToken': csrftoken},


})
  // Code to run if the request succeeds (is done);
  // The response is passed to the function
  .done(function( json ) {
      alert("done")
     //$( "<div class=\"content\">").html( json.html ).appendTo( "body" );
  })

  // Code to run if the request fails; the raw request and
  // status codes are passed to the function
  .fail(function( xhr, status, errorThrown ) {
    // alert( "Sorry, there was a problem!" );
    console.log( "Error: " + errorThrown );
    //console.log( "Status: " + status );
    //console.dir( xhr );
  })
  // Code to run regardless of success or failure;
  .always(function( xhr, status ) {
    alert( "The request is complete!" );
  });
 });
//


//      $.ajax({
//
//          // The URL for the request
//          url: url ,
//     // The data to send (will be converted to a query string)
//     data: {
//         username:$('#username').val(),
//         title:$('#title').val(),
//             comment:$('#comment').val(),
//     },
//
//     // Whether this is a POST or GET request
//          type: "POST",
//
//     // The type of data we expect back
//     dataType : "json",
//     headers:{'X-CSRFToken': csrftoken},
//
//  // Code to run if the request succeeds (is done);
//   // The response is passed to the function
//
// })
//   // Code to run if the request succeeds (is done);
//   // The response is passed to the function
//   .done(function( json ) {
//       alert("done")
//      //$( "<div class=\"content\">").html( json.html ).appendTo( "body" );
//   })
//
//
//   // Code to run if the request fails; the raw request and
//   // status codes are passed to the function
//   .fail(function( xhr, status, errorThrown ) {
//      alert( "Sorry, there was a problem!" );
//      console.log( "Error: " + errorThrown );
//     console.log( "Status: " + status );
//     console.dir( xhr );
//   })
//   // Code to run regardless of success or failure;
//   .always(function( xhr, status ) {
//     alert( "The request is complete!" );
//   });
//  });

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');