/**
 * Created by RaPoSpectre on 4/21/16.
 */

$('#tournamentList.item.card.a.image').dimmer({
    on: 'hover'
});
$('.special.cards .image').dimmer({
    on: 'hover'
});
function addPlayer() {
    $('#addModal')
        .modal('setting', 'closable', false)
        .modal('setting', 'transition', 'horizontal flip')
        .modal('show');
};
$(document).on('change', '.btn-file :file', function () {
    var input = $(this),
        numFiles = input.get(0).files ? input.get(0).files.length : 1,
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
    input.trigger('fileselect', [numFiles, label]);
    var files = input.get(0).files;
    for (var i = 0, f; f = files[i]; i++) {
        if (!f.type.match('image.*')) {
            continue;
        }
        var reader = new FileReader();
        reader.onload = (function (theFile) {
            return function (e) {
                document.getElementById('uploadPicture').src = e.target.result;

            };
        })(f);
        reader.readAsDataURL(f);
    }
});

$('#start_time').datepicker({
    format: 'yyyy-mm-dd'
});
$('#end_time').datepicker({
    format: 'yyyy-mm-dd'
});

$('.ui.accordion')
    .accordion()
;
$('#progress1').progress();
