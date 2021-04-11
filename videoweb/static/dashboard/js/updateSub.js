let number = $('#updateSub-number');
let url = $('#updateSub-url');
let id = $('#updateSub-id');

$('.updatesub-btn').click(function(){
    let videoSubId = $(this).attr('data-id');
    let videoSubNumber = parseInt($(this).attr('data-number'));
    let videoSubUrl = $(this).attr('data-url');

    number.val(videoSubNumber);
    url.val(videoSubUrl);
    id.val(videoSubId);
});