let name = $('#updateSub-name');
let id = $('#updateSub-id');
let form = $('#edit-certain-video');

$('.editCustomVideo-btn').click(function(){
    let data_name = $(this).attr('data-name');
    let data_id = $(this).attr('data-id');

    console.log(data_id);
    console.log(data_name);

    name.val(data_name);
    id.val(data_id);
});