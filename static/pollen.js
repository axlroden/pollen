$(function() {
    $.ajax({
        url: '/api/info',
        success: function (data) {
            $('#last_updated').html("Sidst opdateret: " + JSON.stringify(data['last_updated']).replace(/\"/g, ""));
            $('#el-øst').html(data['el_øst']);
            $('#el-vest').html(data['el_vest']);
            $('#hassel-øst').html(data['hassel_øst']);
            $('#hassel-vest').html(data['hassel_vest']);
            $('#elm-øst').html(data['elm_øst']);
            $('#elm-vest').html(data['elm_vest']);
            $('#birk-øst').html(data['birk_øst']);
            $('#birk-vest').html(data['birk_vest']);
            $('#græs-øst').html(data['græs_øst']);
            $('#græs-vest').html(data['græs_vest']);
            $('#bynke-øst').html(data['bynke_øst']);
            $('#bynke-vest').html(data['bynke_vest']);
        }
    });
 })