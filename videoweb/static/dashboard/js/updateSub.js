let number = $('#updateSub-number');
let url = $('#updateSub-url');
let id = $('#updateSub-id');
let form = $('#update-form');
let status = false;

$('.updatesub-btn').click(function(){
    let videoSubId = $(this).attr('data-id');
    let videoSubNumber = parseInt($(this).attr('data-number'));
    let videoSubUrl = $(this).attr('data-url');

    if(status){
        status = false;
        form.hide();
    } else{
        number.val(videoSubNumber);
        url.val(videoSubUrl);
        id.val(videoSubId);
        status = true;
        form.show();
    }
});