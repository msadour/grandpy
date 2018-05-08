function initMap(latitude, longitude, is_call=false) {
    if(is_call == true){
        $('#map').css( "display", "block" );
        var zoom = 13
        var position = {lat: parseFloat(latitude), lng: parseFloat(longitude)};
    }
    else {
        var zoom = 1
        var uluru = {lat: parseFloat(0), lng: parseFloat(0)};
    }

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: zoom,
      center: position
    });
    var marker = new google.maps.Marker({
      position: position,
      map: map
    });
}

$(function() {
    $('#button').click(function() {
        var request = $('form').serialize();
        $.ajax({
            url: '/get_user_request',
            data: request,
            type: 'GET',
            success: function(response) {
                $('#content').css( "display", "none" );
                $('#map').css( "display", "none" );
                $('#adresse').css( "display", "none" );
                var response_json = JSON.parse(response)
                if (response_json.emplacement == false){
                    alert('Emplacement introuvable')
                }
                else if (response_json.description == false){
                    alert('Description introuvable')
                }
                else{
                    if (response_json['type_search'] == 'place'){
                        adresse = response_json['emplacement']['adresse']
                        $('#adresse').css( "display", "block" ).text("Adresse : " + adresse);
                        latitude = response_json['emplacement']['latitude']
                        longitude = response_json['emplacement']['longitude']
                        initMap(latitude, longitude, true)
                    }
                    else if(response_json['type_search'] == 'information'){
                        $('#description').text(response_json['description'])
                        $('#content').css( "display", "block" );
                    }
                    else if(response_json['type_search'] == 'place information'){
                        adresse = response_json['emplacement']['adresse']
                        $('#adresse').css( "display", "block" ).text("Adresse : " + adresse);
                        $('#description').text(response_json['description'])
                        latitude = response_json['emplacement']['latitude']
                        longitude = response_json['emplacement']['longitude']
                        initMap(latitude, longitude, true)
                        $('#content').css( "display", "block" );
                    }
                    else {
                        console.log("erreur")
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});