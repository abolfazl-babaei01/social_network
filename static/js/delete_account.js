// $(document).ready(function (){
// $('#reason-deleting-account').on('submit', function (event){
//     event.preventDefault();
//     const selectedReason = $('input[name="reason"]:checked').val();
//     const csrfToken = $(this).data('csrf-token')
//     $.ajax({
//         type : 'POST',
//         url : '/account/deleted-account/',
//         data : {'selected_reason': selectedReason, 'csrfmiddlewaretoken': csrfToken},
//
//     })
//
// })
// })